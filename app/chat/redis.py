import redis

client = redis.Redis.from_url(
    "redis://localhost:6379/0",
    decode_responses=True,
)
