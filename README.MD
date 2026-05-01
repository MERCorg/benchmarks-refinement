# Overview

The git repository should be initialized with the submodules, which can be done
by running:

```bash
git submodule update --init
```

Furthermore, for the mCRL2 toolset we disable preprocessing in the source code
since all of the examples are trivially divergence-preserving branching
bisimilar, and this can only be done in the source code. This can be done by
applying the provided patch to the mCRL2 source code:

```bash
cd mCRL2
git apply ../mcrl2.patch
```

Then the [Dockerfile](Dockerfile) can be used to build a Docker image with all
necessary dependencies and tools installed. To build the Docker image, run the
following command in the root directory of the repository:

```bash
docker build -t benchmarks-refinement .
```

This will create a Docker image named `benchmarks-refinement`. From this we can
create a container to run the scripts:

```bash
docker run -it --rm --mount type=bind,source=./results/,target=/root/results/ --mount type=bind,source=./cases/,target=/root/cases/ benchmarks-refinement
```

First the examples must be prepared by running the `prepare.py` script. This can be done with the following command inside the Docker container:

```bash
/root/.venv/bin/python3 /root/scripts/prepare.py /root/mCRL2/build/stage/bin/ /root/cases/ /root/results/prepare.log
```

Then we can run the experiments as follows:

```bash
/root/.venv/bin/python3 /root/scripts/run_mcrl2.py /root/mCRL2/build/stage/bin/ /root/cases/ /root/results/results_mcrl2.json
```

And a similar command to run the merc-lts experiments:

```bash
/root/.venv/bin/python3 /root/scripts/run.py /root/merc/target/release/ /root/cases/ /root/results/results_merc.json
```

Finally, the table can be created from the results with the following command (for either JSON file):

```bash
/root/.venv/bin/python3 /root/scripts/create_table.py /root/results/results_mcrl2.json
```