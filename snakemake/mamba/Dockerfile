ARG tag=mamba
FROM ghcr.io/rse-ops/flux-conda:${tag}
LABEL org.opencontainers.image.authors="@vsoch"

# Mamba + snakemake base for the Flux Operator
    
USER root
ENV LANG C.UTF-8
ENV SHELL /bin/bash

RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    wget curl bzip2 ca-certificates gnupg2 squashfs-tools git \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mamba install -c bioconda -c conda-forge snakemake snakemake-minimal && \
    mamba install -q -y -c conda-forge singularity && \
    conda config --set channel_priority strict && \
    conda clean --all -y && \
    which python && \
    pip install .[reports,messaging,google-cloud]

WORKDIR /workflow
