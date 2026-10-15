"""
Metrics Calculation
===================
"""
from typing import List, Dict, Tuple


def count_alerts(monitor_log: List[Dict]) -> int:
    return sum(1 for e in monitor_log if e.get("alert_generated"))


def count_suppressed_alerts(monitor_log: List[Dict]) -> int:
    return sum(1 for e in monitor_log if e.get("alert_suppressed"))


def calculate_monitoring_overhead(monitor_log: List[Dict], duration_sec: int) -> Dict:
    total = len(monitor_log)
    per_minute = (total / duration_sec) * 60 if duration_sec > 0 else 0
    return {
        "total_probes": total,
        "probes_per_minute": round(per_minute, 2),
        "duration_sec": duration_sec,
    }


def compare_approaches(results: Dict) -> Dict:
    """
    Compare multiple approaches.
    results: {approach_name: stats_dict}
    """
    comparison = {
        "approaches": list(results.keys()),
        "metrics": {},
    }
    
    for approach, stats in results.items():
        comparison["metrics"][approach] = {
            "total_probes": stats.get("total_probes", 0),
            "alerts": stats.get("alerts", 0),
            "avg_interval": stats.get("avg_interval_sec", 0),
            "success_rate": stats.get("success_rate", 0),
        }
    
    return comparison


if __name__ == "__main__":
    print("✅ Metrics module loaded successfully")