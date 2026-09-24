from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum


class IPStatus(str, enum.Enum):
    available = "available"
    used = "used"
    reserved = "reserved"


class IPAddress(Base):
    __tablename__ = "ip_addresses"

    id = Column(Integer, primary_key=True, index=True)
    subnet_id = Column(Integer, ForeignKey("subnets.id", ondelete="CASCADE"))
    ip = Column(String(45), unique=True, nullable=False, index=True)
    status = Column(Enum(IPStatus), default=IPStatus.available)
    assigned_to = Column(String(150), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())