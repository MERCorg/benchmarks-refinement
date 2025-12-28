FROM ubuntu:24.04

# Install dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
# Dependencies for mCRL2
 build-essential \
 cmake \
 git \
 libboost-dev \
 python3 \
 python3-pip \
 python3-psutil \ 
 z3 \
# Requires to install Rust
 curl 
 
# Build mCRL2 from source
COPY ./mCRL2 /root/mCRL2/

# Configure build
RUN mkdir /root/mCRL2/build && cd /root/mCRL2/build && cmake . \
 -DCMAKE_BUILD_TYPE=RELEASE \
 -DMCRL2_ENABLE_GUI_TOOLS=OFF \
 -DMCRL2_PACKAGE_RELEASE=ON \
 /root/mCRL2

# Build the toolset and install it such that the tools are available on the PATH
ARG THREADS=8
RUN cd /root/mCRL2/build && make -j${THREADS} mcrl22lps lps2lts

# Install Rust for building ltsinfo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Build ltsinfo from source
COPY ./merc /root/merc/

ARG THREADS=8
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cd /root/ltsinfo/ \
    && cargo build --release --bin merc-lts -j${THREADS}

# Copy the cases into the container
COPY ./cases/ /root/cases/

COPY ./scripts/ /root/scripts/

# Run the script
RUN python3 /root/scripts/run.py --toolpath /root/mCRL2/build/stage/bin/