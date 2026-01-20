from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from redis import asyncio as redis
import json

redis_client: redis.Redis = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    redis_client = await redis.from_url("redis://localhost:6379", decode_responses=True)
    yield
    await redis_client.aclose()

app = FastAPI(lifespan=lifespan)

async def get_redis():
    return redis_client

# String
@app.post("/cache/{key}")
async def set_cache(key: str, value: str, ttl: int = 300, r: redis.Redis = Depends(get_redis)):
    await r.setex(key, ttl, value)
    return {"cached": True}

@app.get("/cache/{key}")
async def get_cache(key: str, r: redis.Redis = Depends(get_redis)):
    value = await r.get(key)
    if not value:
        raise HTTPException(404, "Not found")
    return {"value": value}

# Hash
@app.post("/users/{user_id}")
async def create_user(user_id: str, name: str, email: str, r: redis.Redis = Depends(get_redis)):
    await r.hset(f"user:{user_id}", mapping={"name": name, "email": email})
    return {"created": True}

@app.get("/users/{user_id}")
async def get_user(user_id: str, r: redis.Redis = Depends(get_redis)):
    user = await r.hgetall(f"user:{user_id}")
    if not user:
        raise HTTPException(404, "User not found")
    return user

# List (Queue)
@app.post("/queue/{name}")
async def enqueue(name: str, item: str, r: redis.Redis = Depends(get_redis)):
    await r.rpush(f"queue:{name}", item)
    return {"enqueued": True, "length": await r.llen(f"queue:{name}")}

@app.post("/queue/{name}/pop")
async def dequeue(name: str, r: redis.Redis = Depends(get_redis)):
    item = await r.lpop(f"queue:{name}")
    return {"item": item}

# Pub/Sub
@app.post("/publish/{channel}")
async def publish(channel: str, message: str, r: redis.Redis = Depends(get_redis)):
    count = await r.publish(channel, message)
    return {"subscribers": count}

# Rate Limiting
@app.get("/limited")
async def rate_limited_endpoint(r: redis.Redis = Depends(get_redis)):
    key = "rate:limited_endpoint"
    count = await r.incr(key)
    
    if count == 1:
        await r.expire(key, 60)
    
    if count > 10:
        raise HTTPException(429, "Rate limited")
    
    return {"remaining": 10 - count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)