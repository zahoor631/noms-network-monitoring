import ipaddress


def subnet_info(ip: str, cidr: int) -> dict:
    """Calculate subnet details."""
    net = ipaddress.ip_network(f"{ip}/{cidr}", strict=False)
    hosts = list(net.hosts())
    return {
        "network": str(net.network_address),
        "broadcast": str(net.broadcast_address),
        "netmask": str(net.netmask),
        "first_host": str(hosts[0]) if hosts else str(net.network_address),
        "last_host": str(hosts[-1]) if hosts else str(net.broadcast_address),
        "total_hosts": net.num_addresses,
        "usable_hosts": max(0, net.num_addresses - 2),
        "hosts": [str(h) for h in hosts],
    }