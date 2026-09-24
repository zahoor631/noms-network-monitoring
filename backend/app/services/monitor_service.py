import asyncio
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ping3 import ping
from app.models.device import Device, DeviceStatus
from app.models.device_metric import DeviceMetric
from app.config import settings


def ping_host(ip: str, timeout: int = 2) -> float | None:
    """Return response time in ms or None if unreachable."""
    try:
        result = ping(ip, timeout=timeout, unit="ms")
        return float(result) if result else None
    except Exception:
        return None


def monitor_device(db: Session, device: Device) -> DeviceMetric:
    resp_ms = ping_host(device.ip_address, timeout=settings.PING_TIMEOUT)
    now = datetime.now(timezone.utc)

    if resp_ms is not None:
        device.status = DeviceStatus.online
        device.last_seen = now
        metric = DeviceMetric(
            device_id=device.id,
            response_time_ms=int(resp_ms),
            packet_loss=0,
        )
    else:
        device.status = DeviceStatus.offline
        metric = DeviceMetric(
            device_id=device.id,
            packet_loss=100,
        )

    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


def monitor_all_devices(db: Session) -> list[DeviceMetric]:
    devices = db.query(Device).all()
    metrics = []
    for d in devices:
        try:
            metrics.append(monitor_device(db, d))
        except Exception as e:
            print(f"[monitor] Error on {d.hostname}: {e}")
    return metrics