from pydantic import BaseModel, Field
from datetime import datetime


class SubnetBase(BaseModel):
    network: str = Field(..., description="e.g. 192.168.1.0")
    cidr: int = Field(..., ge=0, le=32)
    gateway: str | None = None
    vlan: int | None = None
    description: str | None = None


class SubnetCreate(SubnetBase):
    pass


class SubnetUpdate(BaseModel):
    network: str | None = None
    cidr: int | None = None
    gateway: str | None = None
    vlan: int | None = None
    description: str | None = None


class SubnetOut(SubnetBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SubnetCalcRequest(BaseModel):
    ip: str
    cidr: int


class SubnetCalcResponse(BaseModel):
    network: str
    broadcast: str
    netmask: str
    first_host: str
    last_host: str
    total_hosts: int
    usable_hosts: int