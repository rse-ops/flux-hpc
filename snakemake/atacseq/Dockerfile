ARG tag=latest
FROM ghcr.io/flux-framework/flux-restful-api:${tag}

# docker build -t snakemake .
# command: snakemake --cores 1 --flux --jobs 1
# workdir: /workflow

USER root
RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    python3 \
    python3-pip \
    curl \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Wrappers to ensure we source the mamba environment!
RUN git clone --depth 1 https://github.com/snakemake/snakemake-tutorial-data /workflow
WORKDIR /workflow

# This wraps the existing entrypoint
COPY ./setup.sh ./Snakefile ./
RUN mkdir ./scripts && /bin/bash setup.sh
COPY ./scripts/plot-quals.py ./scripts/plot-quals.py

# This is probably cheating a bit :)
# instead of altering the entrypoint to active the environment!
ENV PATH=/opt/micromamba/envs/snakemake/bin:$PATH

# Install deps to same snakemake environment
RUN pip install -r /code/requirements.txt
WORKDIR /code
