import time
from functools import wraps

_cache = {}

def cache_ttl(ttl: int = 5):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = (func.__name__, args, tuple(kwargs.items()))
            now = time.time()

            # If cached and not expired
            if key in _cache:
                value, timestamp = _cache[key]
                if now - timestamp < ttl:
                    return value  # <-- RETURNS REAL VALUE, NOT COROUTINE

            # Otherwise call function properly
            value = await func(*args, **kwargs)  # <-- IMPORTANT!!
            _cache[key] = (value, now)
            return value

        return wrapper
    return decorator
