from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.subnet import Subnet
from app.models.ip_address import IPAddress, IPStatus
from app.schemas.subnet import SubnetCreate, SubnetUpdate
from app.utils.network_utils import subnet_info


def create_subnet(db: Session, payload: SubnetCreate) -> Subnet:
    exists = db.query(Subnet).filter(
        Subnet.network == payload.network,
        Subnet.cidr == payload.cidr,
    ).first()
    if exists:
        raise HTTPException(400, "Subnet already exists")
    subnet = Subnet(**payload.model_dump())
    db.add(subnet)
    db.commit()
    db.refresh(subnet)
    return subnet


def update_subnet(db: Session, subnet_id: int, payload: SubnetUpdate) -> Subnet:
    subnet = db.query(Subnet).get(subnet_id)
    if not subnet:
        raise HTTPException(404, "Subnet not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(subnet, k, v)
    db.commit()
    db.refresh(subnet)
    return subnet


def delete_subnet(db: Session, subnet_id: int) -> None:
    subnet = db.query(Subnet).get(subnet_id)
    if not subnet:
        raise HTTPException(404, "Subnet not found")
    db.delete(subnet)
    db.commit()


def generate_ips_for_subnet(db: Session, subnet_id: int) -> int:
    subnet = db.query(Subnet).get(subnet_id)
    if not subnet:
        raise HTTPException(404, "Subnet not found")

    info = subnet_info(subnet.network, subnet.cidr)
    ips = []
    for ip in info["hosts"]:
        exists = db.query(IPAddress).filter(IPAddress.ip == ip).first()
        if not exists:
            ips.append(IPAddress(subnet_id=subnet.id, ip=ip, status=IPStatus.available))
    db.add_all(ips)
    db.commit()
    return len(ips)