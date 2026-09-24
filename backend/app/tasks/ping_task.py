from app.database import SessionLocal
from app.services import monitor_service


def run_ping_cycle():
    db = SessionLocal()
    try:
        return monitor_service.monitor_all_devices(db)
    finally:
        db.close()