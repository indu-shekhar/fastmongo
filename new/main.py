from fastapi import FastAPI,Request,HTTPException
from redis_client import redis
import json
import asyncio

app = FastAPI(title="FastAPI + aioredis Demo")

@app.on_event("startup")
async def startup():
    await redis.ping()
    print("redis Connected")

@app.on_event("shutdown")
async def shutdown():
    await redis.close()

