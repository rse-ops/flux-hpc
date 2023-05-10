ARG tag=mamba
FROM ghcr.io/rse-ops/flux-conda:${tag}

ENV DEBIAN_FRONTEND=nonintercative
RUN apt-get update && apt-get install -y tzdata && \
    mamba install -y scikit-learn && \
    pip install "ray[serve]" && \
    pip install "ray[default]" && \
    apt-get clean
    
