FROM ghcr.io/rse-ops/flux-spack:ubuntu-20.04

# docker build -t test .
# docker run -it test
# cd libexec/osu-micro-benchmarks/mpi/one-sided/
# flux start --test-size=4
# flux mini run -ompi=openmpi@5 -n 2 ./osu_get_latency

# Prepare tutorial per
# https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/mpi/OSU_MicroBenchmarks/

RUN git clone --depth 1 https://github.com/ULHPC/tutorials /opt/tutorials && \
    mkdir -p /opt/osu-benchmark && \
    cd /opt/osu-benchmark && \
    ln -s /opt/tutorials/parallel/mpi/OSU_MicroBenchmarks ref.d && \
    ln -s ref.d/Makefile . && \
    ln -s ref.d/scripts  . && \
    mkdir src && \
    cd src && \
    export OSU_VERSION=5.8 && \
    wget --no-check-certificate http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-${OSU_VERSION}.tgz && \
    tar xf osu-micro-benchmarks-${OSU_VERSION}.tgz && \
    cd /opt/osu-benchmark && \
    # Compile based on openmpi
    mkdir -p build.openmpi && cd build.openmpi && \
    cd /opt/spack-environment && \
    . spack/share/spack/setup-env.sh && \
    spack env activate . && \
    cd - && \
    ../src/osu-micro-benchmarks-${OSU_VERSION}/configure CC=mpicc CFLAGS=-I$(pwd)/../src/osu-micro-benchmarks-${OSU_VERSION}/util --prefix=$(pwd) && \
    make && make install


# This must be set to work (username / token set won't trigger it alone)
ARG use_auth
ARG user="fluxuser"
ARG token="12345"
ARG port="5000"
ARG host="0.0.0.0"

EXPOSE ${port}

WORKDIR /code
ENV FLUX_USER=${user}
ENV FLUX_TOKEN=${token}
ENV FLUX_REQUIRE_AUTH=${use_auth}
ENV PORT=${port}
ENV HOST=${host}

# Add the server
RUN . /etc/profile.d/z10_spack_environment.sh && \
    python -m ensurepip --upgrade && \
    git clone https://github.com/flux-framework/flux-restful-api /code && \
    cd /code && python -m pip install -r requirements.txt

# Important! The versions of flux with pmix won't work without this flag
# the flux-restful api added support via version 0.0.15 of the python client
ENV FLUX_OPTION_FLAGS="-ompi=openmpi@5"
COPY ./entrypoint.sh /code/entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]
