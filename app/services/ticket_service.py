from app.models.ticket import Ticket, Priority, Status
from app.repositories.ticket_repository import TicketRepository


class TicketService:
    def __init__(self, repository):
        self.repository = repository

    def create_ticket(self, title, description, priority):
        if not title:
            raise ValueError("Titel darf nicht leer sein.")

        if not isinstance(priority, Priority):
            raise ValueError("Ungültige Priorität.")

        ticket = Ticket(
            None,
            title,
            description,
            priority
        )

        self.repository.save(ticket)

        return ticket

    def get_ticket(self, ticket_id):
        ticket = self.repository.find_by_id(ticket_id)

        if ticket is None:
            raise ValueError("Ticket nicht gefunden.")

        return ticket

    def close_ticket(self, ticket_id):
        ticket = self.get_ticket(ticket_id)

        if ticket.status == Status.CLOSED:
            raise ValueError("Ticket ist bereits geschlossen.")

        self.repository.update_status(ticket_id, Status.CLOSED)

        return self.get_ticket(ticket_id)

    def delete_ticket(self, ticket_id):
        ticket = self.get_ticket(ticket_id)

        if ticket.status != Status.CLOSED:
            raise ValueError("Nur geschlossene Tickets dürfen gelöscht werden.")

        self.repository.delete(ticket_id)

    def get_tickets(self):
        return self.repository.find_all()