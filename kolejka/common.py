import csv
import os
import sqlite3
from contextlib import contextmanager

DB_FILE = os.path.join(os.path.dirname(__file__), "queue.db")
QUEUE_CSV_FILE = os.path.join(os.path.dirname(__file__), "queue.csv")
FIELDS = ["id", "task", "status"]


@contextmanager
def file_lock():
    """Kontekst blokady zachowany dla kompatybilności wstecznej.

    Silnik SQLite realizuje blokowanie transakcyjne automatycznie.
    """
    yield


def get_connection(db_file=None):
    """Tworzy i zwraca połączenie do bazy SQLite z konfiguracją współbieżności."""
    conn = sqlite3.connect(db_file or DB_FILE, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_file=None):
    """Inicjalizuje schemat bazy SQLite."""
    target_db = db_file or DB_FILE
    conn = get_connection(target_db)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def migrate_from_csv(csv_path=None, db_file=None):
    """Importuje zadania z pliku CSV do bazy danych SQLite."""
    csv_file = csv_path or QUEUE_CSV_FILE
    if not os.path.exists(csv_file):
        return

    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        jobs = list(reader)

    if not jobs:
        return

    target_db = db_file or DB_FILE
    init_db(target_db)
    conn = get_connection(target_db)
    try:
        cursor = conn.cursor()
        for job in jobs:
            cursor.execute(
                "INSERT INTO jobs (id, task, status) VALUES (?, ?, ?)",
                (int(job["id"]), job["task"], job["status"])
            )
        conn.commit()
    finally:
        conn.close()


def read_jobs(db_file=None):
    """Zwraca listę wszystkich zadań jako słowniki z kluczami id, task, status."""
    init_db(db_file)
    conn = get_connection(db_file)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, status FROM jobs ORDER BY id ASC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def write_jobs(jobs, db_file=None):
    """Zapisuje listę zadań do bazy SQLite (zastępuje dotychczasową zawartość)."""
    init_db(db_file)
    conn = get_connection(db_file)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs")
        for job in jobs:
            cursor.execute(
                "INSERT INTO jobs (id, task, status) VALUES (?, ?, ?)",
                (job.get("id"), job["task"], job["status"])
            )
        conn.commit()
    finally:
        conn.close()


def add_job(task=None, status="pending", db_file=None):
    """Atomowo dodaje nowe zadanie do bazy SQLite."""
    init_db(db_file)
    conn = get_connection(db_file)
    try:
        cursor = conn.cursor()
        if task is None:
            cursor.execute("INSERT INTO jobs (task, status) VALUES ('', ?)", (status,))
            job_id = cursor.lastrowid
            task_name = f"rozmowa_telefoniczna_{job_id}"
            cursor.execute("UPDATE jobs SET task = ? WHERE id = ?", (task_name, job_id))
        else:
            cursor.execute("INSERT INTO jobs (task, status) VALUES (?, ?)", (task, status))
            job_id = cursor.lastrowid
        conn.commit()
        return job_id
    finally:
        conn.close()


def set_status(job_id, status, db_file=None):
    """Aktualizuje status zadania o wskazanym identyfikatorze."""
    init_db(db_file)
    conn = get_connection(db_file)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
        conn.commit()
    finally:
        conn.close()


def take_job(db_file=None):
    """Atomowo pobiera pierwsze zadanie pending i zmienia status na in_progress."""
    init_db(db_file)
    conn = get_connection(db_file)
    try:
        conn.isolation_level = None
        conn.execute("BEGIN IMMEDIATE")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, task, status FROM jobs WHERE status = 'pending' ORDER BY id ASC LIMIT 1"
        )
        row = cursor.fetchone()
        if row is not None:
            job = dict(row)
            cursor.execute(
                "UPDATE jobs SET status = 'in_progress' WHERE id = ?",
                (job["id"],)
            )
            conn.execute("COMMIT")
            job["status"] = "in_progress"
            return job
        conn.execute("COMMIT")
        return None
    except Exception:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()
