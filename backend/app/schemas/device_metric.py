from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class DeviceMetricOut(BaseModel):
    id: int
    device_id: int
    response_time_ms: int | None
    packet_loss: Decimal | None
    cpu_usage: Decimal | None
    memory_usage: Decimal | None
    bandwidth_mbps: Decimal | None
    recorded_at: datetime

    class Config:
        from_attributes = True