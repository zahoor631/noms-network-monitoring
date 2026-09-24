from app.database import SessionLocal
from app.models.device import Device, DeviceStatus
from app.models.alert import Alert, AlertSeverity


def check_offline_devices():
    """Create alerts for offline devices."""
    db = SessionLocal()
    try:
        offline = db.query(Device).filter(Device.status == DeviceStatus.offline).all()
        for d in offline:
            exists = db.query(Alert).filter(
                Alert.device_id == d.id,
                Alert.title == f"{d.hostname} Offline",
                Alert.is_resolved == False,
            ).first()
            if not exists:
                db.add(Alert(
                    device_id=d.id,
                    severity=AlertSeverity.critical,
                    title=f"{d.hostname} Offline",
                    message=f"Device {d.ip_address} is unreachable",
                ))
        db.commit()
    finally:
        db.close()