import pytest

from app.models.ticket import Priority, Status
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService


def test_create_ticket():
    repository = TicketRepository()
    service = TicketService(repository)

    ticket = service.create_ticket(
        "Drucker kaputt",
        "Der Drucker funktioniert nicht.",
        Priority.HIGH
    )

    assert ticket.id == 1
    assert ticket.title == "Drucker kaputt"
    assert ticket.priority == Priority.HIGH
    assert ticket.status == Status.OPEN


def test_create_ticket_without_title_fails():
    repository = TicketRepository()
    service = TicketService(repository)

    with pytest.raises(ValueError):
        service.create_ticket(
            "",
            "Beschreibung",
            Priority.HIGH
        )