"""
SNMP polling service (placeholder).
Real deployment: use pysnmp to poll CPU/Memory/Bandwidth from network devices.
"""


def poll_snmp(ip: str, community: str = "public") -> dict:
    """
    Placeholder. Returns fake metrics.
    Replace with actual pysnmp implementation later.
    """
    return {
        "ip": ip,
        "cpu_usage": None,
        "memory_usage": None,
        "bandwidth_mbps": None,
        "note": "SNMP polling not implemented yet",
    }