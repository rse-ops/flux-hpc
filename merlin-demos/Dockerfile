FROM ubuntu:latest

# docker compose build
# docker compose up -d
# docker exec -it <merlin container> bash
# command with flux: flux start --test-size=4
#                    merlin run feature_demo/feature_demo.yaml
#                    merlin run-workers feature_demo/feature_demo.yaml

# workdir: /workflow

RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    curl \
    redis \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libncurses5-dev \
    python3-pip \
    git \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Wrappers to ensure we source the mamba environment!
WORKDIR /workflow

# Merlin from pip doesn't have flux completely implemented
RUN git clone --depth 1 https://github.com/LLNL/merlin /tmp/merlin && \
    cd /tmp/merlin && \
    pip install .

RUN merlin config --broker redis && \
    rm /root/.merlin/app.yaml

# Install spellbuild
RUN git clone --depth 1 https://github.com/LLNL/merlin-spellbook /tmp/spellbook && \
    cd /tmp/spellbook && \
    pip install .

# Updated app yaml
COPY ./merlinu/app.yaml /root/.merlin/app.yaml
COPY ./merlinu/rabbit.pass /root/.merlin/rabbit.pass

# Entrypoint to keep container running!
ENTRYPOINT ["tail", "-f", "/dev/null"]
