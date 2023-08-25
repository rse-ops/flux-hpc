ARG tag="tag-8"
FROM ghcr.io/rse-ops/spack-mpich:${tag}

USER root
WORKDIR /opt/
RUN yum update -y && \
    yum install -y fftw3-devel fftw3

# install laamps alongside spack
RUN cd /opt/spack-environment && \
    . spack/share/spack/setup-env.sh && \
    git clone --depth 1 --branch stable_29Sep2021_update2 https://github.com/lammps/lammps.git /opt/lammps && \
    cd /opt/lammps && \
    mkdir build && \
    cd build && \
    . /etc/profile && \ 
    cmake ../cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DPKG_REAXFF=yes -DBUILD_MPI=yes -DPKG_OPT=yes -DFFT=FFTW3 -DCMAKE_PREFIX_PATH=/opt/view/lib -DCMAKE_PREFIX_PATH=/usr/lib/x86_64-linux-gnu && \
    make && \
    make install

# Ensure lmp executable is on path for flux user
# And anyone can interact with lammps examples
RUN mkdir -p /home/flux && \
    mv /opt/lammps/examples /home/flux/examples && \
    chown -R flux /home/flux/examples
    
WORKDIR /home/flux/examples/reaxff/HNS
