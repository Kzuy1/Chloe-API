import gc
import os
import threading
import time
import uuid
from concurrent.futures import ProcessPoolExecutor

from utils.file_utils import clear_temp

MAX_WORKERS = int(os.environ.get("VERIFY_MAX_WORKERS", "1"))
MAX_PENDING_JOBS = 50
RESULT_TTL_SECONDS = 60 * 60

_executor = None
_jobs = {}
_lock = threading.Lock()


class QueueFullError(Exception):
    pass


def _run_verification(full_path, data_issue, verification_type):
    # Roda em outro processo, para o parse do ezdxf não prender o GIL do servidor
    if verification_type == 'redecam':
        from Verify_Drawing_Redecam.Drawing import Drawing
    else:
        from Verify_Drawing.Drawing import Drawing
    try:
        drawing = Drawing(full_path, data_issue)
        message = drawing.message
        del drawing
        return message
    finally:
        gc.collect()


def _get_executor():
    global _executor
    if _executor is None:
        _executor = ProcessPoolExecutor(max_workers=MAX_WORKERS)
    return _executor


def _purge_expired():
    now = time.time()
    for job_id in [j for j, v in _jobs.items() if v["finished_at"] and now - v["finished_at"] > RESULT_TTL_SECONDS]:
        del _jobs[job_id]


def _on_done(job_id, temp_dir, future):
    with _lock:
        job = _jobs.get(job_id)
        if job is None:
            return
        job["finished_at"] = time.time()
        job["future"] = None
        try:
            job["message"] = future.result()
            job["status"] = "done"
        except Exception as e:
            job["message"] = str(e)
            job["status"] = "error"

    try:
        clear_temp(temp_dir)
    except OSError as e:
        print(f"Falha ao limpar {temp_dir}: {e}")


def submit_job(full_path, temp_dir, data_issue, verification_type):
    with _lock:
        _purge_expired()
        pending = sum(1 for v in _jobs.values() if v["finished_at"] is None)
        if pending >= MAX_PENDING_JOBS:
            raise QueueFullError()

        job_id = str(uuid.uuid4())
        future = _get_executor().submit(_run_verification, full_path, data_issue, verification_type)
        _jobs[job_id] = {"future": future, "status": "pending", "message": None, "finished_at": None}

    future.add_done_callback(lambda f: _on_done(job_id, temp_dir, f))
    return job_id


def get_job(job_id):
    with _lock:
        _purge_expired()
        job = _jobs.get(job_id)
        if job is None:
            return None
        status = job["status"]
        if status == "pending" and job["future"] is not None and job["future"].running():
            status = "running"
        return {"status": status, "message": job["message"]}
