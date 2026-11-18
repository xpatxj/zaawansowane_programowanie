import os
import sqlite3
import threading
import pytest
from kolejka.common import (
    add_job,
    file_lock,
    get_connection,
    init_db,
    migrate_from_csv,
    read_jobs,
    set_status,
    take_job,
    write_jobs,
)
from kolejka.consumer import take_job as consumer_take_job
from kolejka.producer import produce


@pytest.fixture
def tmp_db(tmp_path):
    db_file = str(tmp_path / "test_queue.db")
    init_db(db_file)
    return db_file


def test_init_db(tmp_db):
    conn = get_connection(tmp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
    assert cursor.fetchone() is not None
    conn.close()


def test_add_job_auto_task(tmp_db):
    id1 = add_job(db_file=tmp_db)
    id2 = add_job(db_file=tmp_db)
    assert id1 == 1
    assert id2 == 2
    jobs = read_jobs(db_file=tmp_db)
    assert len(jobs) == 2
    assert jobs[0] == {"id": 1, "task": "rozmowa_telefoniczna_1", "status": "pending"}
    assert jobs[1] == {"id": 2, "task": "rozmowa_telefoniczna_2", "status": "pending"}


def test_add_job_custom_task(tmp_db):
    job_id = add_job(task="custom_task", status="custom_status", db_file=tmp_db)
    jobs = read_jobs(db_file=tmp_db)
    assert len(jobs) == 1
    assert jobs[0] == {"id": job_id, "task": "custom_task", "status": "custom_status"}


def test_take_job(tmp_db):
    assert take_job(db_file=tmp_db) is None
    add_job(db_file=tmp_db)
    add_job(db_file=tmp_db)
    job1 = take_job(db_file=tmp_db)
    assert job1["id"] == 1
    assert job1["status"] == "in_progress"

    jobs = read_jobs(db_file=tmp_db)
    assert jobs[0]["status"] == "in_progress"
    assert jobs[1]["status"] == "pending"

    job2 = take_job(db_file=tmp_db)
    assert job2["id"] == 2
    assert job2["status"] == "in_progress"

    assert take_job(db_file=tmp_db) is None


def test_set_status(tmp_db):
    job_id = add_job(db_file=tmp_db)
    set_status(job_id, "in_progress", db_file=tmp_db)
    jobs = read_jobs(db_file=tmp_db)
    assert jobs[0]["status"] == "in_progress"

    set_status(job_id, "done", db_file=tmp_db)
    jobs = read_jobs(db_file=tmp_db)
    assert jobs[0]["status"] == "done"


def test_write_jobs(tmp_db):
    sample_jobs = [
        {"id": 10, "task": "task_10", "status": "done"},
        {"id": 11, "task": "task_11", "status": "pending"},
    ]
    write_jobs(sample_jobs, db_file=tmp_db)
    jobs = read_jobs(db_file=tmp_db)
    assert len(jobs) == 2
    assert jobs[0]["id"] == 10
    assert jobs[1]["status"] == "pending"


def test_file_lock_context():
    with file_lock():
        pass


def test_consumer_take_job(tmp_db):
    add_job(db_file=tmp_db)
    job = consumer_take_job(db_file=tmp_db)
    assert job is not None
    assert job["id"] == 1
    assert job["status"] == "in_progress"


def test_producer_produce(tmp_db):
    job_id = produce(db_file=tmp_db)
    assert job_id == 1
    jobs = read_jobs(db_file=tmp_db)
    assert len(jobs) == 1
    assert jobs[0]["task"] == "rozmowa_telefoniczna_1"


def test_concurrent_take_jobs(tmp_db):
    num_jobs = 30
    for _ in range(num_jobs):
        add_job(db_file=tmp_db)

    results = []
    errors = []

    def worker():
        try:
            while True:
                job = take_job(db_file=tmp_db)
                if job is None:
                    break
                results.append(job["id"])
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert len(results) == num_jobs
    assert len(set(results)) == num_jobs


def test_migrate_from_csv(tmp_path):
    csv_file = tmp_path / "test_queue.csv"
    csv_file.write_text("id,task,status\n1,task_1,done\n2,task_2,pending\n", encoding="utf-8")
    db_file = str(tmp_path / "migrated.db")

    init_db(db_file)
    migrate_from_csv(str(csv_file), db_file)

    jobs = read_jobs(db_file)
    assert len(jobs) == 2
    assert jobs[0] == {"id": 1, "task": "task_1", "status": "done"}
    assert jobs[1] == {"id": 2, "task": "task_2", "status": "pending"}
