from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.services import topology_service

router = APIRouter()


@router.get("/")
def get_topology(db: Session = Depends(get_db), _=Depends(get_current_user)):
    """Simple topology — nodes only."""
    return topology_service.build_topology(db)


@router.get("/auto-discover")
def auto_discover(db: Session = Depends(get_db), _=Depends(get_current_user)):
    """
    Auto-discover network topology using layered + subnet inference.
    """
    return topology_service.auto_discover_topology(db)