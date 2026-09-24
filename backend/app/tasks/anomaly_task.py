from app.database import SessionLocal
from app.models.device import Device
from app.services import anomaly_service


def run_anomaly_detection():
    db = SessionLocal()
    try:
        devices = db.query(Device).all()
        for d in devices:
            result = anomaly_service.detect_anomalies(db, d.id)
            if result.get("anomaly"):
                print(f"[anomaly] {d.hostname}: {result}")
    finally:
        db.close()