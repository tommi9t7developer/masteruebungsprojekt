
import pytest

from app.exceptions import (
    InvalidTicketError,
    TicketConflictError,
    TicketNotFoundError,
)
from app.models.ticket import Priority, Status
from app.services.ticket_service import TicketService


class FakeTicketRepository:
    """Ein kleines Repository nur für unsere Tests."""

    def __init__(self):
        self.tickets = {}
        self.next_id = 1

    def save(self, ticket):
        ticket.id = self.next_id
        self.tickets[self.next_id] = ticket
        self.next_id += 1

    def find_by_id(self, ticket_id):
        return self.tickets.get(ticket_id)

    def find_all(self):
        return list(self.tickets.values())

    def update_status(self, ticket_id, status):
        self.tickets[ticket_id].status = status

    def delete(self, ticket_id):
        return self.tickets.pop(ticket_id, None) is not None


@pytest.fixture
def service():
    repository = FakeTicketRepository()
    return TicketService(repository)


def test_create_ticket(service):
    ticket = service.create_ticket(
        "Drucker funktioniert nicht",
        "Der Drucker reagiert nicht.",
        Priority.HIGH,
    )

    assert ticket.id == 1
    assert ticket.title == "Drucker funktioniert nicht"
    assert ticket.priority == Priority.HIGH
    assert ticket.status == Status.OPEN


def test_empty_title_is_rejected(service):
    with pytest.raises(InvalidTicketError):
        service.create_ticket(
            "   ",
            "Eine Beschreibung",
            Priority.LOW,
        )


def test_missing_ticket_is_rejected(service):
    with pytest.raises(TicketNotFoundError):
        service.get_ticket(999)


def test_open_ticket_cannot_be_deleted(service):
    ticket = service.create_ticket(
        "Neues Problem",
        "Das Problem besteht noch.",
        Priority.MEDIUM,
    )

    with pytest.raises(TicketConflictError):
        service.delete_ticket(ticket.id)


def test_closed_ticket_can_be_deleted(service):
    ticket = service.create_ticket(
        "Gelöstes Problem",
        "Das Problem wurde behoben.",
        Priority.LOW,
    )

    service.close_ticket(ticket.id)
    service.delete_ticket(ticket.id)

    assert service.repository.find_by_id(ticket.id) is None


def test_ticket_cannot_be_closed_twice(service):
    ticket = service.create_ticket(
        "Testticket",
        "Beschreibung",
        Priority.LOW,
    )

    service.close_ticket(ticket.id)

    with pytest.raises(TicketConflictError):
        service.close_ticket(ticket.id)