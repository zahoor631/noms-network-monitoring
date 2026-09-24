from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.device import Device, DeviceType, DeviceStatus
from app.schemas.device import DeviceCreate, DeviceOut, DeviceUpdate, DeviceStats
from app.core.dependencies import get_current_user, admin_or_engineer
from app.services import device_service

router = APIRouter()


@router.get("/stats", response_model=DeviceStats)
def device_stats(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return device_service.get_device_stats(db)


@router.get("/", response_model=List[DeviceOut])
def list_devices(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
    device_type: Optional[DeviceType] = Query(None),
    status: Optional[DeviceStatus] = Query(None),
    search: Optional[str] = Query(None),
):
    q = db.query(Device)
    if device_type:
        q = q.filter(Device.device_type == device_type)
    if status:
        q = q.filter(Device.status == status)
    if search:
        like = f"%{search}%"
        q = q.filter((Device.hostname.like(like)) | (Device.ip_address.like(like)))
    return q.order_by(Device.id.desc()).all()


@router.post("/", response_model=DeviceOut, dependencies=[Depends(admin_or_engineer)])
def create_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    return device_service.create_device(db, payload)


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    return device


@router.patch("/{device_id}", response_model=DeviceOut, dependencies=[Depends(admin_or_engineer)])
def update_device(device_id: int, payload: DeviceUpdate, db: Session = Depends(get_db)):
    return device_service.update_device(db, device_id, payload)


@router.delete("/{device_id}", dependencies=[Depends(admin_or_engineer)])
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device_service.delete_device(db, device_id)
    return {"message": "Device deleted"}