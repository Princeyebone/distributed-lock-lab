import httpx
import uuid
import time
import random

worker_id = str(uuid.uuid4())
lock_key = "order_123"

print(f"Worker {worker_id} trying to acquire lock")

response = httpx.post(
    "http://127.0.0.1:8001/lock/acquire",
    params={
        "lock_key": lock_key,
        "worker_id": worker_id
    }
)

data = response.json()

if data["lock_acquired"]:
    print(f"Worker {worker_id} acquired lock")

    # simulate work
    work_time = random.randint(2,5)
    print(f"Worker {worker_id} processing for {work_time} seconds")
    time.sleep(work_time)

    httpx.post(
        "http://127.0.0.1:8001/lock/release",
        params={
            "lock_key": lock_key,
            "worker_id": worker_id
        }
    )

    print(f"Worker {worker_id} released lock")

else:
    print(f"Worker {worker_id} failed to acquire lock")