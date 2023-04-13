ARG tag=mamba
FROM ghcr.io/rse-ops/flux-conda:${tag}

ENV DEBIAN_FRONTEND=nonintercative
RUN apt-get update && apt-get install -y tzdata && \
    mamba install singularity && \
    mamba install -y -c conda-forge fireworks numpy pandas pytest scikit-learn && \
    MPICC="mpicc -shared" pip install --no-cache-dir --no-binary=mpi4py mpi4py && \
    apt-get clean

