from enum import Enum

from pydantic import BaseModel


class Priority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Status(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Ticket:
    def __init__(self, id, title, description, priority):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = Status.OPEN


class CreateTicketRequest(BaseModel):
    title: str
    description: str
    priority: Priority