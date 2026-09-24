from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


def create_ticket(db: Session, payload: TicketCreate, created_by: int | None) -> Ticket:
    ticket = Ticket(**payload.model_dump(), created_by=created_by)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def update_ticket(db: Session, ticket_id: int, payload: TicketUpdate) -> Ticket:
    ticket = db.query(Ticket).get(ticket_id)
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(ticket, k, v)
    db.commit()
    db.refresh(ticket)
    return ticket