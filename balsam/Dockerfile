ARG tag=mamba
FROM ghcr.io/rse-ops/flux-conda:${tag}

ENV DEBIAN_FRONTEND=nonintercative
RUN apt-get update && apt-get install -y tzdata && \
    mamba install singularity && \
    mamba install -y numpy matplotlib scipy && \
    pip install balsam && \
    apt-get clean
