ARG flux_restful_tag=latest
FROM ghcr.io/flux-framework/flux-restful-api:${flux_restful_tag}

# docker build -t amg .
# amg -n %SIZE% %SIZE% %SIZE% -P %SIZE% %SIZE% %SIZE%" 
# command: ./amg -n 1 1 1 -P 1 1 1
# workdir: /opt/AMG/test


USER root
RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    build-essential \
    cmake \
    fftw3-dev fftw3 \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /opt
RUN git clone --single-branch --branch 1.2 https://github.com/LLNL/AMG.git && \
    cd AMG && \
    make -j
WORKDIR /code
