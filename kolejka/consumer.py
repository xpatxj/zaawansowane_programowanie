import os
import time

from common import file_lock, read_jobs, set_status, write_jobs

POLL_INTERVAL = 5
WORK_TIME = 30
NAME = f"consumer-{os.getpid()}"


def take_job():
    """Pobiera pierwszą pracę pending i od razu zmienia jej status na in_progress."""
    with file_lock():
        jobs = read_jobs()
        for job in jobs:
            if job["status"] == "pending":
                job["status"] = "in_progress"
                write_jobs(jobs)
                return job
    return None


if __name__ == "__main__":
    print(f"{NAME} wystartował")
    while True:
        job = take_job()
        if job is None:
            time.sleep(POLL_INTERVAL)
            continue
        print(f"{NAME}: wykonuję {job['task']}")
        time.sleep(WORK_TIME)
        set_status(job["id"], "done")
        print(f"{NAME}: zakończono {job['task']}")
