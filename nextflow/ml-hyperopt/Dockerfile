ARG flux_restful_tag=latest
FROM ghcr.io/flux-framework/flux-restful-api:${flux_restful_tag}

# docker build -t nextflow .
# command: nextflow -c nextflow.config run main.nf -profile flux
# launcher: checked
# workdir: /workflow

USER root
RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    python3 \
    python3-pip \
    default-jdk \
    curl \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Wrappers to ensure we source the mamba environment!
RUN git clone --depth 1 https://github.com/nextflow-io/ml-hyperopt /workflow
WORKDIR /workflow

# This wraps the existing entrypoint
COPY ./setup.sh ./
RUN /bin/bash setup.sh

# Install nextflow from source (since Flux not in release yet)
RUN git clone --depth 1 https://github.com/nextflow-io/nextflow /nextflow && \
    cd /nextflow && \
    make compile && make pack && make install && \
    # This finishes getting some deps
    /nextflow/nextflow -h
COPY ./nextflow.config /workflow/nextflow.config
ENV PATH=/nextflow:$PATH    
# ENV NXF_VER=22.11.0-edge 
# This is probably cheating a bit :)
# instead of altering the entrypoint to active the environment!
ENV PATH=/root/micromamba/envs/nf/bin:$PATH
WORKDIR /code
