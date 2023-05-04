ARG tag=latest
FROM ghcr.io/flux-framework/flux-restful-api:${tag}

# docker build -t snakemake .
# command: snakemake --cores 1 --flux --jobs 1
# workdir: /workflow

USER root
RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    bwa \
    samtools \
    bcftools \
    curl \
    libbz2-dev \
    liblzma-dev \
    libcurl4-openssl-dev \
    libncurses5-dev \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Wrappers to ensure we source the mamba environment!
RUN git clone --depth 1 https://github.com/snakemake/snakemake-tutorial-data /workflow
WORKDIR /workflow

# Install everything to current python install (alongside Flux)
COPY ./Snakefile ./
RUN mkdir -p ./scripts && \
    python3 -m pip install --upgrade pip --ignore-installed && \
    python3 -m pip install snakemake --ignore-installed && \
    python3 -m pip install jinja2 && \
    python3 -m pip install matplotlib && \
    python3 -m pip install jinja2 && \
    python3 -m pip install graphviz && \
    python3 -m pip install pysam && \
    python3 -m pip install pygments
COPY ./scripts/plot-quals.py ./scripts/plot-quals.py

# Install deps to same snakemake environment
RUN pip install -r /code/requirements.txt && ln -s /usr/bin/python3 /usr/bin/python
WORKDIR /code
