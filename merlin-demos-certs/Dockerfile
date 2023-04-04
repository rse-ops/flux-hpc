FROM ghcr.io/rse-ops/flux-conda:mamba

# docker compose build
# docker compose up -d
# docker exec -it <merlin container> bash
# command with flux: flux start --test-size=4
#                    merlin run feature_demo/feature_demo.yaml
#                    merlin run-workers feature_demo/feature_demo.yaml

# workdir: /workflow

USER root
RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    curl \
    redis \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libncurses5-dev \
    squashfs-tools \
    tzdata \
    wget \
    build-essential \
    libseccomp-dev \
    libglib2.0-dev \
    pkg-config \
    cryptsetup \
    runc \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Singularity
RUN export VERSION=1.18.2 OS=linux ARCH=amd64 && \
  wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \
  sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \
  rm go$VERSION.$OS-$ARCH.tar.gz && \
  export PATH=/usr/local/go/bin:$PATH && \
  export VERSION=3.11.0 && \
    wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-ce-${VERSION}.tar.gz && \
    tar -xzf singularity-ce-${VERSION}.tar.gz && \
    cd singularity-ce-${VERSION} && \
    ./mconfig && \
    make -C builddir && \
    sudo make -C builddir install
    
ENV PATH=/usr/local/go/bin:$PATH

# Wrappers to ensure we source the mamba environment!
USER fluxuser
WORKDIR /workflow
ENV PATH=$PATH:/home/fluxuser/.local/bin

# Merlin from pip doesn't have flux completely implemented
RUN git clone --depth 1 https://github.com/LLNL/merlin /tmp/merlin && \
    cd /tmp/merlin && \
    pip install .

# Generate the example in advance so we have it ready to go
# in the Flux Operator
RUN merlin config --broker redis && \
    rm /home/fluxuser/.merlin/app.yaml

# Install spellbuild
RUN git clone --depth 1 https://github.com/LLNL/merlin-spellbook /tmp/spellbook && \
    cd /tmp/spellbook && \
    pip install .

# Updated app yaml
COPY ./merlinu/app.yaml /home/fluxuser/.merlin/app.yaml
COPY ./merlinu/rabbit.pass /home/fluxuser/.merlin/rabbit.pass
COPY ./merlinu/cert_rabbitmq /cert_rabbitmq
COPY ./merlinu/cert_redis /cert_redis
# This will need to be copied to /workflow/flux/flux_par.yaml
# after running     merlin example flux_par
COPY ./merlinu/flux_par.yaml /workflow/flux_par.yaml

RUN sudo chown -R fluxuser /cert_redis/ && \
    sudo chown -R fluxuser /cert_rabbitmq/
    
# Entrypoint to keep container running!
ENTRYPOINT ["tail", "-f", "/dev/null"]
