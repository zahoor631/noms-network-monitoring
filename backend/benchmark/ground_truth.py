"""
Ground Truth Logger
===================
Converts scenarios into timeline events (UP/DOWN) for comparison
with monitoring output.
"""
from typing import List, Dict, Tuple
from benchmark.scenarios import Scenario


def generate_ground_truth_timeline(
    scenario: Scenario,
    interval_sec: float = 1.0,
) -> List[Dict]:
    """
    Generate ground truth timeline at every interval_sec.
    
    Returns list of:
    {
        "timestamp_sec": float,
        "actual_status": "up" | "down",
        "event": description
    }
    """
    timeline = []
    total_duration = scenario.duration_sec
    t = 0.0
    
    # Build status at each moment
    while t <= total_duration:
        status = "up"  # default
        current_event = None
        
        for event in scenario.ground_truth:
            event_start = event.timestamp_sec
            event_end = event_start + event.duration_sec
            if event_start <= t < event_end:
                status = event.event_type
                current_event = event
                break
        
        timeline.append({
            "scenario_id": scenario.id,
            "timestamp_sec": round(t, 2),
            "actual_status": status,
            "event": current_event.event_type if current_event else "none",
        })
        
        t += interval_sec
    
    return timeline


def find_actual_failure_windows(scenario: Scenario) -> List[Tuple[float, float]]:
    """
    Find windows where device was actually DOWN.
    Returns list of (start_sec, end_sec) tuples.
    """
    windows = []
    for event in scenario.ground_truth:
        if event.event_type == "down":
            windows.append((event.timestamp_sec, event.timestamp_sec + event.duration_sec))
    return windows


def export_ground_truth_csv(scenario: Scenario, output_path: str) -> int:
    """Export ground truth to CSV"""
    import csv
    
    timeline = generate_ground_truth_timeline(scenario, interval_sec=1.0)
    
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["scenario_id", "timestamp_sec", "actual_status", "event"])
        writer.writeheader()
        writer.writerows(timeline)
    
    return len(timeline)


if __name__ == "__main__":
    from benchmark.scenarios import get_all_scenarios
    
    scenarios = get_all_scenarios()
    for s in scenarios:
        timeline = generate_ground_truth_timeline(s)
        failures = find_actual_failure_windows(s)
        print(f"\n{s.id}: {s.name}")
        print(f"  Timeline entries: {len(timeline)}")
        print(f"  Actual failure windows: {failures}")