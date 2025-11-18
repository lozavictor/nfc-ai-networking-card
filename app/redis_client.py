import redis
from app.config import settings

redis_client = redis.StrictRedis.from_url(
    settings.redis_url,
    decode_responses=True
)

def test_connection():
    try:
        redis_client.ping()
        print("Redis Connection Successful")
    except redis.ConnectionError as e:
        print("Redis connection failed:", e)