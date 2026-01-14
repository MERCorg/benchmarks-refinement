# Overview

The git repository should be initialized with the submodules, which can be done by running:

```bash
git submodule update --init
```

Then the [Dockerfile](Dockerfile) can be used to build a Docker image with all necessary dependencies and tools installed. To build the Docker image, run the following command in the root directory of the repository:

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
/root/.venv/bin/python3 /root/scripts/run.py /root/mCRL2/build/stage/bin/ /root/cases/ /root/results/results.json
```