FROM ubuntu:20.04 as builder

# docker build -t test .
# docker run -it test
# cd libexec/osu-micro-benchmarks/mpi/one-sided/
# flux start --test-size=4
# flux mini run -ompi=openmpi@5 -n 2 ./osu_get_latency

ENV DEBIAN_FRONTEND=noninteractive
ARG spack_cpu_arch=x86_64
ARG build_jobs=6

RUN apt-get update && \
    apt-get -y install \
    build-essential \
    gfortran \
    autotools-dev \
    autoconf \
    automake \
    ca-certificates \
    cmake \
    git \
    curl \
    unzip \
    python3 \
    openssh-server \
    openssh-client \
    libnuma-dev \
    libgomp1 \
    fftw3-dev fftw3 \
    apt-utils \
    pdsh \
    sudo \
    dnsutils \
    wget \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# What we want to install and how we want to install it
# is specified in a manifest file (spack.yaml)
RUN mkdir /opt/spack-environment \
    &&  (echo "spack:" \
    &&   echo "  specs:" \
    &&   echo "  - openmpi@4.1.2 target=${spack_cpu_arch}" \
    &&   echo "  - flux-sched target=${spack_cpu_arch}" \
    &&   echo "  - flux-pmix target=${spack_cpu_arch}" \
    &&   echo "  - python target=${spack_cpu_arch}" \
    &&   echo "  concretizer:" \
    &&   echo "    unify: true" \
    &&   echo "  config:" \
    &&   echo "    install_tree: /opt/software" \
    &&   echo "  view: /opt/view") > /opt/spack-environment/spack.yaml

# Install the software, remove unnecessary deps
RUN cd /opt/spack-environment \
    && git clone --single-branch --branch v0.19.0 https://github.com/spack/spack.git \
    && . spack/share/spack/setup-env.sh \
    && spack env activate . \
    && spack external find openssh \
    && spack external find cmake \
    && spack install --reuse --fail-fast \
    && spack gc -y

# Strip all the binaries
RUN find -L /opt/view/* -type f -exec readlink -f '{}' \; | \
    xargs file -i | \
    grep 'charset=binary' | \
    grep 'x-executable\|x-archive\|x-sharedlib' | \
    awk -F: '{print $1}' | xargs strip -s

# Modifications to the environment that are necessary to run
RUN cd /opt/spack-environment \
    && . spack/share/spack/setup-env.sh \
    && spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh

ENV PATH=/opt/view/bin:$PATH

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

# The script below borks without this.
ENV SPACK_ROOT=/opt/spack-environment/spack

# This must be set to work (username / token set won't trigger it alone)
ARG use_auth
ARG user="fluxuser"
ARG token="12345"
ARG port="5000"
ARG host="0.0.0.0"

EXPOSE ${port}

# For easier Python development.
RUN . /etc/profile.d/z10_spack_environment.sh && \
    python -m ensurepip --upgrade && \
    git clone https://github.com/flux-framework/flux-restful-api /code && \
    cd /code && python -m pip install -r requirements.txt

WORKDIR /code
ENV FLUX_USER=${user}
ENV FLUX_TOKEN=${token}
ENV FLUX_REQUIRE_AUTH=${use_auth}
ENV PORT=${port}
ENV HOST=${host}

# Important! The versions of flux with pmix won't work without this flag
# the flux-restful api added support via version 0.0.15 of the python client
ENV FLUX_OPTION_FLAGS="-ompi=openmpi@5"
COPY ./entrypoint.sh /code/entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]

# This is dumping out the spack environment so the operator can use it
ENV SPACK_ENV=/opt/spack-environment;
ENV ACLOCAL_PATH=/opt/view/share/aclocal:/usr/share/aclocal;
ENV CMAKE_PREFIX_PATH=/opt/view;
ENV CPATH=/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/python-3.10.8-qh3hml3swbcfbaaqf2o4pxz4752mticr/include/python3.10;
ENV FLUX_CONNECTOR_PATH=/opt/view/lib/flux/connectors;
ENV FLUX_EXEC_PATH=/opt/view/libexec/flux/cmd;
ENV FLUX_MODULE_PATH=/opt/view/lib/flux/modules:/opt/view/lib/flux/modules/sched;
ENV FLUX_RC_EXTRA=/opt/view/etc/flux;
ENV FLUX_SHELL_RC_PATH=/opt/view/etc/flux/shell/lua.d;
ENV LUA_CPATH='/opt/view/lib/lua/5.3/?.so;/opt/view/lib/lua/5.3/?.so;/opt/view/lib/lua/5.3/?.so';
ENV LUA_PATH='/opt/view/lib/lua/5.3/?/init.lua;/opt/view/lib/lua/5.3/?.lua;/opt/view/share/lua/5.3/?/init.lua;/opt/view/share/lua/5.3/?.lua;/opt/view/share/lua/5.3/?.lua;/opt/view/share/lua/5.3/?.lua';
ENV MANPATH=/opt/view/share/man:/opt/view/man:/usr/share/man:;
ENV MPICC=/opt/view/bin/mpicc;
ENV MPICXX=/opt/view/bin/mpic++;
ENV MPIF77=/opt/view/bin/mpif77;
ENV MPIF90=/opt/view/bin/mpif90;
ENV PATH=/opt/view/bin:/opt/spack-environment/spack/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin;
ENV PKG_CONFIG_PATH=/opt/view/lib/pkgconfig:/usr/share/pkgconfig:/opt/view/share/pkgconfig:/opt/view/lib64/pkgconfig;
ENV PYTHONPATH=/opt/view/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-pyrsistent-0.18.1-4y45yicct333hekudm6spwmfo4zurvir/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-attrs-22.1.0-6l7qhin5aaqyev56skpsvruxox2ywn3s/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-pycparser-2.21-7seqp6a5ivvr4t3xygon2ttiyh55bbm6/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-pyyaml-6.0-ayf2ig4btgiev7ir675l7oywhvgl7rhs/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-jsonschema-4.16.0-6zl5yjunrcsn4zpywynn5oph32iqlvou/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-cffi-1.15.0-gyk2my27jc3b5gno4zcqtm3riumyl4vp/lib/python3.10/site-packages;

# Just for demo!
ENV FLUX_REQUIRE_AUTH="true"
