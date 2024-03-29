ARG tag=focal
FROM fluxrm/flux-sched:${tag}

# docker build --build-arg tag=focal -t ghcr.io/rse-ops/lammps-mpi:focal .
# Potential entrypoint:
#    mpirun -x PATH -np 2 --map-by socket lmp -v x 2 -v y 2 -v z 2 -in in.reaxc.hns -nocite
# To run with flux
#    flux start --test-size=4 
#    flux submit lmp -v x 1 -v y 1 -v z 1 -in in.reaxc.hns -nocite
#    flux job attach <outid>
#    flux run lmp -v x 1 -v y 1 -v z 1 -in in.reaxc.hns -nocite

ENV DEBIAN_FRONTEND=noninteractive

# It's good to be root :)
USER root
WORKDIR /opt/
RUN apt-get update && \
    apt-get install -y fftw3-dev fftw3 pdsh libfabric-dev libfabric-bin libfabric1

# install laamps
RUN git clone --depth 1 --branch stable_29Sep2021_update2 https://github.com/lammps/lammps.git /opt/lammps && \
    cd /opt/lammps && \
    mkdir build && \
    cd build && \
    . /etc/profile && \ 
    cmake ../cmake -D PKG_REAXFF=yes -D BUILD_MPI=yes -D PKG_OPT=yes -D FFT=FFTW3 && \
    make && \
    make install

# Create a home to put the examples in, and
# ensure lmp executable is on path for flux user
# And anyone can interact with lammps examples
RUN useradd -ms /bin/bash -u 1234 flux && \
    mv /opt/lammps/examples /home/flux/examples && \
    chown -R 1234 /home/flux/examples && \
    cp /root/.local/bin/lmp /usr/local/bin/lmp
    
# Target this example
ENV PATH=/root/.local/bin:$PATH
WORKDIR /home/flux/examples/reaxff/HNS
