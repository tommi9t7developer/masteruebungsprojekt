
import os

import psycopg
import pytest
from dotenv import load_dotenv

from app.models.ticket import Ticket, Priority, Status
from app.repositories.ticket_repository import TicketRepository


load_dotenv()


@pytest.fixture
def repository():
    """Bereitet die Testdatenbank vor und leert die Tickets-Tabelle."""

    connection_settings = {
        "host": os.environ["TEST_DB_HOST"],
        "port": os.environ["TEST_DB_PORT"],
        "dbname": os.environ["TEST_DB_NAME"],
        "user": os.environ["TEST_DB_USER"],
        "password": os.environ["TEST_DB_PASSWORD"],
    }

    # Stellt sicher, dass das Repository die Testdatenbank verwendet.
    def test_connection_factory():
        return psycopg.connect(**connection_settings)

    # Erstellt die Tabelle, falls sie noch nicht existiert,
    # und setzt die Testdatenbank für diesen Test zurück.
    with test_connection_factory() as connection:
        print("Verwendete Testdatenbank:", connection.info.dbname)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                priority TEXT NOT NULL
                    CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH')),
                status TEXT NOT NULL DEFAULT 'OPEN'
                    CHECK (status IN ('OPEN', 'CLOSED'))
            )
        """)

        connection.execute(
            "TRUNCATE TABLE tickets RESTART IDENTITY"
        )

    # Gibt ein Repository zurück, das dieselbe Testdatenbank nutzt.
    return TicketRepository(
        connection_factory=test_connection_factory
    )


def test_save_and_find_ticket(repository):
    ticket = Ticket(
        None,
        "Testticket",
        "Testbeschreibung",
        Priority.HIGH,
    )

    repository.save(ticket)

    found_ticket = repository.find_by_id(ticket.id)

    assert found_ticket is not None
    assert found_ticket.id == ticket.id
    assert found_ticket.title == "Testticket"
    assert found_ticket.priority == Priority.HIGH
    assert found_ticket.status == Status.OPEN


def test_find_all(repository):
    first = Ticket(
        None,
        "Ticket 1",
        "Beschreibung 1",
        Priority.LOW,
    )
    second = Ticket(
        None,
        "Ticket 2",
        "Beschreibung 2",
        Priority.HIGH,
    )

    repository.save(first)
    repository.save(second)

    tickets = repository.find_all()

    assert len(tickets) == 2
    assert [ticket.title for ticket in tickets] == [
        "Ticket 1",
        "Ticket 2",
    ]


def test_update_status(repository):
    ticket = Ticket(
        None,
        "Testticket",
        "Testbeschreibung",
        Priority.MEDIUM,
    )

    repository.save(ticket)
    repository.update_status(ticket.id, Status.CLOSED)

    found_ticket = repository.find_by_id(ticket.id)

    assert found_ticket is not None
    assert found_ticket.status == Status.CLOSED


def test_delete_ticket(repository):
    ticket = Ticket(
        None,
        "Testticket",
        "Testbeschreibung",
        Priority.LOW,
    )

    repository.save(ticket)

    deleted = repository.delete(ticket.id)

    assert deleted is True
    assert repository.find_by_id(ticket.id) is None

