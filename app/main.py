from fastapi import FastAPI, HTTPException

from app.models.ticket import Priority
from app.models.ticket import CreateTicketRequest
from app.repositories.ticket_repository import TicketRepository
from app.services.ticket_service import TicketService


app = FastAPI()

repository = TicketRepository()
service = TicketService(repository)


@app.get("/")
def root():
    return {"message": "Mini Helpdesk API läuft"}

@app.post("/tickets")
def create_ticket(request: CreateTicketRequest):
    ticket = service.create_ticket(
        request.title,
        request.description,
        request.priority
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
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Ticket nicht gefunden."
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
    except ValueError as error:
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

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    try:
        service.delete_ticket(ticket_id)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "message": "Ticket gelöscht"
    }
