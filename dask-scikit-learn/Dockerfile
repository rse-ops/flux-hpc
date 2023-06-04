ARG tag=mamba
FROM ghcr.io/rse-ops/flux-conda:${tag}

ENV DEBIAN_FRONTEND=nonintercative
RUN apt-get update && apt-get install -y tzdata && \
    pip install scikit-learn numpy && \
    # Install my branch of dask distributed with flux integration
    pip install git+https://github.com/researchapps/dask-jobqueue.git@add/flux && \
    pip install dask-ml && \
    apt-get clean
