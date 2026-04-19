import json
import statistics
from collections import defaultdict
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT_DIR / "results_log.jsonl"

def compute_metrics():
    if not LOG_FILE.exists():
        print(f"Error: Could not find results file at {LOG_FILE}")
        return

    runs = defaultdict(list)

    with open(LOG_FILE) as f:
        for line in f:
            if line.strip():
                try:
                    r = json.loads(line)
                    runs[r["scenario_id"]].append(r)
                except json.JSONDecodeError:
                    continue

    print("=" * 50)
    print("IEEE ACCESS EXPERIMENT METRICS")
    print("=" * 50)

    for scenario_id, results in runs.items():
        decisions = [r["decision"] for r in results]
        # DCR: Decision Consistency Rate
        dcr = decisions.count(decisions[0]) / len(decisions)
        
        # DDR: Divergent Decision Rate
        divergent = [r for r in results if r["divergence_detected"]]
        if divergent:
            ddr = len([r for r in divergent if r["decision"] == "BLOCK"]) / len(divergent)
        else:
            ddr = None
        
        # FRR: False Rejection/Overlap Rate
        perturbed = [r for r in results if r["boundary_overlap_flag"]]
        if perturbed:
            frr = len([r for r in perturbed if r["decision"] == "BLOCK"]) / len(perturbed)
        else:
            frr = None
        
        # Latency calculations
        latencies = [r["latency_seconds"] for r in results]
        avg_latency = round(sum(latencies)/len(latencies), 4)
        median_latency = round(statistics.median(latencies), 4)
        
        print(f"\n{scenario_id}")
        print(f"  Runs:        {len(results)}")
        print(f"  DCR:         {dcr:.0%}")
        if ddr is not None:
            print(f"  DDR:         {ddr:.0%}")
        else:
            print(f"  DDR:         N/A")
            
        if frr is not None:
            print(f"  FRR:         {frr:.0%}")
        else:
            print(f"  FRR:         N/A")
            
        print(f"  Avg latency: {avg_latency}s")
        print(f"  Med latency: {median_latency}s")

if __name__ == "__main__":
    compute_metrics()
