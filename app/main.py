from fastapi import FastAPI, HTTPException

from app.models.ticket import Priority
from app.models.ticket import CreateTicketRequest
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService
from app.exceptions import (
    InvalidTicketError,
    TicketConflictError,
    TicketNotFoundError,
)

app = FastAPI()

repository = TicketRepository()
service = TicketService(repository)


@app.get("/")
def root():
    return {"message": "Mini Helpdesk API läuft"}

@app.post("/tickets")
def create_ticket(request: CreateTicketRequest):
    try:
        ticket = service.create_ticket(
            request.title,
            request.description,
            request.priority
        )
    except InvalidTicketError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    return {
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "priority": ticket.priority.value,
        "status": ticket.status.value
    }

@app.get("/tickets")
def get_tickets():
    tickets = service.get_tickets()

    return [
        {
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "priority": ticket.priority.value,
            "status": ticket.status.value
        }
        for ticket in tickets
    ]


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    try:
        ticket = service.get_ticket(ticket_id)
    except TicketNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    return {
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "priority": ticket.priority.value,
        "status": ticket.status.value
    }


@app.post("/tickets/{ticket_id}/close")
def close_ticket(ticket_id: int):
    try:
        ticket = service.close_ticket(ticket_id)
    except TicketNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except TicketConflictError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

    return {
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "priority": ticket.priority.value,
        "status": ticket.status.value
    }


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    try:
        service.delete_ticket(ticket_id)
    except TicketNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except TicketConflictError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

    return {
        "message": "Ticket gelöscht"
    }