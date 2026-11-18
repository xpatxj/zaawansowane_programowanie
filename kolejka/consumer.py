import os
import time

try:
    from kolejka.common import (
        file_lock,
        read_jobs,
        set_status,
        take_job as common_take_job,
        write_jobs,
    )
except ImportError:
    from common import (
        file_lock,
        read_jobs,
        set_status,
        take_job as common_take_job,
        write_jobs,
    )

POLL_INTERVAL = 5
WORK_TIME = 30
NAME = f"consumer-{os.getpid()}"


def take_job(queue_name=None):
    """Pobiera pierwszą pracę pending i od razu zmienia jej status na in_progress."""
    return common_take_job(queue_name=queue_name)


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
