import argparse
import os
import subprocess
import time
import shutil
import json

SCRIPT_PATH=os.path.dirname(__file__)

def prepare(toolpath):
    
    mcrl22lps = shutil.which("mcrl22lps", toolpath)
    if mcrl22lps is None:
        raise FileNotFoundError("mcrl22lps not found in PATH")

    lps2lts = shutil.which("lps2lts", toolpath)
    if lps2lts is None:
        raise FileNotFoundError("lps2lts not found in PATH")

    # Iterate over all files in the specified directory
    for directory in os.listdir(SCRIPT_PATH):
        if not os.path.isdir(directory) or "auts" in directory:
            continue

        for file in os.listdir(directory):
            if ".mcrl2" in file:
                name, _ = os.path.splitext(file)

                if f"{name}.aut" not in os.listdir(directory):
                    print(f"Converting {file} to {name}.aut")
                    mcrl2_file = os.path.join(SCRIPT_PATH, directory, file)
                    lps_file = os.path.join(SCRIPT_PATH, directory, f"{name}.lps")
                    aut_file = os.path.join(SCRIPT_PATH, directory, f"{name}.aut")

                    subprocess.run([mcrl22lps, "-lregular2", "-n", "-v", mcrl2_file, lps_file], check=True)
                    subprocess.run([lps2lts, "-v", lps_file, aut_file], check=True)

def main():
    # Parse some configuration options
    parser = argparse.ArgumentParser(
        prog="run_examples.py",
        description="Prepares the examples specifications for testing",
        epilog="",
    )

    parser.add_argument(
        "FILE", action="store", type=str
    )
    parser.add_argument(
        "-t", "--toolpath", action="store", type=str, required=True
    )
    args = parser.parse_args()

    # Prepare the examples for testing
    prepare(args.toolpath)

    # Set the toolset path
    ltscompare_bin = shutil.which("ltscompare", args.toolpath)
    if ltscompare_bin is None:
        raise FileNotFoundError("ltscompare not found in PATH")
    
    timeout = shutil.which("timeout", args.toolpath)
    if timeout is None:
        raise FileNotFoundError("timeout not found in PATH")

    # Iterate over all files in the specified directory
    results = {
        "timeout": "10m",
    }

    for i in range(0, 5):
        for directory in os.listdir(SCRIPT_PATH):
            if not os.path.isdir(directory) or "auts" in directory:
                continue

            print(f"Running experiments for {directory}")

            files = os.listdir(directory)
            impl_file = os.path.join(directory, [f for f in files if f.endswith('_impl.aut')][0])
            spec_file = os.path.join(directory, [f for f in files if f.endswith('_spec.aut')][0])
            
            # Execute the command
            start_time = time.time()
            result = subprocess.run([timeout, "10m", ltscompare_bin, "-d", "-pimpossible-futures", impl_file, spec_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            end_time = time.time()

            if result.returncode is not None and result.returncode == 124:
                print(f"Timeout for {directory}")
                results[directory] = {
                    "stdout": result.stdout.decode(),
                    "stderr": result.stderr.decode(),
                    "time": "-1",	
                }
            else:
                # Add the results
                results[directory] = {
                    "stdout": result.stdout.decode(),
                    "stderr": result.stderr.decode(),
                    "time": end_time - start_time,	
                }
            print(results[directory])

        with open(f"{args.FILE}_{i}.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()