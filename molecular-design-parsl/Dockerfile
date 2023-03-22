ARG tag=mamba
FROM ghcr.io/rse-ops/flux-conda:${tag}

# docker build -t mdparsl .
# docker run -it mdparsl --rm --name mdparsl
# command with flux: flux start --test-size=4
#                    conda activate /opt/conda/envs/moldesign-demo/
#                    python3 ./scripts/0_molecular-design-with-parsl.py

# Then to copy over data... mkdir -p ./data && cd ./data
# docker cp ecstatic_wiles:/workflow/training-data-vs-time.svg .
# docker cp ecstatic_wiles:/workflow/parsl-results.csv .

# workdir: /workflow

USER root
RUN apt-get update --fix-missing
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
RUN git clone --depth 1 https://github.com/ExaWorks/molecular-design-parsl-demo /workflow
WORKDIR /workflow
COPY ./environment.yml ./environment.yml
RUN mamba env create --file environment.yml && mamba init
RUN conda init --system
COPY ./scripts ./scripts
COPY ./data ./data
