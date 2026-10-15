"""
Automated Test Runner
=====================
Runs all scenarios with all approaches and multiple repetitions.
"""
import os
import csv
import sys
import time
from datetime import datetime
from typing import List, Dict

from benchmark.scenarios import get_all_scenarios, get_scenario_by_id
from benchmark.baseline import FixedIntervalMonitor
from benchmark.adaptive import AdaptiveMonitor
from benchmark.adaptive_conf import AdaptiveConfirmationMonitor
from benchmark.ground_truth import generate_ground_truth_timeline


OUTPUT_DIR = "benchmark/results"
GROUND_TRUTH_DIR = "benchmark/ground_truth"
TARGET_IP = "8.8.8.8"  # Google DNS (reliable target)
TEST_DURATION = 30  # seconds per test (reduced for speed)
REPETITIONS = 2  # Start with 2; scale to 10 later


def save_results_csv(results: List[Dict], filepath: str) -> None:
    """Save results to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if not results:
        return
    
    # Collect all unique keys
    all_keys = set()
    for entry in results:
        all_keys.update(entry.keys())
    
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
        writer.writeheader()
        writer.writerows(results)


def save_ground_truth(scenario, filepath: str) -> int:
    """Save ground truth timeline to CSV."""
    timeline = generate_ground_truth_timeline(scenario, interval_sec=1.0)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["scenario_id", "timestamp_sec", "actual_status", "event"])
        writer.writeheader()
        writer.writerows(timeline)
    
    return len(timeline)


def run_single_test(scenario_id: str, approach: str, rep: int) -> Dict:
    """
    Run one test: scenario × approach × repetition.
    
    Returns summary dict.
    """
    scenario = get_scenario_by_id(scenario_id)
    
    if approach == "A_baseline":
        monitor = FixedIntervalMonitor(interval=5, failure_threshold=3)
    elif approach == "B_adaptive":
        monitor = AdaptiveMonitor(min_interval=5, max_interval=30, failure_threshold=3)
    elif approach == "C_adaptive_conf":
        monitor = AdaptiveConfirmationMonitor(
            min_interval=5, max_interval=30,
            failure_threshold=3, recovery_threshold=2,
            alert_cooldown_sec=60,
        )
    else:
        raise ValueError(f"Unknown approach: {approach}")
    
    # Run test
    entries = monitor.run(scenario_id, TARGET_IP, TEST_DURATION)
    
    # Save CSV
    output_file = os.path.join(OUTPUT_DIR, f"{scenario_id}_{approach}_rep{rep}.csv")
    save_results_csv(entries, output_file)
    
    stats = monitor.get_stats()
    stats["scenario_id"] = scenario_id
    stats["approach"] = approach
    stats["repetition"] = rep
    
    return stats


def run_full_benchmark(repetitions: int = REPETITIONS, scenarios_filter: List[str] = None):
    """
    Run full benchmark: all scenarios × all approaches × repetitions.
    """
    scenarios = get_all_scenarios()
    
    if scenarios_filter:
        scenarios = [s for s in scenarios if s.id in scenarios_filter]
    
    approaches = ["A_baseline", "B_adaptive", "C_adaptive_conf"]
    
    total_tests = len(scenarios) * len(approaches) * repetitions
    
    print(f"\n{'='*70}")
    print(f"AUTOMATED BENCHMARK")
    print(f"{'='*70}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Approaches: {len(approaches)}")
    print(f"Repetitions: {repetitions}")
    print(f"Total tests: {total_tests}")
    print(f"Estimated time: ~{total_tests * (TEST_DURATION + 10) / 60:.1f} minutes")
    print(f"{'='*70}\n")
    
    # Save all ground truths first
    for scenario in scenarios:
        gt_file = os.path.join(GROUND_TRUTH_DIR, f"{scenario.id}_ground_truth.csv")
        save_ground_truth(scenario, gt_file)
    
    all_results = []
    test_num = 0
    start_time = time.time()
    
    for scenario in scenarios:
        for approach in approaches:
            for rep in range(1, repetitions + 1):
                test_num += 1
                elapsed = time.time() - start_time
                eta = (elapsed / test_num) * (total_tests - test_num) if test_num > 1 else 0
                
                print(f"[{test_num}/{total_tests}] "
                      f"Scenario={scenario.id} "
                      f"Approach={approach} "
                      f"Rep={rep} "
                      f"(ETA: {eta/60:.1f}min)")
                
                try:
                    result = run_single_test(scenario.id, approach, rep)
                    all_results.append(result)
                except Exception as e:
                    print(f"  ❌ Error: {e}")
    
    # Save summary
    summary_file = os.path.join(OUTPUT_DIR, "benchmark_summary.csv")
    save_results_csv(all_results, summary_file)
    
    total_time = (time.time() - start_time) / 60
    print(f"\n{'='*70}")
    print(f"BENCHMARK COMPLETE")
    print(f"{'='*70}")
    print(f"Total tests: {len(all_results)}")
    print(f"Total time: {total_time:.1f} minutes")
    print(f"Summary saved: {summary_file}")
    print(f"{'='*70}")
    
    return all_results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=REPETITIONS, help="Repetitions per test")
    parser.add_argument("--scenarios", nargs="*", default=None, help="Scenario IDs (e.g., S1 S2)")
    args = parser.parse_args()
    
    run_full_benchmark(repetitions=args.reps, scenarios_filter=args.scenarios)