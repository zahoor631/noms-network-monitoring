from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.ticket import Ticket, TicketStatus
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketOut, TicketUpdate
from app.core.dependencies import get_current_user, admin_or_engineer
from app.services import ticket_service

router = APIRouter()


@router.get("/", response_model=List[TicketOut])
def list_tickets(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
    status: Optional[TicketStatus] = None,
):
    q = db.query(Ticket)
    if status:
        q = q.filter(Ticket.status == status)
    return q.order_by(Ticket.created_at.desc()).all()


@router.post("/", response_model=TicketOut, dependencies=[Depends(admin_or_engineer)])
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ticket_service.create_ticket(db, payload, created_by=current_user.id)


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    ticket = db.query(Ticket).get(ticket_id)
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    return ticket


@router.patch("/{ticket_id}", response_model=TicketOut, dependencies=[Depends(admin_or_engineer)])
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    return ticket_service.update_ticket(db, ticket_id, payload)