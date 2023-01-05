ARG ubuntu_version=20.04
FROM ghcr.io/rse-ops/spack-ubuntu-libfabric:ubuntu-${ubuntu_version} as builder

ARG build_jobs=6
ENV build_jobs=${build_jobs}

# These are needed for network
ENV FI_EFA_USE_DEVICE_RDMA=1
ENV RDMAV_FORK_SAFE=1
ENV DEBIAN_FRONTEND=noninteractive

# install laamps
USER root
RUN git clone --depth 1 --branch stable_29Sep2021_update2 https://github.com/lammps/lammps.git /opt/lammps && \
    cd /opt/lammps && \
    mkdir build && \
    cd build && \
    . /etc/profile && \ 
    cmake ../cmake -D PKG_REAXFF=yes -D BUILD_MPI=yes -D PKG_OPT=yes -D FFT=FFTW3 && \
    make -j ${build_jobs} && \
    make install

# Create a home to put the examples in, and
# ensure lmp executable is on path for flux user
# And anyone can interact with lammps examples
RUN mv /opt/lammps/examples /home/flux/examples && \
    chown -R 1234 /home/flux/examples && \
    cp /root/.local/bin/lmp /usr/local/bin/lmp
    
# Target this example
ENV PATH=/root/.local/bin:$PATH
WORKDIR /home/flux/examples/reaxff/HNS

