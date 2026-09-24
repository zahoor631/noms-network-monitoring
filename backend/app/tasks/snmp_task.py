from app.database import SessionLocal
from app.models.device import Device
from app.services import snmp_service


def run_snmp_cycle():
    """Placeholder: iterate devices and poll SNMP."""
    db = SessionLocal()
    try:
        devices = db.query(Device).all()
        for d in devices:
            result = snmp_service.poll_snmp(d.ip_address)
            print(f"[snmp] {d.hostname}: {result}")
    finally:
        db.close()