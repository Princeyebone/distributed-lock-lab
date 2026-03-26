# worker.py
import uuid
import time
import threading
import random
import httpx
from lock_service.lock_manager import acquire_lock, release_lock, renew_lock, job_completed, mark_job_completed

worker_id = str(uuid.uuid4())
lock_key = "order_123"
job_id = "order_123"

# Shared stop signal
stop_event = threading.Event()
TTL = 30
HEARTBEAT_INTERVAL = 10

def heartbeat():
    while not stop_event.is_set():
        time.sleep(HEARTBEAT_INTERVAL)
        try:
            renewed = renew_lock(lock_key, worker_id, ttl=TTL)
            if not renewed:
                print(f"[{worker_id}] ❌ Lost lock during heartbeat. Stopping work.")
                stop_event.set()
        except Exception as e:
            print(f"[{worker_id}] ⚠️ Heartbeat error: {e}")
            stop_event.set()

def process_job():
    if job_completed(job_id):
        print(f"[{worker_id}] ⚠️ Job already processed. Skipping.")
        return

    total_time = random.randint(20, 40)
    print(f"[{worker_id}] Processing job for {total_time}s")

    for i in range(total_time):
        if stop_event.is_set():
            print(f"[{worker_id}] 🛑 Stopping job due to lost lock")
            return

        # Simulate random crash (5% chance per second)
        if random.random() < 0.05:
            print(f"[{worker_id}] 💥 Simulated crash!")
            raise Exception("Worker crashed unexpectedly")

        time.sleep(1)

    mark_job_completed(job_id)
    print(f"[{worker_id}] ✅ Job completed successfully")

def main():
    print(f"[{worker_id}] Attempting to acquire lock")
    if not acquire_lock(lock_key, worker_id, ttl=TTL):
        print(f"[{worker_id}] ❌ Failed to acquire lock")
        return

    print(f"[{worker_id}] 🔐 Lock acquired")

    # Start heartbeat thread
    hb_thread = threading.Thread(target=heartbeat, daemon=True)
    hb_thread.start()

    # Process the job
    try:
        process_job()
    except Exception as e:
        print(f"[{worker_id}] 💥 Worker crashed: {e}")

    # Stop heartbeat and release lock
    stop_event.set()
    hb_thread.join()
    release_lock(lock_key, worker_id)
    print(f"[{worker_id}] 🔓 Lock released")

if __name__ == "__main__":
    main()