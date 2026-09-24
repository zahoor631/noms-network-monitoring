from pydantic import BaseModel
from datetime import datetime
from app.models.ip_address import IPStatus


class IPAddressBase(BaseModel):
    ip: str
    status: IPStatus = IPStatus.available
    assigned_to: str | None = None


class IPAddressCreate(IPAddressBase):
    subnet_id: int


class IPAddressUpdate(BaseModel):
    status: IPStatus | None = None
    assigned_to: str | None = None


class IPAddressOut(IPAddressBase):
    id: int
    subnet_id: int
    created_at: datetime

    class Config:
        from_attributes = True