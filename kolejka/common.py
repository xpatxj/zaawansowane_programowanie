import json
import os
import threading
import time
import warnings
from contextlib import contextmanager

import pika

warnings.filterwarnings("ignore", category=DeprecationWarning)

QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "rozmowy_telefoniczne")
COUNTER_FILE = os.path.join(os.path.dirname(__file__), ".counter")
FIELDS = ["id", "task", "status"]

_LOCAL = threading.local()
_COUNTER_LOCK = threading.Lock()


@contextmanager
def file_lock():
    """Kontekst blokady zachowany dla kompatybilności wstecznej.

    RabbitMQ realizuje kolejkowanie i współbieżne rozpraszanie zadań automatycznie.
    """
    yield


def get_next_id():
    """Zwraca kolejny unikalny identyfikator zadania."""
    with _COUNTER_LOCK:
        counter = 1
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        counter = int(content) + 1
            except Exception:
                counter = 1
        with open(COUNTER_FILE, "w", encoding="utf-8") as f:
            f.write(str(counter))
        return counter


def reset_counter(val=0):
    """Resetuje licznik zadań."""
    with _COUNTER_LOCK:
        with open(COUNTER_FILE, "w", encoding="utf-8") as f:
            f.write(str(val))


def get_connection(host=None, port=None, user=None, password=None):
    """Tworzy połączenie do RabbitMQ."""
    h = host or os.getenv("RABBITMQ_HOST", "localhost")
    u = user or os.getenv("RABBITMQ_USER", "guest")
    pwd = password or os.getenv("RABBITMQ_PASSWORD", "guest")

    env_port = os.getenv("RABBITMQ_PORT")
    if port is not None:
        ports_to_try = [int(port)]
    elif env_port:
        ports_to_try = [int(env_port)]
    else:
        ports_to_try = [8081, 5672]

    credentials = pika.PlainCredentials(u, pwd)
    last_err = None
    for p in ports_to_try:
        try:
            params = pika.ConnectionParameters(
                host=h,
                port=p,
                credentials=credentials,
                connection_attempts=3,
                retry_delay=1,
                heartbeat=600,
            )
            return pika.BlockingConnection(params)
        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(
        f"Nie udało się połączyć z RabbitMQ ({h}:{ports_to_try}). "
        f"Upewnij się, że kontener działa (np. 'docker compose up -d'). Błąd: {last_err}"
    )


def _get_active_jobs():
    if not hasattr(_LOCAL, "active_jobs"):
        _LOCAL.active_jobs = {}
    return _LOCAL.active_jobs


def get_channel(queue_name=None):
    """Zwraca aktywny kanał RabbitMQ i deklaruje trwałą kolejkę."""
    q_name = queue_name or QUEUE_NAME
    conn = getattr(_LOCAL, "connection", None)
    chan = getattr(_LOCAL, "channel", None)

    if conn is None or conn.is_closed:
        conn = get_connection()
        chan = conn.channel()
        chan.queue_declare(queue=q_name, durable=True)
        chan.basic_qos(prefetch_count=1)
        _LOCAL.connection = conn
        _LOCAL.channel = chan
    elif chan is None or chan.is_closed:
        chan = conn.channel()
        chan.queue_declare(queue=q_name, durable=True)
        chan.basic_qos(prefetch_count=1)
        _LOCAL.channel = chan

    return chan


def close_connection():
    """Zamyka połączenie wątku do RabbitMQ."""
    conn = getattr(_LOCAL, "connection", None)
    chan = getattr(_LOCAL, "channel", None)
    if chan is not None and not chan.is_closed:
        try:
            chan.close()
        except Exception:
            pass
    if conn is not None and not conn.is_closed:
        try:
            conn.close()
        except Exception:
            pass
    _LOCAL.connection = None
    _LOCAL.channel = None
    _LOCAL.active_jobs = {}


def add_job(task=None, job_id=None, queue_name=None):
    """Dodaje nowe zadanie do kolejki RabbitMQ ze statusem pending."""
    channel = get_channel(queue_name)
    q_name = queue_name or QUEUE_NAME

    if job_id is None:
        job_id = get_next_id()
    if task is None:
        task = f"rozmowa_telefoniczna_{job_id}"

    payload = json.dumps({
        "id": job_id,
        "task": task,
        "status": "pending",
    })

    channel.basic_publish(
        exchange="",
        routing_key=q_name,
        body=payload.encode("utf-8"),
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
            content_type="application/json",
        ),
    )
    return job_id


def take_job(queue_name=None):
    """Pobiera zadanie z kolejki RabbitMQ i oznacza je jako in_progress (Unacked)."""
    channel = get_channel(queue_name)
    q_name = queue_name or QUEUE_NAME

    method_frame, header_frame, body = channel.basic_get(queue=q_name, auto_ack=False)
    if method_frame is None:
        return None

    try:
        data = json.loads(body.decode("utf-8"))
    except Exception:
        data = {
            "id": str(method_frame.delivery_tag),
            "task": body.decode("utf-8", errors="replace"),
            "status": "pending",
        }

    job_id = str(data.get("id", method_frame.delivery_tag))
    job = {
        "id": job_id,
        "task": data.get("task", f"rozmowa_telefoniczna_{job_id}"),
        "status": "in_progress",
    }
    _get_active_jobs()[job_id] = (channel, method_frame.delivery_tag, job)
    return job


def set_status(job_id, status):
    """Aktualizuje status zadania (status 'done' zatwierdza wiadomość przez basic_ack)."""
    key = str(job_id)
    active_jobs = _get_active_jobs()
    if key in active_jobs:
        channel, delivery_tag, job = active_jobs.pop(key)
        if status == "done":
            channel.basic_ack(delivery_tag=delivery_tag)
            job["status"] = "done"
        elif status in ("pending", "nack"):
            channel.basic_nack(delivery_tag=delivery_tag, requeue=True)
            job["status"] = "pending"
        else:
            channel.basic_ack(delivery_tag=delivery_tag)
            job["status"] = status


def read_jobs(queue_name=None):
    """Zwraca listę aktywnych zadań w toku."""
    channel = get_channel(queue_name)
    q_name = queue_name or QUEUE_NAME
    channel.queue_declare(queue=q_name, durable=True)
    return [job for _, _, job in _get_active_jobs().values()]


def write_jobs(jobs, queue_name=None):
    """Dodaje listę zadań do kolejki RabbitMQ."""
    for job in jobs:
        add_job(
            task=job.get("task"),
            job_id=job.get("id"),
            queue_name=queue_name,
        )
