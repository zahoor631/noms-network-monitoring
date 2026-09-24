from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.subnet import Subnet
from app.models.ip_address import IPAddress
from app.schemas.subnet import (
    SubnetCreate, SubnetOut, SubnetUpdate, SubnetCalcRequest, SubnetCalcResponse,
)
from app.schemas.ip_address import IPAddressOut, IPAddressUpdate
from app.core.dependencies import get_current_user, admin_or_engineer
from app.services import ipam_service
from app.utils.network_utils import subnet_info

router = APIRouter()


# ----- Subnets -----
@router.get("/subnets", response_model=List[SubnetOut])
def list_subnets(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Subnet).order_by(Subnet.id.desc()).all()


@router.post("/subnets", response_model=SubnetOut, dependencies=[Depends(admin_or_engineer)])
def create_subnet(payload: SubnetCreate, db: Session = Depends(get_db)):
    return ipam_service.create_subnet(db, payload)


@router.patch("/subnets/{subnet_id}", response_model=SubnetOut, dependencies=[Depends(admin_or_engineer)])
def update_subnet(subnet_id: int, payload: SubnetUpdate, db: Session = Depends(get_db)):
    return ipam_service.update_subnet(db, subnet_id, payload)


@router.delete("/subnets/{subnet_id}", dependencies=[Depends(admin_or_engineer)])
def delete_subnet(subnet_id: int, db: Session = Depends(get_db)):
    ipam_service.delete_subnet(db, subnet_id)
    return {"message": "Subnet deleted"}


@router.post("/subnets/{subnet_id}/generate-ips", dependencies=[Depends(admin_or_engineer)])
def generate_ips(subnet_id: int, db: Session = Depends(get_db)):
    count = ipam_service.generate_ips_for_subnet(db, subnet_id)
    return {"generated": count}


# ----- IPs -----
@router.get("/ips", response_model=List[IPAddressOut])
def list_ips(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(IPAddress).order_by(IPAddress.id.desc()).all()


@router.get("/subnets/{subnet_id}/ips", response_model=List[IPAddressOut])
def list_subnet_ips(subnet_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(IPAddress).filter(IPAddress.subnet_id == subnet_id).all()


@router.patch("/ips/{ip_id}", response_model=IPAddressOut, dependencies=[Depends(admin_or_engineer)])
def update_ip(ip_id: int, payload: IPAddressUpdate, db: Session = Depends(get_db)):
    ip = db.query(IPAddress).get(ip_id)
    if not ip:
        raise HTTPException(404, "IP not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(ip, k, v)
    db.commit()
    db.refresh(ip)
    return ip


# ----- Calculator -----
@router.post("/subnet-calculator", response_model=SubnetCalcResponse)
def subnet_calculator(payload: SubnetCalcRequest, _=Depends(get_current_user)):
    info = subnet_info(payload.ip, payload.cidr)
    return {
        "network": info["network"],
        "broadcast": info["broadcast"],
        "netmask": info["netmask"],
        "first_host": info["first_host"],
        "last_host": info["last_host"],
        "total_hosts": info["total_hosts"],
        "usable_hosts": info["usable_hosts"],
    }