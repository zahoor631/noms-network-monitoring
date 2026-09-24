"""
AI anomaly detection (simple statistical baseline).
Later: replace with ML model.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from app.models.device_metric import DeviceMetric


def detect_anomalies(db: Session, device_id: int, window_days: int = 7) -> dict:
    since = datetime.now(timezone.utc) - timedelta(days=window_days)

    stats = db.query(
        func.avg(DeviceMetric.bandwidth_mbps),
        func.stddev(DeviceMetric.bandwidth_mbps),
    ).filter(
        DeviceMetric.device_id == device_id,
        DeviceMetric.recorded_at >= since,
        DeviceMetric.bandwidth_mbps.isnot(None),
    ).first()

    avg_bw, std_bw = stats
    if avg_bw is None or std_bw is None:
        return {"anomaly": False, "reason": "Not enough data"}

    latest = db.query(DeviceMetric).filter(
        DeviceMetric.device_id == device_id
    ).order_by(DeviceMetric.recorded_at.desc()).first()

    if not latest or latest.bandwidth_mbps is None:
        return {"anomaly": False, "reason": "No recent data"}

    threshold = float(avg_bw) + 3 * float(std_bw)
    current = float(latest.bandwidth_mbps)

    if current > threshold:
        return {
            "anomaly": True,
            "current_bw": current,
            "average_bw": float(avg_bw),
            "threshold": threshold,
            "message": f"Abnormal bandwidth: {current:.2f} Mbps (avg {avg_bw:.2f})",
        }
    return {"anomaly": False, "current_bw": current, "average_bw": float(avg_bw)}