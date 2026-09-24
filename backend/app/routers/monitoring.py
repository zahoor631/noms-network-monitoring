from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.device_metric import DeviceMetric
from app.schemas.device_metric import DeviceMetricOut
from app.core.dependencies import get_current_user, admin_or_engineer
from app.services import monitor_service

router = APIRouter()


@router.post("/ping/{device_id}", dependencies=[Depends(admin_or_engineer)])
def ping_now(device_id: int, db: Session = Depends(get_db)):
    from app.models.device import Device
    device = db.query(Device).get(device_id)
    if not device:
        return {"error": "Device not found"}
    metric = monitor_service.monitor_device(db, device)
    return {
        "device_id": device.id,
        "status": device.status.value,
        "response_time_ms": metric.response_time_ms,
        "packet_loss": float(metric.packet_loss or 0),
    }


@router.post("/ping-all", dependencies=[Depends(admin_or_engineer)])
def ping_all(db: Session = Depends(get_db)):
    metrics = monitor_service.monitor_all_devices(db)
    return {"monitored": len(metrics)}


@router.get("/metrics/{device_id}", response_model=List[DeviceMetricOut])
def device_metrics(
    device_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return (
        db.query(DeviceMetric)
        .filter(DeviceMetric.device_id == device_id)
        .order_by(DeviceMetric.recorded_at.desc())
        .limit(limit)
        .all()
    )