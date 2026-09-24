from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.device import Device, DeviceStatus
from app.schemas.device import DeviceCreate, DeviceUpdate


def create_device(db: Session, payload: DeviceCreate) -> Device:
    if db.query(Device).filter(Device.ip_address == payload.ip_address).first():
        raise HTTPException(400, "IP address already exists")
    device = Device(**payload.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def update_device(db: Session, device_id: int, payload: DeviceUpdate) -> Device:
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(device, k, v)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int) -> None:
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    db.delete(device)
    db.commit()


def get_device_stats(db: Session) -> dict:
    total = db.query(func.count(Device.id)).scalar() or 0
    online = db.query(func.count(Device.id)).filter(
        Device.status == DeviceStatus.online
    ).scalar() or 0
    offline = db.query(func.count(Device.id)).filter(
        Device.status == DeviceStatus.offline
    ).scalar() or 0
    unknown = total - online - offline
    return {"total": total, "online": online, "offline": offline, "unknown": unknown}