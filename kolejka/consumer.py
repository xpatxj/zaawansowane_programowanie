import os
import time

try:
    from kolejka.common import (
        file_lock,
        get_connection,
        init_db,
        read_jobs,
        set_status,
        take_job as common_take_job,
        write_jobs,
    )
except ImportError:
    from common import (
        file_lock,
        get_connection,
        init_db,
        read_jobs,
        set_status,
        take_job as common_take_job,
        write_jobs,
    )

POLL_INTERVAL = 5
WORK_TIME = 30
NAME = f"consumer-{os.getpid()}"


def take_job(db_file=None):
    """Pobiera pierwszą pracę pending i od razu zmienia jej status na in_progress."""
    return common_take_job(db_file=db_file)


if __name__ == "__main__":
    init_db()
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
