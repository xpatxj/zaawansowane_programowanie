import csv
import os
import time
from contextlib import contextmanager

QUEUE_FILE = os.path.join(os.path.dirname(__file__), "queue.csv")
LOCK_FILE = QUEUE_FILE + ".lock"
FIELDS = ["id", "task", "status"]


@contextmanager
def file_lock():
    """Prosty lock międzyprocesowy: atomowe utworzenie pliku .lock."""
    while True:
        try:
            fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL)
            break
        except FileExistsError:
            time.sleep(0.05)
    try:
        yield
    finally:
        os.close(fd)
        os.remove(LOCK_FILE)


def read_jobs():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_jobs(jobs):
    with open(QUEUE_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(jobs)


def set_status(job_id, status):
    with file_lock():
        jobs = read_jobs()
        for job in jobs:
            if job["id"] == job_id:
                job["status"] = status
        write_jobs(jobs)
