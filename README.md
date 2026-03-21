# Distributed Lock System

A distributed locking mechanism designed to ensure safe concurrency control across multiple workers in a distributed system.

## 🚀 Overview

In distributed systems, multiple workers may attempt to process the same job simultaneously, leading to **race conditions, duplicate processing, and data inconsistencies**.

This project implements a **distributed lock** to ensure that only one worker can process a resource at a time.

## 🧠 Why This Project?

This system addresses:
- Duplicate job execution
- Race conditions
- Inconsistent system state
- Coordination between distributed workers

## 🏗️ How It Works

- A worker attempts to acquire a lock before processing a job
- The lock is stored in a centralized store (Redis)
- If acquired → worker proceeds
- If not → worker retries or skips
- Locks have TTL to prevent deadlocks

## ⚙️ Features

- Distributed lock acquisition
- TTL-based expiration (prevents deadlocks)
- Heartbeat mechanism for lock renewal
- Fail-safe lock release
- Retry strategy for contention handling

## 🔧 Tech Stack

- FastAPI
- Redis
- Python (asyncio)

## 📌 Example Flow

1. Worker A tries to process Job X
2. Worker A acquires lock
3. Worker B attempts same job → fails to acquire lock
4. Worker A completes job and releases lock
5. Worker B can now process next job

## ⚠️ Challenges Addressed

- What happens if a worker crashes?
- How to prevent stale locks?
- How to ensure fairness?

## 🧪 Future Improvements

- Redlock algorithm implementation
- Lock priority queue
- Observability (metrics/logging)
- Multi-region lock coordination

## 📖 Key Concepts Demonstrated

- Distributed systems coordination
- Concurrency control
- Fault tolerance
- Locking strategies (TTL, heartbeat)
