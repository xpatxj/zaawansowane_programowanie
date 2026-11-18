# zaawansowane_programowanie
Repo na przedmiot Zaawansowane Programowanie

## Kolejkowanie rozmów telefonicznych (RabbitMQ)

Logika kolejkowania zadań oparta na brokerze wiadomości **RabbitMQ** przy użyciu biblioteki `pika`.

### Uruchomienie brokera RabbitMQ

Broker jest uruchamiany w kontenerze Docker za pomocą Docker Compose:

```bash
docker compose up -d
```

Lub za pomocą pojedynczego polecenia Dockera:

```bash
docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 -p 8081:5672 rabbitmq:3-management
```

Po poprawnym uruchomieniu:
- **Management Dashboard**: [http://localhost:8080](http://localhost:8080)
  - Login: `guest`
  - Hasło: `guest`
- **Port AMQP**: `8081` (lub domyślny `5672`)

### Instrukcja uruchomienia

- **Producent (producer)**:
  Dodaje zadania ze statusem `pending` do kolejki RabbitMQ:
  ```bash
  python kolejka/producer.py        # dodaje 1 zadanie
  python kolejka/producer.py 100     # dodaje 100 zadań
  ```

- **Konsument (consumer)**:
  Pobiera zadania z kolejki, oznacza jako `in_progress` (w RabbitMQ: stan `Unacked`), symuluje pracę (`WORK_TIME`) i potwierdza zakończenie (`basic_ack` -> `done`):
  ```bash
  python kolejka/consumer.py
  ```

- **Testy jednostkowe**:
  ```bash
  pytest
  ```

- **Weryfikacja stylu (PEP 8)**:
  ```bash
  pycodestyle .
  ```
