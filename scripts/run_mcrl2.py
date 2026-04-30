import argparse
from run import run_benchmark

SCRIPT_PATH = __file__


def main():
    # Parse some configuration options
    parser = argparse.ArgumentParser(
        prog="run_mcrl2.py",
        description="Prepares the examples specifications for testing",
        epilog="",
    )

    parser.add_argument("toolpath", action="store", type=str)
    parser.add_argument("directory", action="store", type=str)
    parser.add_argument("result_file", action="store", type=str)
    args = parser.parse_args()

    preorders = ["trace-ac", "weak-trace-ac", "weak-failures", "failures-divergence", "impossible-futures"]

    for preorder in preorders:
        def ltscompare_command_args(impl_file, spec_file, p=preorder):
            return ["-v", f"-p{p}", impl_file, spec_file]

        run_benchmark(
            "ltscompare",
            ltscompare_command_args,
            args.toolpath,
            args.directory,
            args.result_file,
            algorithm=preorder,
        )


if __name__ == "__main__":
    main()
