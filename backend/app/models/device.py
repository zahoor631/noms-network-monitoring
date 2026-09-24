from sqlalchemy import Column, Integer, String, Enum, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base
import enum


class DeviceType(str, enum.Enum):
    router = "router"
    switch = "switch"
    server = "server"
    firewall = "firewall"
    access_point = "access_point"
    pc = "pc"


class DeviceStatus(str, enum.Enum):
    online = "online"
    offline = "offline"
    unknown = "unknown"


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(100), nullable=False, index=True)
    device_type = Column(Enum(DeviceType), nullable=False)
    ip_address = Column(String(45), unique=True, nullable=False, index=True)
    mac_address = Column(String(17), nullable=True)
    location = Column(String(150), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(DeviceStatus), default=DeviceStatus.unknown)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())