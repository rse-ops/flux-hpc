ARG tag=focal
FROM fluxrm/flux-sched:${tag}

ENV DEBIAN_FRONTEND=noninteractive

# su flux
# . /opt/ramble/share/ramble/setup-env.sh
# ramble workspace activate /home/flux/test_workspace/
# ramble workspace concretize
# ramble workspace setup
# ramble on

USER root
WORKDIR /opt/
RUN apt-get update && \
    apt-get install -y fftw3-dev fftw3 pdsh libfabric-dev libfabric-bin libfabric1 time

# install ramble and add example
RUN git clone -c feature.manyFiles=true https://github.com/GoogleCloudPlatform/ramble.git && \
    cd ramble && \
    pip install -r requirements.txt
ENV PATH=/opt/ramble/bin:$PATH
RUN ramble workspace create -d /home/flux/test_workspace -c /opt/ramble/examples/basic_hostname_config.yaml
RUN useradd -ms /bin/bash -u 1234 flux && \
    chown -R 1234 /home/flux/test_workspace && \
    echo ". /opt/ramble/share/ramble/setup-env.sh" >> /home/flux/.bashrc && \
    echo ". /opt/ramble/share/ramble/setup-env.sh" >> /home/flux/.profile
