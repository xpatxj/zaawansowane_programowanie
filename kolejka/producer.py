"""Każde uruchomienie dodaje 1 pracę (status pending). Opcjonalnie: python producer.py 100"""
import sys

try:
    from kolejka.common import add_job, file_lock, read_jobs, write_jobs
except ImportError:
    from common import add_job, file_lock, read_jobs, write_jobs


def produce():
    job_id = add_job()
    print(f"Dodano pracę {job_id}")
    return job_id


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for _ in range(count):
        produce()
