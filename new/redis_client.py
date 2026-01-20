from redis.asyncio import Redis

redis = Redis(
    host = "localhost",
    port=6379,
    decode_responses=True
)
#redis.asyncio.redis is non-blocking , and each redis clal uses await , fastapi even loop stays free to serve other requests.
