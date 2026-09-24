from pydantic import BaseModel
from datetime import datetime
from app.models.ticket import TicketPriority, TicketStatus


class TicketBase(BaseModel):
    title: str
    description: str | None = None
    priority: TicketPriority = TicketPriority.medium
    device_id: int | None = None
    assigned_to: int | None = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: TicketPriority | None = None
    status: TicketStatus | None = None
    assigned_to: int | None = None


class TicketOut(TicketBase):
    id: int
    status: TicketStatus
    created_by: int | None
    created_at: datetime
    updated_at: datetime | None
    resolved_at: datetime | None

    class Config:
        from_attributes = True