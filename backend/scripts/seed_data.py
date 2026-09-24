"""
Run: python -m scripts.seed_data
Insert demo devices & subnets.
"""
from app.database import SessionLocal, Base, engine
from app.models.device import Device, DeviceType, DeviceStatus
from app.models.subnet import Subnet
from app import models  # noqa

Base.metadata.create_all(bind=engine)

DEMO_DEVICES = [
    ("core-router-01", DeviceType.router, "10.0.0.1", "Data Center"),
    ("core-switch-01", DeviceType.switch, "10.0.0.2", "Data Center"),
    ("fw-01", DeviceType.firewall, "10.0.0.3", "Data Center"),
    ("web-server-01", DeviceType.server, "10.0.1.10", "Server Room"),
    ("ap-floor1", DeviceType.access_point, "10.0.2.5", "Floor 1"),
]

DEMO_SUBNETS = [
    ("192.168.1.0", 24, "192.168.1.1", 10, "Office LAN"),
    ("10.0.0.0", 24, "10.0.0.1", 100, "Data Center"),
]

db = SessionLocal()
try:
    for hostname, dtype, ip, loc in DEMO_DEVICES:
        if not db.query(Device).filter(Device.ip_address == ip).first():
            db.add(Device(
                hostname=hostname,
                device_type=dtype,
                ip_address=ip,
                location=loc,
                status=DeviceStatus.unknown,
            ))

    for network, cidr, gw, vlan, desc in DEMO_SUBNETS:
        if not db.query(Subnet).filter(Subnet.network == network, Subnet.cidr == cidr).first():
            db.add(Subnet(
                network=network, cidr=cidr, gateway=gw,
                vlan=vlan, description=desc,
            ))

    db.commit()
    print("✅ Demo data inserted")
finally:
    db.close()