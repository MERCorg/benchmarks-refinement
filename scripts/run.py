import argparse
import os
import subprocess
import time
import shutil
import json

from merc import RunProcess

SCRIPT_PATH = os.path.dirname(__file__)

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

    # Set the toolset path
    ltscompare_bin = shutil.which("ltscompare", path=args.toolpath)
    if ltscompare_bin is None:
        raise FileNotFoundError("ltscompare not found in PATH")

    # Iterate over all files in the specified directory
    for directory in os.listdir(args.directory):
        directory = os.path.join(args.directory, directory)

        for _ in range(0, 5):
            print(f"Running experiments for {directory}")

            files = os.listdir(directory)
            impl_file = os.path.join(
                directory, [f for f in files if f.endswith("_impl.aut")][0]
            )
            spec_file = os.path.join(
                directory, [f for f in files if f.endswith("_spec.aut")][0]
            )

            # Execute the command
            result = {
                "directory": directory,
                "algorithm": "trace",
            }

            try:
                proc = RunProcess(
                    ltscompare_bin,
                    ["-v", "-ptrace", impl_file, spec_file],
                )
                result["time"] = proc.user_time
            except subprocess.TimeoutExpired:
                result["time"] = -1

            print(result)

            with open(args.result_file, "a", encoding="utf-8") as f:
                json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
