import time
def handle_task(payload):
    """Example task handler. Replace with actual AI orchestration.
    This runs inside the worker process.
    """
    # Simulate long-running task
    time.sleep(2)
    task = payload.get('task')
    data = payload.get('data')
    print(f"Handled task={task} data_keys={list(data.keys()) if isinstance(data, dict) else None}")
    return {"status": "ok", "task": task}
