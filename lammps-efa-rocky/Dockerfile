ARG tag=8
FROM ghcr.io/rse-ops/spack-rocky-libfabric:tag-${tag}

# Google cloud doesn't have EFA
# ENV FI_EFA_USE_DEVICE_RDMA=1
# ENV RDMAV_FORK_SAFE=1
ENV DEBIAN_FRONTEND=noninteractive

# Install time for timed commands
RUN dnf update -y && dnf install -y time && \
    dnf clean all && \
    ldconfig && \
    rm -rf /tmp/* /var/tmp/*

# install laamps
USER root
RUN git clone --depth 1 --branch stable_29Sep2021_update2 https://github.com/lammps/lammps.git /opt/lammps && \
    cd /opt/lammps && \
    mkdir build && \
    cd build && \
    . /etc/profile && \ 
    cmake ../cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -D PKG_REAXFF=yes -D BUILD_MPI=yes -D PKG_OPT=yes -D FFT=FFTW3 && \
    make && \
    make install

# We are running this as root for storage, so do not
# need to put examples elsewhere and change permissions
    
# Needed for ffmpeg
# dnf install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm
# dnf install -y https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-8.noarch.rpm
# dnf install -y ffmpeg

# install laamps

# The cmake prefix path is needed otherwise openmpi is not found
# cmake ../cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -D PKG_REAXFF=yes -D BUILD_MPI=yes -D PKG_OPT=yes -D FFT=FFTW3 -DCMAKE_PREFIX_PATH=/usr/lib64/openmpi
# Run from a node:
# cd /opt/lammps/examples/reaxff/HNS
# flux run -n 1 lmp -v x 1 -v y 1 -v z 1 -in in.reaxc.hns -nocite
