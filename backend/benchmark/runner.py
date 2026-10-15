"""
Test Runner — Compares 3 Approaches
====================================
A: Baseline (Fixed-Interval)
B: Adaptive
C: Adaptive + Confirmation
"""
import csv
import os
from typing import List, Dict

from benchmark.scenarios import get_scenario_by_id
from benchmark.baseline import FixedIntervalMonitor
from benchmark.adaptive import AdaptiveMonitor
from benchmark.adaptive_conf import AdaptiveConfirmationMonitor
from benchmark.ground_truth import generate_ground_truth_timeline


OUTPUT_DIR = "benchmark/results"
GROUND_TRUTH_DIR = "benchmark/ground_truth"


def save_results_csv(results: List[Dict], filename: str) -> str:
    """Save results to CSV."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    if not results:
        return filepath
    
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    return filepath


def save_ground_truth(scenario, filepath: str) -> int:
    """Save ground truth timeline to CSV."""
    timeline = generate_ground_truth_timeline(scenario, interval_sec=1.0)
    
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["scenario_id", "timestamp_sec", "actual_status", "event"])
        writer.writeheader()
        writer.writerows(timeline)
    
    return len(timeline)


def run_all_approaches(scenario_id: str, target_ip: str = "8.8.8.8", test_duration: int = 30) -> Dict:
    """
    Run all 3 approaches on same scenario.
    
    Returns dict with results from all 3 approaches.
    """
    scenario = get_scenario_by_id(scenario_id)
    
    print(f"\n{'='*70}")
    print(f"Scenario: {scenario.id} — {scenario.name}")
    print(f"{'='*70}")
    print(f"Duration: {scenario.duration_sec}s (test: {test_duration}s)")
    print(f"Target IP: {target_ip}")
    print(f"Description: {scenario.description}")
    
    # Save ground truth
    os.makedirs(GROUND_TRUTH_DIR, exist_ok=True)
    ground_truth_file = os.path.join(GROUND_TRUTH_DIR, f"{scenario_id}_ground_truth.csv")
    export_count = save_ground_truth(scenario, ground_truth_file)
    print(f"\n✅ Ground truth saved: {ground_truth_file} ({export_count} entries)")
    
    # ───── APPROACH A: Baseline ─────
    print(f"\n{'─'*70}")
    print("Approach A: Baseline (Fixed-Interval)")
    print(f"{'─'*70}")
    baseline = FixedIntervalMonitor(interval=5, failure_threshold=3)
    baseline_entries = baseline.run(scenario_id, target_ip, test_duration)
    save_results_csv(baseline_entries, f"{scenario_id}_A_baseline.csv")
    baseline_stats = baseline.get_stats()
    print(f"  Probes: {baseline_stats['total_probes']}")
    print(f"  Alerts: {baseline_stats['alerts']}")
    print(f"  Success rate: {baseline_stats['success_rate']}%")
    
    # ───── APPROACH B: Adaptive ─────
    print(f"\n{'─'*70}")
    print("Approach B: Adaptive Polling")
    print(f"{'─'*70}")
    adaptive = AdaptiveMonitor(min_interval=5, max_interval=30, failure_threshold=3)
    adaptive_entries = adaptive.run(scenario_id, target_ip, test_duration)
    save_results_csv(adaptive_entries, f"{scenario_id}_B_adaptive.csv")
    adaptive_stats = adaptive.get_stats()
    print(f"  Probes: {adaptive_stats['total_probes']}")
    print(f"  Alerts: {adaptive_stats['alerts']}")
    print(f"  Avg interval: {adaptive_stats['avg_interval_sec']}s")
    print(f"  Success rate: {adaptive_stats['success_rate']}%")
    
    # ───── APPROACH C: Adaptive + Confirmation ─────
    print(f"\n{'─'*70}")
    print("Approach C: Adaptive + Confirmation")
    print(f"{'─'*70}")
    adaptive_conf = AdaptiveConfirmationMonitor(
        min_interval=5, max_interval=30,
        failure_threshold=3, recovery_threshold=2,
        alert_cooldown_sec=60,
    )
    adaptive_conf_entries = adaptive_conf.run(scenario_id, target_ip, test_duration)
    save_results_csv(adaptive_conf_entries, f"{scenario_id}_C_adaptive_conf.csv")
    adaptive_conf_stats = adaptive_conf.get_stats()
    print(f"  Probes: {adaptive_conf_stats['total_probes']}")
    print(f"  Alerts: {adaptive_conf_stats['alerts']}")
    print(f"  Alerts suppressed: {adaptive_conf_stats['alerts_suppressed']}")
    print(f"  Avg interval: {adaptive_conf_stats['avg_interval_sec']}s")
    
    # ───── COMPARISON ─────
    print(f"\n{'='*70}")
    print("COMPARISON SUMMARY")
    print(f"{'='*70}")
    print(f"{'Metric':<25} {'A: Baseline':<15} {'B: Adaptive':<15} {'C: Adap+Conf':<15}")
    print(f"{'-'*70}")
    print(f"{'Total Probes':<25} {baseline_stats['total_probes']:<15} {adaptive_stats['total_probes']:<15} {adaptive_conf_stats['total_probes']:<15}")
    print(f"{'Alerts':<25} {baseline_stats['alerts']:<15} {adaptive_stats['alerts']:<15} {adaptive_conf_stats['alerts']:<15}")
    print(f"{'Avg Interval (s)':<25} {'5.0':<15} {adaptive_stats['avg_interval_sec']:<15} {adaptive_conf_stats['avg_interval_sec']:<15}")
    
    return {
        "scenario_id": scenario_id,
        "A_baseline": baseline_stats,
        "B_adaptive": adaptive_stats,
        "C_adaptive_conf": adaptive_conf_stats,
    }


if __name__ == "__main__":
    # Run all 3 approaches on S1
    result = run_all_approaches("S1", target_ip="8.8.8.8", test_duration=30)
    print(f"\n✅ All approaches complete for {result['scenario_id']}")