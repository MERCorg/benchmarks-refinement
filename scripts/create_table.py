import json
import argparse
from collections import defaultdict


def main():
    # Parse some configuration options
    parser = argparse.ArgumentParser(
        prog="create_table.py",
        description="Creates a table from benchmark results",
        epilog="",
    )

    parser.add_argument(
        "result_path", action="store", type=str
    )
    args = parser.parse_args()

    # Read NDJSON format (one JSON object per line)
    results_by_dir_algo = defaultdict(list)
    
    with open(args.result_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                result = json.loads(line)
                directory = result.get("directory", "unknown")
                algorithm = result.get("algorithm", "unknown")
                time_val = result.get("time", 0)
                
                results_by_dir_algo[(directory, algorithm)].append(time_val)
    
    # Calculate statistics
    stats = {}
    for (directory, algorithm), times in results_by_dir_algo.items():
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        stats[(directory, algorithm)] = {
            "avg": avg_time,
            "min": min_time,
            "max": max_time,
            "runs": len(times)
        }
    
    # Group by directory and algorithm
    directories = sorted(set(d for d, a in stats.keys()))
    algorithms = sorted(set(a for d, a in stats.keys()))
    
    # Print table header
    print(f"{'Directory':<25} | {' | '.join(f'{algo:<15}' for algo in algorithms)}")
    print("-" * (25 + 3 + len(algorithms) * 19))
    
    # Print table rows
    for directory in directories:
        row_parts = [f"{directory:<25}"]
        for algorithm in algorithms:
            if (directory, algorithm) in stats:
                avg_time = stats[(directory, algorithm)]["avg"]
                row_parts.append(f"{avg_time:>14.6f}s")
            else:
                row_parts.append(f"{'N/A':>14}")
        print(" | ".join(row_parts))

if __name__ == "__main__":
    main()