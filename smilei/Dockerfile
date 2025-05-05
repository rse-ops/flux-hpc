ARG ubuntu_version=24.04
FROM ubuntu:$ubuntu_version

# docker build -t ghcr.io/rse-ops/smilei .
# https://smileipic.github.io/tutorials/basics.html
ENV OMP_SCHEDULE=dynamic
ENV OMP_PROC_BIND=true
RUN apt-get update && apt-get install -y git build-essential \
    openmpi-bin openmpi-doc libopenmpi-dev python3-dev cmake libattr1-dev libhdf5-mpi-dev python3-pip python3-numpy
RUN git clone https://github.com/SmileiPIC/Smilei /opt/smilei && \
    cd /opt/smilei && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    cp /usr/include/hdf5/openmpi/* /usr/include/ && \
    cp /usr/lib/x86_64-linux-gnu/hdf5/openmpi/* /usr/lib/ && \
    make -j 4  && cp smilei* /usr/bin/
