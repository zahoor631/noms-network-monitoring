from sqlalchemy.orm import Session
from app.models.device import Device, DeviceType, DeviceStatus
import ipaddress


def build_topology(db: Session) -> dict:
    """Basic topology — nodes only, no auto-links."""
    devices = db.query(Device).all()
    nodes = [
        {
            "id": str(d.id),
            "label": d.hostname,
            "type": d.device_type.value,
            "ip": d.ip_address,
            "status": d.status.value,
            "location": d.location,
        }
        for d in devices
    ]
    return {"nodes": nodes, "edges": []}


def _parse_ip_safe(ip_str: str):
    """Return ip_address object or None if invalid."""
    try:
        return ipaddress.ip_address(ip_str)
    except Exception:
        return None


def _subnet_of(ip_obj):
    """Guess a /24 subnet for private IPs; /24 for public too (best effort)."""
    if ip_obj is None:
        return None
    return ipaddress.ip_network(f"{ip_obj}/24", strict=False)


def auto_discover_topology(db: Session) -> dict:
    """
    Auto-discover topology using multiple heuristics:

    1. Classify devices into layers:
       - L1: Firewall, Router
       - L2: Switch, Access Point
       - L3: Server, PC

    2. Connect:
       - Every L1  -> every L2 (if any L2 exists)
       - Every L2  -> every L3 (if any L2 exists)
       - If no L2, L1 -> every L3

    3. Subnet inference (bonus edges):
       - Devices in the same /24 subnet are connected to a "virtual hub"
         (represented by the first device of that subnet in L2/L1)

    Returns: {nodes: [...], edges: [...]}
    """
    devices = db.query(Device).all()

    # Nodes
    nodes = [
        {
            "id": str(d.id),
            "label": d.hostname,
            "type": d.device_type.value,
            "ip": d.ip_address,
            "status": d.status.value,
            "location": d.location,
        }
        for d in devices
    ]

    # Classify devices
    L1_types = {DeviceType.firewall, DeviceType.router}
    L2_types = {DeviceType.switch, DeviceType.access_point}
    L3_types = {DeviceType.server, DeviceType.pc}

    l1 = [d for d in devices if d.device_type in L1_types]
    l2 = [d for d in devices if d.device_type in L2_types]
    l3 = [d for d in devices if d.device_type in L3_types]

    edges = []
    edge_set = set()  # to avoid duplicates

    def add_edge(src, dst, label="", etype="ethernet"):
        key = tuple(sorted([str(src), str(dst)]))
        if key in edge_set:
            return
        edge_set.add(key)
        edges.append({
            "id": f"e{src}-{dst}",
            "source": str(src),
            "target": str(dst),
            "label": label,
            "type": etype,
        })

    # Case 1: All 3 layers present
    if l1 and l2 and l3:
        # L1 -> L2
        for r in l1:
            for s in l2:
                add_edge(r.id, s.id, "trunk", "trunk")
        # L2 -> L3
        for s in l2:
            for srv in l3:
                add_edge(s.id, srv.id, "access", "access")

    # Case 2: L1 + L3 only (no L2)
    elif l1 and l3:
        for r in l1:
            for srv in l3:
                add_edge(r.id, srv.id, "direct", "direct")

    # Case 3: L1 + L2 only
    elif l1 and l2:
        for r in l1:
            for s in l2:
                add_edge(r.id, s.id, "trunk", "trunk")

    # Case 4: L2 + L3 only
    elif l2 and l3:
        for s in l2:
            for srv in l3:
                add_edge(s.id, srv.id, "access", "access")

    # Case 5: Same subnet (bonus) — connect devices in same /24 to L1/L2 hub
    # Build subnet -> devices map
    subnet_map: dict[str, list[Device]] = {}
    for d in devices:
        ip_obj = _parse_ip_safe(d.ip_address)
        if not ip_obj:
            continue
        net = _subnet_of(ip_obj)
        if not net:
            continue
        subnet_map.setdefault(str(net), []).append(d)

    for net, devs in subnet_map.items():
        if len(devs) < 2:
            continue
        # Find a hub: prefer L2, then L1, then first device
        hub = None
        for d in devs:
            if d.device_type in L2_types:
                hub = d
                break
        if not hub:
            for d in devs:
                if d.device_type in L1_types:
                    hub = d
                    break
        if not hub:
            hub = devs[0]
        # Connect all others to hub
        for d in devs:
            if d.id != hub.id:
                add_edge(hub.id, d.id, f"subnet {net}", "subnet")

    return {"nodes": nodes, "edges": edges}