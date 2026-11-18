import os
import threading
import uuid
import pytest
from kolejka.common import (
    add_job,
    close_connection,
    file_lock,
    get_channel,
    get_connection,
    read_jobs,
    reset_counter,
    set_status,
    take_job,
    write_jobs,
)
from kolejka.consumer import take_job as consumer_take_job
from kolejka.producer import produce


def is_rabbitmq_available():
    try:
        conn = get_connection()
        conn.close()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not is_rabbitmq_available(),
    reason="RabbitMQ nie jest dostępny (uruchom 'docker compose up -d')"
)


@pytest.fixture
def test_queue():
    queue_name = f"test_queue_{uuid.uuid4().hex[:8]}"
    channel = get_channel(queue_name)
    channel.queue_purge(queue=queue_name)
    reset_counter(0)
    yield queue_name
    try:
        channel.queue_delete(queue=queue_name)
    except Exception:
        pass
    close_connection()


def test_connection():
    conn = get_connection()
    assert conn.is_open
    conn.close()


def test_add_job_auto_id(test_queue):
    id1 = add_job(queue_name=test_queue)
    id2 = add_job(queue_name=test_queue)
    assert id1 == 1
    assert id2 == 2

    job1 = take_job(queue_name=test_queue)
    assert job1 is not None
    assert job1["id"] == "1"
    assert job1["task"] == "rozmowa_telefoniczna_1"
    assert job1["status"] == "in_progress"
    set_status(job1["id"], "done")

    job2 = take_job(queue_name=test_queue)
    assert job2 is not None
    assert job2["id"] == "2"
    assert job2["task"] == "rozmowa_telefoniczna_2"
    set_status(job2["id"], "done")


def test_add_job_custom(test_queue):
    job_id = add_job(task="pilna_rozmowa", job_id=99, queue_name=test_queue)
    assert job_id == 99

    job = take_job(queue_name=test_queue)
    assert job["id"] == "99"
    assert job["task"] == "pilna_rozmowa"
    set_status(job["id"], "done")


def test_take_job_empty(test_queue):
    assert take_job(queue_name=test_queue) is None


def test_set_status_nack_requeues(test_queue):
    add_job(task="zadanie_do_powtorzenia", queue_name=test_queue)
    job = take_job(queue_name=test_queue)
    assert job is not None
    assert job["task"] == "zadanie_do_powtorzenia"

    set_status(job["id"], "nack")

    requeued_job = take_job(queue_name=test_queue)
    assert requeued_job is not None
    assert requeued_job["task"] == "zadanie_do_powtorzenia"
    set_status(requeued_job["id"], "done")


def test_file_lock_compat():
    with file_lock():
        pass


def test_write_jobs(test_queue):
    jobs_to_write = [
        {"id": 10, "task": "rozmowa_10", "status": "pending"},
        {"id": 11, "task": "rozmowa_11", "status": "pending"},
    ]
    write_jobs(jobs_to_write, queue_name=test_queue)

    j1 = take_job(queue_name=test_queue)
    j2 = take_job(queue_name=test_queue)
    assert j1["id"] == "10"
    assert j2["id"] == "11"
    set_status(j1["id"], "done")
    set_status(j2["id"], "done")


def test_producer_and_consumer(test_queue, monkeypatch):
    monkeypatch.setattr("kolejka.common.QUEUE_NAME", test_queue)
    job_id = produce()
    assert job_id == 1

    job = consumer_take_job(queue_name=test_queue)
    assert job is not None
    assert job["id"] == "1"
    assert job["task"] == "rozmowa_telefoniczna_1"
    set_status(job["id"], "done")


def test_concurrent_consumers(test_queue):
    num_jobs = 20
    for i in range(num_jobs):
        add_job(task=f"watek_rozmowa_{i}", job_id=i + 1, queue_name=test_queue)

    results = []
    errors = []

    def worker():
        try:
            while True:
                job = take_job(queue_name=test_queue)
                if job is None:
                    break
                results.append(job["id"])
                set_status(job["id"], "done")
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
