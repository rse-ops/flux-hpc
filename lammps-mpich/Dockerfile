ARG tag=mamba
FROM ghcr.io/rse-ops/flux-conda:${tag}
ENV DEBIAN_FRONTEND=noninteractive



USER root
WORKDIR /opt/
RUN apt-get update && \
    apt-get install -y fftw3-dev fftw3 pdsh libfabric-dev libfabric1

# install laamps
RUN git clone --depth 1 --branch stable_29Sep2021_update2 https://github.com/lammps/lammps.git /opt/lammps && \
    cd /opt/lammps && \
    mkdir build && \
    cd build && \
    . /etc/profile && \ 
    cmake ../cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DPKG_REAXFF=yes -DBUILD_MPI=yes -DPKG_OPT=yes -DFFT=FFTW3 -DCMAKE_PREFIX_PATH=/usr/lib/mpich -DCMAKE_PREFIX_PATH=/usr/lib/x86_64-linux-gnu && \
    make && \
    make install

# Create a home to put the examples in, and
# ensure lmp executable is on path for flux user
# And anyone can interact with lammps examples
RUN useradd -ms /bin/bash -u 1234 flux && \
    mv /opt/lammps/examples /home/flux/examples && \
    chown -R 1234 /home/flux/examples
    
WORKDIR /home/flux/examples/reaxff/HNS
