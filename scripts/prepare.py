# pylint: disable=missing-module-docstring
# pylint: disable=wrong-import-position

import argparse
import os
import shutil
from merc import MercLogger, RunProcess

SCRIPT_PATH = os.path.dirname(__file__)

def prepare(logger: MercLogger, toolpath: str, cases_path: str):
    """"Prepares the case specifications for benchmarking"""
    mcrl22lps = shutil.which("mcrl22lps", path=toolpath)
    if mcrl22lps is None:
        raise FileNotFoundError("mcrl22lps not found in")

    lps2lts = shutil.which("lps2lts", path=toolpath)
    if lps2lts is None:
        raise FileNotFoundError("lps2lts not found in")

    # Iterate over all files in the specified directory
    for directory in os.listdir(cases_path):
        if not os.path.isdir(os.path.join(cases_path, directory)) or "auts" in directory:
            continue

        for file in os.listdir(os.path.join(cases_path, directory)):
            if ".mcrl2" in file:
                name, _ = os.path.splitext(file)

                if f"{name}.aut" not in os.listdir(os.path.join(cases_path, directory)):
                    print(f"Converting {file} to {name}.aut")
                    mcrl2_file = os.path.join(cases_path, directory, file)
                    lps_file = os.path.join(cases_path, directory, f"{name}.lps")
                    aut_file = os.path.join(cases_path, directory, f"{name}.aut")

                    RunProcess(
                        mcrl22lps, ["-lregular2", "-n", "-v", mcrl2_file, lps_file],
                        read_stdout=logger.info,
                    )
                    RunProcess(lps2lts, ["-v", lps_file, aut_file],
                        read_stdout=logger.info
                    )

def main():
    # Parse some configuration options
    parser = argparse.ArgumentParser(
        prog="run.py",
        description="Prepares the examples specifications for testing",
        epilog="",
    )

    parser.add_argument("toolpath", action="store", type=str)
    parser.add_argument("cases", action="store", type=str)
    parser.add_argument("log", action="store", type=str)
    args = parser.parse_args()

    logger = MercLogger(args.log)

    # Prepare the examples for testing
    prepare(logger, args.toolpath, args.cases)


if __name__ == "__main__":
    main()
