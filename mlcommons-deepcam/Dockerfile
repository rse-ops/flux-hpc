ARG tag="21.12-py3"
FROM nvcr.io/nvidia/pytorch:${tag}
ARG commit=ca8af13c2b6996fe60622406b1c6826a3cd34a7c

# some requirements
RUN pip install h5py==3.2.1

#install mpi4py
RUN pip install mpi4py==3.0.3

#install mlperf logging
RUN pip install "git+https://github.com/mlperf/logging.git@501bbde47f005d67c6357da6e5c1931eab339f8e"

# core assets
RUN git clone https://github.com/mlcommons/hpc /tmp/hpc && \
    cd /tmp/hpc && \
    git checkout ${commit} && \
    cd ./deepcam && \
    mv ./src/deepCam /opt/deepCam && \
    mv ./src/utils /opt/utils

# additional folders for mapping data
RUN mkdir -p /data

