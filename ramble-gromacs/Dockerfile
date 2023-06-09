ARG tag=focal
FROM fluxrm/flux-sched:${tag}

ENV DEBIAN_FRONTEND=noninteractive

# su flux
# flux start --test-size=4
# . /home/flux/ramble/share/ramble/setup-env.sh
# ramble workspace activate /home/flux/gromacs_workspace/
# ramble workspace concretize # (might already be done)
# ramble workspace setup # (requires spack in path, already done in build)
# ramble on

# Ensure the flux user owns the spack install
USER root
RUN useradd -ms /bin/bash -u 1234 flux && \
    chown -R 1234 /home/flux && \
    apt-get update && \
    apt-get install -y fftw3-dev fftw3 pdsh libfabric-dev libfabric-bin libfabric1 time

USER flux
WORKDIR /home/flux
RUN git clone --depth 1 https://github.com/spack/spack && \
    git clone -c feature.manyFiles=true https://github.com/GoogleCloudPlatform/ramble.git && \
    cd ramble && \
    pip install -r requirements.txt
COPY ./flux_gromacs.yaml /home/flux/ramble/examples/flux_gromacs.yaml
ENV PATH=/home/flux/ramble/bin:/home/flux/spack/bin:$PATH
RUN ramble workspace create -d /home/flux/test_workspace -c /home/flux/ramble/examples/basic_hostname_config.yaml && \
    ramble workspace create -d /home/flux/gromacs_workspace -c /home/flux/ramble/examples/flux_gromacs.yaml
    
WORKDIR /home/flux/gromacs_workspace
RUN . /home/flux/ramble/share/ramble/setup-env.sh && \
    ramble workspace activate /home/flux/gromacs_workspace/ && \
    ramble workspace concretize && \
    ramble workspace setup

# Allow setup for Flux operator
USER root
