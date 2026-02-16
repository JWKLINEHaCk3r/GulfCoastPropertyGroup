"""Lightweight RQ worker bootstrap for background AI tasks
Run with: `python backend/worker.py` after setting REDIS_URL env var.
"""
import os
from rq import Worker, Queue, Connection
from redis import Redis

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
conn = Redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        q = Queue()
        worker = Worker([q])
        print('Starting RQ worker, listening for jobs...')
        worker.work()
