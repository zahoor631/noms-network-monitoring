"""
Test Scenarios
==============
6 scenarios to test monitoring approaches.

Each scenario simulates a specific network condition and produces:
- Device behavior (UP/DOWN/latency)
- Ground truth log (when device was actually UP/DOWN)
- Duration for the test
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict


@dataclass
class ScenarioEvent:
    """Single event in scenario (e.g., device goes down)"""
    timestamp_sec: float  # seconds from start
    event_type: str  # "up", "down", "latency_spike", "packet_loss"
    duration_sec: float = 0  # 0 = instant, >0 = lasts for X seconds
    value: float = 0  # e.g., latency in ms


@dataclass
class Scenario:
    """Test scenario definition"""
    id: str
    name: str
    description: str
    duration_sec: int
    ground_truth: List[ScenarioEvent]
    expected_probes_per_min: int


def get_all_scenarios() -> List[Scenario]:
    """Return all 6 test scenarios"""
    
    scenarios = []
    
    # ───── S1: Stable Network ─────
    s1 = Scenario(
        id="S1",
        name="Stable Network",
        description="Device always reachable. Tests false alarm rate.",
        duration_sec=60,
        ground_truth=[
            ScenarioEvent(0, "up", 60),  # Always UP
        ],
        expected_probes_per_min=12,
    )
    scenarios.append(s1)
    
    # ───── S2: Transient Packet Loss ─────
    s2 = Scenario(
        id="S2",
        name="Transient Packet Loss",
        description="1-2 consecutive probes lost, then recover. Tests flapping resistance.",
        duration_sec=60,
        ground_truth=[
            ScenarioEvent(0, "up", 60),  # Always UP (packet loss is not failure)
        ],
        expected_probes_per_min=12,
    )
    scenarios.append(s2)
    
    # ───── S3: Short Outage (10s) ─────
    s3 = Scenario(
        id="S3",
        name="Short Outage (10s)",
        description="Device DOWN for 10 seconds. Tests detection delay.",
        duration_sec=60,
        ground_truth=[
            ScenarioEvent(0, "up", 20),
            ScenarioEvent(20, "down", 10),
            ScenarioEvent(30, "up", 30),
        ],
        expected_probes_per_min=12,
    )
    scenarios.append(s3)
    
    # ───── S4: Long Outage (60s) ─────
    s4 = Scenario(
        id="S4",
        name="Long Outage (60s)",
        description="Device DOWN for 60 seconds. Tests sustained failure detection.",
        duration_sec=120,
        ground_truth=[
            ScenarioEvent(0, "up", 30),
            ScenarioEvent(30, "down", 60),
            ScenarioEvent(90, "up", 30),
        ],
        expected_probes_per_min=12,
    )
    scenarios.append(s4)
    
    # ───── S5: Latency Spike ─────
    s5 = Scenario(
        id="S5",
        name="Latency Spike",
        description="Device UP but latency spikes 20ms → 500ms. Tests latency handling.",
        duration_sec=60,
        ground_truth=[
            ScenarioEvent(0, "up", 60),  # Always UP
        ],
        expected_probes_per_min=12,
    )
    scenarios.append(s5)
    
    # ───── S6: Recovery Detection ─────
    s6 = Scenario(
        id="S6",
        name="Recovery Detection",
        description="Device DOWN for 30s, then recovers. Tests recovery detection.",
        duration_sec=60,
        ground_truth=[
            ScenarioEvent(0, "up", 10),
            ScenarioEvent(10, "down", 30),
            ScenarioEvent(40, "up", 20),
        ],
        expected_probes_per_min=12,
    )
    scenarios.append(s6)
    
    return scenarios


def get_scenario_by_id(scenario_id: str) -> Scenario:
    """Get scenario by ID"""
    scenarios = get_all_scenarios()
    for s in scenarios:
        if s.id == scenario_id:
            return s
    raise ValueError(f"Scenario {scenario_id} not found")


def export_ground_truth(scenario: Scenario) -> List[Dict]:
    """
    Export scenario as ground truth log.
    Each entry: {timestamp_sec, event_type, duration_sec, value}
    """
    entries = []
    for event in scenario.ground_truth:
        entries.append({
            "scenario_id": scenario.id,
            "timestamp_sec": event.timestamp_sec,
            "event_type": event.event_type,
            "duration_sec": event.duration_sec,
            "value": event.value,
        })
    return entries


if __name__ == "__main__":
    scenarios = get_all_scenarios()
    print(f"Total scenarios: {len(scenarios)}")
    for s in scenarios:
        print(f"\n{s.id}: {s.name}")
        print(f"  Duration: {s.duration_sec}s")
        print(f"  Events: {len(s.ground_truth)}")
        print(f"  Description: {s.description}")