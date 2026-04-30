import argparse
import os
import subprocess
import time
import shutil
import json

from merc import RunProcess

SCRIPT_PATH = os.path.dirname(__file__)


def run_benchmark(tool_name, command_args_fn, toolpath, directory, result_file, algorithm="trace-ac", num_runs=5):
    """
    Generic function to run benchmarks on test cases.
    
    Args:
        tool_name: Name of the binary tool to use
        command_args_fn: Function that takes (impl_file, spec_file) and returns command arguments list
        toolpath: Path to search for the tool binary
        directory: Directory containing test cases
        result_file: File to write results to
        algorithm: Name of the algorithm/preorder being benchmarked
        num_runs: Number of times to run each test (default: 5)
    """
    # Set the toolset path
    tool_bin = shutil.which(tool_name, path=toolpath)
    if tool_bin is None:
        raise FileNotFoundError(f"{tool_name} not found in PATH")

    # Iterate over all files in the specified directory
    for subdir in os.listdir(directory):
        subdir = os.path.join(directory, subdir)

        for _ in range(0, num_runs):
            print(f"Running experiments for {subdir}")

            files = os.listdir(subdir)
            impl_file = os.path.join(
                subdir, [f for f in files if f.endswith("_impl.aut")][0]
            )
            spec_file = os.path.join(
                subdir, [f for f in files if f.endswith("_spec.aut")][0]
            )

            # Execute the command
            result = {
                "directory": subdir,
                "algorithm": algorithm,
            }

            try:
                command_args = command_args_fn(impl_file, spec_file)
                proc = RunProcess(tool_bin, command_args)
                result["time"] = proc.user_time
            except subprocess.TimeoutExpired:
                result["time"] = -1

            print(result)

            with open(result_file, "a", encoding="utf-8") as f:
                json.dump(result, f)
                f.write("\n")


def main():
    # Parse some configuration options
    parser = argparse.ArgumentParser(
        prog="run.py",
        description="Prepares the examples specifications for testing",
        epilog="",
    )

    parser.add_argument("toolpath", action="store", type=str)
    parser.add_argument("directory", action="store", type=str)
    parser.add_argument("result_file", action="store", type=str)
    args = parser.parse_args()

    # Run merc-lts with each preorder
    preorders = ["trace", "weaktrace", "stable-failures", "failures-divergences", "impossible-futures"]
    for preorder in preorders:
        def merc_command_args(impl_file, spec_file, p=preorder):
            return ["refines", p, impl_file, spec_file, "--no-preprocess", "--format=aut-mcrl2"]

        run_benchmark("merc-lts", merc_command_args, args.toolpath, args.directory, args.result_file, algorithm=preorder)


if __name__ == "__main__":
    main()
