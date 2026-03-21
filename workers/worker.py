import httpx
import uuid
import time
import threading
import random

BASE_URL = "http://127.0.0.1:8002"

worker_id = str(uuid.uuid4())
lock_key = "order_123"

# Shared stop signal
stop_event = threading.Event()


def heartbeat():
    while not stop_event.is_set():
        time.sleep(10)

        try:
            response = httpx.post(
                f"{BASE_URL}/lock/renew",
                params={
                    "lock_key": lock_key,
                    "worker_id": worker_id
                },
                timeout=5
            )

            data = response.json()

            if not data["lock_renewed"]:
                print(f"[{worker_id}] ❌ Lost lock during heartbeat. Stopping work.")
                stop_event.set()

        except Exception as e:
            print(f"[{worker_id}] ⚠️ Heartbeat error: {e}")
            stop_event.set()


def process_job():
    total_time = random.randint(20, 40)
    print(f"[{worker_id}] Processing job for {total_time}s")

    for i in range(total_time):
        if stop_event.is_set():
            print(f"[{worker_id}] 🛑 Stopping job due to lost lock")
            return

        time.sleep(1)

    print(f"[{worker_id}] ✅ Job completed successfully")


def main():
    print(f"[{worker_id}] Attempting to acquire lock")

    response = httpx.post(
        f"{BASE_URL}/lock/acquire",
        params={
            "lock_key": lock_key,
            "worker_id": worker_id
        }
    )

    data = response.json()

    if not data["lock_acquired"]:
        print(f"[{worker_id}] ❌ Failed to acquire lock")
        return

    print(f"[{worker_id}] 🔐 Lock acquired")

    # Start heartbeat thread
    hb_thread = threading.Thread(target=heartbeat, daemon=True)
    hb_thread.start()

    # Process job
    process_job()

    # Stop heartbeat
    stop_event.set()
    hb_thread.join()

    # Release lock
    httpx.post(
        f"{BASE_URL}/lock/release",
        params={
            "lock_key": lock_key,
            "worker_id": worker_id
        }
    )

    print(f"[{worker_id}] 🔓 Lock released")


if __name__ == "__main__":
    main()