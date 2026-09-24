from pydantic import BaseModel, Field
from datetime import datetime
from app.models.device import DeviceType, DeviceStatus


class DeviceBase(BaseModel):
    hostname: str = Field(..., min_length=1, max_length=100)
    device_type: DeviceType
    ip_address: str
    mac_address: str | None = None
    location: str | None = None
    description: str | None = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    hostname: str | None = None
    device_type: DeviceType | None = None
    ip_address: str | None = None
    mac_address: str | None = None
    location: str | None = None
    description: str | None = None


class DeviceOut(DeviceBase):
    id: int
    status: DeviceStatus
    last_seen: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


class DeviceStats(BaseModel):
    total: int
    online: int
    offline: int
    unknown: int