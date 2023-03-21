FROM ghcr.io/rse-ops/flux-conda:mamba

# docker build -t demo .
# docker exec -it demo bash
# command with flux: flux start --test-size=4
#                    cd /workflow/Laghos 
#                    make tests
#                    flux run make tests

# workdir: /workflow

USER root
RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    libbz2-dev \
    liblzma-dev \
    libncurses5-dev \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV MAKE_CXX_FLAG="MPICXX=mpic++"

# Wrappers to ensure we source the mamba environment!
WORKDIR /workflow

# Install hypre
RUN export hypre_options="--disable-fortran --enable-bigint" && \
    wget --no-verbose https://github.com/hypre-space/hypre/archive/v2.11.2.tar.gz && \
    tar -xzf v2.11.2.tar.gz && \
    mv hypre-2.11.2 hypre && \
    cd hypre/src && \
   ./configure ${hypre_options} CC=mpicc CXX=mpic++ && \
    make -j3

# Metis
RUN wget --no-verbose http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/OLD/metis-4.0.3.tar.gz && \
    tar -xzf metis-4.0.3.tar.gz && \
    mv metis-4.0.3 metis-4.0 && \
    make -j3 -C metis-4.0/Lib CC=mpicc OPTFLAGS="-Wno-error=implicit-function-declaration -O2"

RUN git clone --single-branch --depth 1 https://github.com/mfem/mfem && \
    unset LD_LIBRARY_PATH && \
    cd mfem && \
    make config MFEM_USE_MPI=YES MPICXX=mpiCC MFEM_MPI_NP=2 MFEM_DEBUG=${DEBUG} CPPFLAGS="${CPPFLAGS}" && \
    make
       
# And laghos! Laaaaggghhooooos sounds like lakes
RUN git clone --depth 1 https://github.com/CEED/Laghos && \
    cd Laghos && \ 
    make
