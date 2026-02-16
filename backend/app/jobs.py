from fastapi import APIRouter, HTTPException, Depends
import os
from redis import Redis
from rq import Queue
import json

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

REDIS_URL = os.getenv('REDIS_URL')
if not REDIS_URL:
    # allow missing in dev — handler will error if used
    redis_conn = None
else:
    redis_conn = Redis.from_url(REDIS_URL)

@router.post('/enqueue')
async def enqueue_job(payload: dict):
    """Enqueue a background job. Example payload: {"task":"generate_contract","data":{...}}"""
    if not redis_conn:
        raise HTTPException(status_code=500, detail="REDIS_URL not configured")
    q = Queue(connection=redis_conn)
    # For demo: push payload to 'default' queue; worker should import a task handler
    job = q.enqueue('backend.app.task_handlers.handle_task', payload)
    return {"job_id": job.get_id(), "status": "queued"}
