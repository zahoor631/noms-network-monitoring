from ping3 import ping


def is_host_up(ip: str, timeout: int = 2) -> bool:
    try:
        return ping(ip, timeout=timeout) is not None
    except Exception:
        return False


def get_response_time(ip: str, timeout: int = 2) -> float | None:
    try:
        result = ping(ip, timeout=timeout, unit="ms")
        return float(result) if result else None
    except Exception:
        return None