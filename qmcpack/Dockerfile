ARG flux_restful_tag=latest
FROM ghcr.io/flux-framework/flux-k8s-nio-data as base
FROM ghcr.io/flux-framework/flux-restful-api:${flux_restful_tag}

# This has the data needed by the dummy workflow
COPY --from=base /NiO-fcc-supertwist111-supershift000-S8.h5 /NiO-fcc-supertwist111-supershift000-S8.h5
ARG qmcpack_version=3.16.0
ENV qmcpack_version=${qmcpack_version}

# docker build -t qmc .
# command: qmcpack NiO-fcc-S8-dmc-strongscale.xml
# workdir: /coral2/NiO/dmc-a32-e384-batched_driver-DU32/

USER root
WORKDIR /root
ENV DEBIAN_FRONTEND=nonintercative
RUN apt-get update && apt-get install -y build-essential \
    tar \
    autoconf \
    automake \
    make \
    wget \
    git \
    gcc \
    g++ \
    zip \
    libblas-dev \
    liblapack-dev \
    fftw3-dev fftw3 \
    libxml2 \
    libxml2-dev \
    hdf5-tools \
    libhdf5-dev \
    libboost-all-dev \
    && apt-get clean

RUN wget https://github.com/Kitware/CMake/releases/download/v3.26.0/cmake-3.26.0-linux-x86_64.sh && \
    chmod +x cmake-3.26.0-linux-x86_64.sh && \
    /bin/bash cmake-3.26.0-linux-x86_64.sh --prefix=/usr/local --skip-license

# Install QMCpack
RUN wget https://github.com/QMCPACK/qmcpack/archive/refs/tags/v${qmcpack_version}.tar.gz && \
    tar -zxvf v${qmcpack_version}.tar.gz && \
    cd qmcpack-${qmcpack_version}/build  && \
    cmake -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx -DENABLE_SOA=1 -DQMC_MIXED_PRECISION=1 .. && make;

RUN cp -R /root/qmcpack-${qmcpack_version}/build/bin/qmcpack /usr/local/bin && \
    mkdir -p /coral2/NiO

# This is for reference in case we need to run the ctest that helps in generating the run config for strong scaling experiment
#    && cmake -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx -DENABLE_SOA=1 -DQMC_MIXED_PRECISION=1 -DQMC_DATA=/coral2 .. && make;

ENV PATH=/root/qmcpack:$PATH
COPY ./NiO/nio_data.tgz /coral2/NiO/nio_data.tgz
RUN cd /coral2/NiO/ && tar -xzvf nio_data.tgz && \
   mv /NiO-fcc-supertwist111-supershift000-S8.h5 /coral2/NiO/
WORKDIR /code
