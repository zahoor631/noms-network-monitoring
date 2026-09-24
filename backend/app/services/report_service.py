from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from app.models.device import Device, DeviceStatus
from app.models.device_metric import DeviceMetric
from app.models.alert import Alert
from app.models.ticket import Ticket


def uptime_report(db: Session, days: int = 1) -> list[dict]:
    since = datetime.now(timezone.utc) - timedelta(days=days)
    devices = db.query(Device).all()
    report = []
    for d in devices:
        total = db.query(func.count(DeviceMetric.id)).filter(
            DeviceMetric.device_id == d.id,
            DeviceMetric.recorded_at >= since,
        ).scalar() or 0

        online = db.query(func.count(DeviceMetric.id)).filter(
            DeviceMetric.device_id == d.id,
            DeviceMetric.recorded_at >= since,
            DeviceMetric.packet_loss < 100,
        ).scalar() or 0

        uptime_pct = (online / total * 100) if total else 0
        report.append({
            "device_id": d.id,
            "hostname": d.hostname,
            "uptime_percent": round(uptime_pct, 2),
            "samples": total,
        })
    return report


def incident_report(db: Session) -> list[dict]:
    tickets = db.query(Ticket).all()
    return [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status.value,
            "priority": t.priority.value,
            "created_at": t.created_at.isoformat(),
        }
        for t in tickets
    ]


def dashboard_summary(db: Session) -> dict:
    """Dashboard ke liye saara data ek saath."""
    # Stats
    total = db.query(func.count(Device.id)).scalar() or 0
    online = db.query(func.count(Device.id)).filter(
        Device.status == DeviceStatus.online
    ).scalar() or 0
    offline = db.query(func.count(Device.id)).filter(
        Device.status == DeviceStatus.offline
    ).scalar() or 0
    unknown = total - online - offline

    # Alerts
    active_alerts = db.query(func.count(Alert.id)).filter(
        Alert.is_resolved == False
    ).scalar() or 0

    # Open tickets
    open_tickets = db.query(func.count(Ticket.id)).filter(
        Ticket.status.in_(["open", "in_progress"])
    ).scalar() or 0

    # Bandwidth (last 24h hourly avg)
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    bandwidth_rows = (
        db.query(
            func.date_format(DeviceMetric.recorded_at, "%Y-%m-%d %H:00").label("hour"),
            func.avg(DeviceMetric.bandwidth_mbps).label("avg_bw"),
        )
        .filter(
            DeviceMetric.recorded_at >= since,
            DeviceMetric.bandwidth_mbps.isnot(None),
        )
        .group_by("hour")
        .order_by("hour")
        .all()
    )
    bandwidth = [
        {"time": r.hour, "value": float(r.avg_bw or 0)} for r in bandwidth_rows
    ]

    # CPU / Memory (latest per device avg)
    cpu_rows = (
        db.query(
            func.avg(DeviceMetric.cpu_usage).label("cpu"),
            func.avg(DeviceMetric.memory_usage).label("mem"),
        )
        .filter(
            DeviceMetric.recorded_at >= since,
            DeviceMetric.cpu_usage.isnot(None),
        )
        .first()
    )
    cpu = float(cpu_rows.cpu or 0) if cpu_rows else 0
    memory = float(cpu_rows.mem or 0) if cpu_rows else 0

    # Recent alerts
    recent_alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .limit(5)
        .all()
    )
    alerts_list = [
        {
            "id": a.id,
            "severity": a.severity.value,
            "title": a.title,
            "created_at": a.created_at.isoformat(),
            "is_resolved": a.is_resolved,
        }
        for a in recent_alerts
    ]

    return {
        "stats": {
            "total": total,
            "online": online,
            "offline": offline,
            "unknown": unknown,
            "active_alerts": active_alerts,
            "open_tickets": open_tickets,
        },
        "bandwidth": bandwidth,
        "cpu": round(cpu, 2),
        "memory": round(memory, 2),
        "recent_alerts": alerts_list,
    }