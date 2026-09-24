from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.config import settings
from app.database import Base, engine

from app import models  # noqa
from app.routers import (
    auth, users, devices, monitoring, ipam,
    alerts, tickets, topology, reports,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NOMS API",
    description="Network Operations & Monitoring System",
    version="0.1.0",
)

# Create uploads folder
Path("uploads/avatars").mkdir(parents=True, exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,       prefix="/api/auth",       tags=["Auth"])
app.include_router(users.router,      prefix="/api/users",      tags=["Users"])
app.include_router(devices.router,    prefix="/api/devices",    tags=["Devices"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["Monitoring"])
app.include_router(ipam.router,       prefix="/api/ipam",       tags=["IPAM"])
app.include_router(alerts.router,     prefix="/api/alerts",     tags=["Alerts"])
app.include_router(tickets.router,    prefix="/api/tickets",    tags=["Tickets"])
app.include_router(topology.router,   prefix="/api/topology",   tags=["Topology"])
app.include_router(reports.router,    prefix="/api/reports",    tags=["Reports"])


@app.get("/")
def root():
    return {"message": "NOMS API running", "version": "0.1.0"}


@app.get("/health")
def health():
    return {"status": "ok"}