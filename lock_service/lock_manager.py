# lock_manager.py
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def acquire_lock(lock_key: str, worker_id: str, ttl=30) -> bool:
    return redis_client.set(lock_key, worker_id, nx=True, ex=ttl)

def release_lock(lock_key: str, worker_id: str) -> bool:
    owner = redis_client.get(lock_key)
    if owner == worker_id:
        redis_client.delete(lock_key)
        return True
    return False

def renew_lock(lock_key: str, worker_id: str, ttl=30) -> bool:
    owner = redis_client.get(lock_key)
    if owner == worker_id:
        redis_client.expire(lock_key, ttl)
        return True
    return False

# Idempotency helpers
def job_completed(job_id: str) -> bool:
    return redis_client.get(f"job:{job_id}:done") == "true"

def mark_job_completed(job_id: str):
    redis_client.set(f"job:{job_id}:done", "true")