import pickle

import redis
from functools import wraps

from starlette.responses import JSONResponse

from app.core.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=False
)

class RedisCache:
    @classmethod
    def delete(cls, key_pattern):
        keys_to_remove = list(redis_client.scan_iter(key_pattern))
        for key in keys_to_remove:
            try:
                redis_client.delete(key)
                print(f"Deleted cache key: {key}")
            except Exception as e:
                print(f"Error deleting cache key {key}: {e}")

    #TODO: Cache key generate method requires improvements for specific posts
    @classmethod
    def generate_cache_key(cls, f, *args, **kwargs):
        cache_key = f"{settings.environment.lower()}"
        user_id = kwargs.get('ums_user').id
        post_id = kwargs.get('post_id')

        if user_id:
            cache_key += f":user_id:{user_id}"
        if post_id:
            cache_key += f":post_id:{post_id}"
        else:
            cache_key = cache_key

        return cache_key


def redis_cache_result(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        cache_key = RedisCache.generate_cache_key(func, *args, **kwargs)
        result = redis_client.get(cache_key)
        if result is None:
            result = func(*args, **kwargs)
            redis_client.set(cache_key, pickle.dumps(result))
            return result
        else:
            return pickle.loads(result)

    return decorated_func

def invalidate_cache(user_id, post_id=None):
    base_key = f"{settings.environment.lower()}:user_id:{user_id}"
    if post_id:
        RedisCache.delete(f"{base_key}:post_id:{post_id}")
    else:
        RedisCache.delete(f"{base_key}*")

def flush_redis_client():
    try:
        redis_client.flushdb()
        return JSONResponse({'msg': 'Redis cache cleared'})
    except Exception as ex:
        return JSONResponse({'msg': f"Error: {ex}"})
