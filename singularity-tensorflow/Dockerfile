ARG tag=mamba
FROM ghcr.io/rse-ops/flux-conda:${tag}

ENV DEBIAN_FRONTEND=nonintercative
RUN apt-get update && apt-get install -y tzdata && \
    mamba install singularity tensorflow ipython && \
    apt-get clean
