from .config import settings
from .redis_client import redis_client


def acquire_lock(lock_key:str, worker_id:str):
    result = redis_client.set(
        lock_key,
        worker_id,
        nx=True,
        ex=settings.LOCK_EXPIRY
    )

    return result is True

def release_lock(lock_key:str, worker_id:str):
    owner = redis_client.get(lock_key)

    if owner == worker_id:
        redis_client.delete(lock_key)
        return True
    
    return False

def renew_lock(lock_key:str, worker_id:str):
    owner = redis_client.get(lock_key)

    if owner == worker_id:
        # Extend the TTL
        result = redis_client.expire(lock_key, settings.LOCK_EXPIRY)
        return bool(result)
        
    return False