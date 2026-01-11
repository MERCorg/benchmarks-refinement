FROM ubuntu:24.04

# Install dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
# Dependencies for mCRL2
 build-essential \
 cmake \
 git \
 libboost-dev \
 # Requires to install Rust
 curl \
 # Required for the scripts
 python3 \
 python3-pip \
 python3-venv
 
# Build mCRL2 from source
COPY ./mCRL2 /root/mCRL2/

# Configure build
RUN mkdir /root/mCRL2/build && cd /root/mCRL2/build && cmake . \
 -DCMAKE_BUILD_TYPE=RELEASE \
 -DMCRL2_ENABLE_GUI_TOOLS=OFF \
 /root/mCRL2

# Build the toolset and install it such that the tools are available on the PATH
ARG THREADS=8
RUN cd /root/mCRL2/build && make -j${THREADS} mcrl22lps lps2lts

# Install Rust for building merc-lts
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Build merc-lts from source
COPY ./merc /root/merc/

ARG THREADS=8
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cd /root/merc/ \
    && cargo build --release --bin merc-lts -j${THREADS}

# Install merc-py module, and create a virtual environment
COPY merc-py /root/merc-py/

RUN python3 -m venv /root/.venv
RUN /root/.venv/bin/pip install /root/merc-py

# Copy the scripts
COPY ./scripts /root/scripts/