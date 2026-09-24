from sqlalchemy import Column, BigInteger, Integer, DECIMAL, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base


class DeviceMetric(Base):
    __tablename__ = "device_metrics"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(
        Integer,
        ForeignKey("devices.id", ondelete="CASCADE"),
        index=True,
    )
    response_time_ms = Column(Integer, nullable=True)
    packet_loss = Column(DECIMAL(5, 2), default=0)
    cpu_usage = Column(DECIMAL(5, 2), nullable=True)
    memory_usage = Column(DECIMAL(5, 2), nullable=True)
    bandwidth_mbps = Column(DECIMAL(10, 2), nullable=True)
    recorded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )