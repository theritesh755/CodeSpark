import redis
from config.settings import settings

def get_redis():
    try:
        client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=1)
        client.ping()
        return client
    except redis.RedisError:
        return None
