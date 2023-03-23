ARG tag=mamba
FROM ghcr.io/rse-ops/flux-conda:${tag}

# docker build -t demo .
# docker exec -it demo bash
# command with flux: flux start --test-size=4

# workdir: /workflow

USER root
RUN apt-get update

# Wrappers to ensure we source the mamba environment!
WORKDIR /workflow

# Install maestro
RUN git clone --depth 1 -b bugfix/flux_adapter_pickling https://github.com/jwhite242/maestrowf /tmp/m && \
    cd /tmp/m && \
    pip install . && \
    mkdir -p /run/flux  
    
COPY ./study /workflow/study
