from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.services import monitor_service

scheduler = BackgroundScheduler()


def ping_job():
    db = SessionLocal()
    try:
        monitor_service.monitor_all_devices(db)
        print("[scheduler] Ping cycle complete")
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(ping_job, "interval", seconds=60, id="ping_job", replace_existing=True)
    scheduler.start()
    print("[scheduler] Started")