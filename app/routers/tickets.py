from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Ticket
from app.schemas.ticket import (
    TicketCreate,
    TicketCreatedResponse,
    TicketDeletedResponse,
    TicketResponse,
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


def _get_ticket_or_404(ticket_id: int, db: Session) -> Ticket:
    ticket = db.scalar(select(Ticket).where(Ticket.id == ticket_id))

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.post("/", status_code=201, response_model=TicketCreatedResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = Ticket(
        title=ticket.title, description=ticket.description, priority=ticket.priority
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {"message": "Ticket created successfully", "data": new_ticket}


@router.get("/", response_model=list[TicketResponse])
def list_tickets(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    priority: Literal["low", "medium", "high"] | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = select(Ticket)

    if priority is not None:
        query = query.where(Ticket.priority == priority)

    tickets = db.scalars(query.order_by(Ticket.id).offset(skip).limit(limit)).all()

    return tickets


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.scalar(select(Ticket).where(Ticket.id == ticket_id))

    ticket = _get_ticket_or_404(ticket_id, db)

    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int, ticket_data: TicketCreate, db: Session = Depends(get_db)
):
    ticket = db.scalar(select(Ticket).where(Ticket.id == ticket_id))

    ticket = _get_ticket_or_404(ticket_id, db)

    ticket.title = ticket_data.title
    ticket.description = ticket_data.description
    ticket.priority = ticket_data.priority

    db.commit()
    db.refresh(ticket)

    return ticket


@router.delete("/{ticket_id}", response_model=TicketDeletedResponse)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.scalar(select(Ticket).where(Ticket.id == ticket_id))

    ticket = _get_ticket_or_404(ticket_id, db)

    db.delete(ticket)
    db.commit()

    return {"message": "Ticket deleted successfully", "id": ticket_id}
