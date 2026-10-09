class TicketNotFoundError(Exception):
    """Wird ausgelöst, wenn ein Ticket nicht existiert."""

class TicketConflictError(Exception):
    """Wird ausgelöst, wenn eine Aktion nicht zum Ticket-Zustand passt."""

class InvalidTicketError(Exception):
    """Wird ausgelöst, wenn Ticket-Daten ungültig sind."""
