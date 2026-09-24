from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Subnet(Base):
    __tablename__ = "subnets"

    id = Column(Integer, primary_key=True, index=True)
    network = Column(String(45), nullable=False, index=True)  # e.g. 192.168.1.0
    cidr = Column(Integer, nullable=False)                    # e.g. 24
    gateway = Column(String(45), nullable=True)
    vlan = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())