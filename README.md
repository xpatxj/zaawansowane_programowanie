# zaawansowane_programowanie
Repo na przedmiot Zaawansowane Programowanie

## Kolejkowanie rozmów telefonicznych (SQLite)

Logika kolejkowania zadań oparta na wbudowanej w standardową bibliotekę Pythona bazie SQLite (`sqlite3`).

### Struktura bazy danych (`kolejka/queue.db` / `kolejka/schema.sql`)
```sql
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT NOT NULL
);
```

### Narzędzia do zarządzania i podglądu bazy danych
- **DBeaver** (dla pracujących na komputerach uczelnianych):
  - *Nowe połączenie (New Database Connection)* -> Wybierz *SQLite* -> Wskaż ścieżkę do pliku `kolejka/queue.db`.
- **PyCharm Professional** (dla pracujących na swoich komputerach):
  - Zakładka *Database* (po prawej stronie) -> `+` (*Data Source*) -> *SQLite* -> Wskaż plik `kolejka/queue.db`.

### Instrukcja uruchomienia
- **Producent (producer)**:
  ```bash
  python kolejka/producer.py        # dodaje 1 zadanie ze statusem pending
  python kolejka/producer.py 100     # dodaje 100 zadań
  ```
- **Konsument (consumer)**:
  ```bash
  python kolejka/consumer.py        # pobiera zadania pending, zmienia status na in_progress i po zakończeniu na done
  ```
- **Testy jednostkowe**:
  ```bash
  pytest
  ```
- **Weryfikacja stylu (pycodestyle / CI)**:
  ```bash
  pycodestyle .
  ```
