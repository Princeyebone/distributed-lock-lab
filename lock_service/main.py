from fastapi import FastAPI
from .lock_manager import acquire_lock, release_lock

app  = FastAPI(title="Lock service")

@app.post("/lock/acquire")
def acquire(lock_key:str, worker_id:str):
    success = acquire_lock(lock_key, worker_id)
    return{
        "lock_key":lock_key,
        "worker_id":worker_id,
        "lock_acquired":success
    }

@app.post("/lock/release")
def release(lock_key:str, worker_id:str):
    success = release_lock(lock_key, worker_id)
    return{
        "lock_key":lock_key,
        "worker_id":worker_id,
        "lock_released":success
    }