"""Każde uruchomienie dodaje 1 pracę (status pending). Opcjonalnie: python producer.py 100"""
import sys

from common import file_lock, read_jobs, write_jobs


def produce():
    with file_lock():
        jobs = read_jobs()
        job_id = str(len(jobs) + 1)
        jobs.append({"id": job_id, "task": f"rozmowa_telefoniczna_{job_id}", "status": "pending"})
        write_jobs(jobs)
    print(f"Dodano pracę {job_id}")


if __name__ == "__main__":
    for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 1):
        produce()
