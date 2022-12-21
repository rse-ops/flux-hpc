FROM ghcr.io/rse-ops/flux-spack:ubuntu-20.04

# docker build -t clc .

RUN touch /etc/apt/apt.conf.d/99verify-peer.conf \
    && echo >>/etc/apt/apt.conf.d/99verify-peer.conf "Acquire { https::Verify-Peer false }"

WORKDIR /code
RUN cd /opt/spack-environment && \
    . spack/share/spack/setup-env.sh && \
    spack env activate . && \
    spack mirror add develop https://binaries.spack.io/releases/develop && \
    spack buildcache keys --install --trust && \ 
    git clone https://github.com/XiaohuaZhangLLNL/spack4atom /code/spack4atom && \
    rm spack.lock && \
    spack repo add /code/spack4atom && \
    spack repo list && \
    spack add hdf5+cxx && \
    spack add conveyorlc@master && \
    spack install
    
# Create conda environment with amber tools in /opt/conda
RUN /bin/bash -c "curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh > mambaforge.sh && \
    bash mambaforge.sh -b -p /opt/conda && \
    rm mambaforge.sh"
ENV PATH=$PATH:/opt/conda/bin
RUN mamba install -c bioconda ambertools && \   
    ln -s /opt/conda/dat/leap/cmd/oldff/leaprc.ff14SB /opt/conda/dat/leap/cmd/leaprc.ff14SB && \
    ln -s /opt/conda/dat/leap/cmd/oldff/leaprc.ff99SB /opt/conda/dat/leap/cmd/leaprc.ff99SB

# Update spack environment (and include ambertools)
RUN cd /opt/spack-environment && \
    . spack/share/spack/setup-env.sh && \
    rm /etc/profile.d/z10_spack_environment.sh && \
    spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh && \
    echo "export PATH=$PATH:/opt/conda/bin" >> /etc/profile.d/z10_spack_environment.sh

# Plop examples into /code
COPY ./examples /code/examples

# Install extra bits for restful server - ensure we install to same spack root
WORKDIR /code
RUN git clone --depth 1 https://github.com/flux-framework/flux-restful-api /code/flux-restful-api && \
    cd /code/flux-restful-api && \
    python -m pip install -r requirements.txt

# Tokens for development
ENV FLUX_USER=fluxuser
ENV FLUX_TOKEN=12345
ENV FLUX_REQUIRE_AUTH="true"

# Server level option flags
ENV FLUX_OPTION_FLAGS="-ompi=openmpi@5"

# No token required for development
EXPOSE 5000
WORKDIR /code/flux-restful-api
COPY ./scripts/ /code/scripts/
COPY ./examples /code/examples
ENTRYPOINT /bin/bash /code/scripts/entrypoint.sh
