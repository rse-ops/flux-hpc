ARG tag=bionic
FROM ubuntu:${tag}
# docker build -t rse-ops/flux-conda:latest .

# This first section from src/test/docker/bionic/Dockerfile in flux-core
# https://github.com/flux-framework/flux-core/blob/master/src/test/docker/bionic/Dockerfile
RUN apt-get update && \
    apt-get -qq install -y --no-install-recommends \
        apt-utils && \
    rm -rf /var/lib/apt/lists/*

# Utilities
RUN apt-get update && \
    apt-get -qq install -y --no-install-recommends \
        locales \
        ca-certificates \
        curl \
        wget \
        man \
        git \
        flex \
        ssh \
        sudo \
        vim \
        luarocks \
        munge \
        lcov \
        ccache \
        lua5.2 \
        mpich \
        valgrind \
        jq && \
    rm -rf /var/lib/apt/lists/*

# Compilers, autotools
RUN apt-get update && \
    apt-get -qq install -y --no-install-recommends \
        build-essential \
        pkg-config \
        autotools-dev \
        libtool \
	libffi-dev \
        autoconf \
        automake \
        make \
        cmake \
        clang-6.0 \
        clang-tidy \
        gcc-8 \
        g++-8 && \
    rm -rf /var/lib/apt/lists/*

# Python - instead of a system python we install mamba
RUN /bin/bash -c "curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh > mambaforge.sh && \
    bash mambaforge.sh -b -p /opt/conda && \
    rm mambaforge.sh" && \
    export PATH=/opt/conda/bin:$PATH  && \
    pip install --upgrade --ignore-installed \
        "markupsafe==2.0.0" \
        coverage cffi ply six pyyaml "jsonschema>=2.6,<4.0" \
        sphinx sphinx-rtd-theme sphinxcontrib-spelling
ENV PATH=/opt/conda/bin:$PATH

# Other deps
RUN apt-get update && \
    apt-get -qq install -y --no-install-recommends \
        libsodium-dev \
        libzmq3-dev \
        libczmq-dev \
        libjansson-dev \
        libmunge-dev \
        libncursesw5-dev \
        liblua5.2-dev \
        liblz4-dev \
        libsqlite3-dev \
        uuid-dev \
        libhwloc-dev \
        libmpich-dev \
        libs3-dev \
        libevent-dev \
        libarchive-dev \
        libpam-dev && \
    rm -rf /var/lib/apt/lists/*

# Testing utils and libs
RUN apt-get update && \
    apt-get -qq install -y --no-install-recommends \
        faketime \
        libfaketime \
        pylint \
        cppcheck \
        enchant \
        aspell \
        aspell-en && \
    rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

# NOTE: luaposix installed by rocks due to Ubuntu bug: #1752082 https://bugs.launchpad.net/ubuntu/+source/lua-posix/+bug/1752082
RUN luarocks install luaposix

# Install caliper by hand for now
WORKDIR /opt/caliper
RUN wget -O - https://github.com/LLNL/Caliper/archive/v1.7.0.tar.gz | tar xvz --strip-components 1 && \
    mkdir build && \
    cd build && \
    CC=gcc CXX=g++ cmake .. -DCMAKE_INSTALL_PREFIX=/usr && \
    make -j 4 && \
    make install && \
    cd ../.. && \
    rm -rf caliper

# Install openpmix, prrte
WORKDIR /opt/prrte
RUN git clone https://github.com/openpmix/openpmix.git && \
    git clone https://github.com/openpmix/prrte.git && \
    ls -l && \
    set -x && \
    cd openpmix && \
    git checkout fefaed568f33bf86f28afb6e45237f1ec5e4de93 && \
    ./autogen.pl && \
    PYTHON=/opt/conda/bin/python ./configure --prefix=/usr --disable-static && make -j 4 install && \
    ldconfig && \
    cd .. && \
    cd prrte && \
    git checkout 477894f4720d822b15cab56eee7665107832921c && \
    ./autogen.pl && \
    PYTHON=/opt/conda/bin/python ./configure --prefix=/usr && make -j 4 install && \
    cd ../.. && \
    rm -rf prrte

ENV LANG=C.UTF-8

# This is from the docker check script (run interactively during a test)
# https://github.com/flux-framework/flux-core/blob/master/src/test/docker/checks/Dockerfile
ARG USER=fluxuser
ARG UID=1000
ARG GID=1000
ARG FLUX_SECURITY_VERSION=0.8.0

# Install flux-security by hand for now:
#
WORKDIR /opt
RUN CCACHE_DISABLE=1 && \
    V=$FLUX_SECURITY_VERSION && \
    PKG=flux-security-$V && \
    URL=https://github.com/flux-framework/flux-security/releases/download && \
    wget ${URL}/v${V}/${PKG}.tar.gz && \
    tar xvfz ${PKG}.tar.gz && \
    cd ${PKG} && \
    PYTHON=/opt/conda/bin/python ./configure --prefix=/usr --sysconfdir=/etc || cat config.log && \
    make -j 4 && \
    make install && \
    cd .. && \
    rm -rf flux-security-*


# Add configured user to image with sudo access:
#
RUN set -x && groupadd -g $UID $USER && \
    useradd -g $USER -u $UID -d /home/$USER -m $USER && \
    printf "$USER ALL= NOPASSWD: ALL\\n" >> /etc/sudoers

# Setup MUNGE directories & key
RUN mkdir -p /var/run/munge && \
    dd if=/dev/urandom bs=1 count=1024 > /etc/munge/munge.key && \
    chown -R munge /etc/munge/munge.key /var/run/munge && \
    chmod 600 /etc/munge/munge.key

# Build flux core
# This I added and copied how to build with caliper / flux security enabled
# https://github.com/flux-framework/flux-core/blob/master/src/test/docker/docker-run-checks.sh#L185-L191
RUN git clone -b flub https://github.com/garlick/flux-core && \
    cd flux-core && \
    git fetch && \
    ./autogen.sh && \
    PYTHON=/opt/conda/bin/python PYTHON_PREFIX=PYTHON_EXEC_PREFIX=/opt/conda/lib/python3.8/site-packages ./configure --prefix=/usr --sysconfdir=/etc \
        --with-systemdsystemunitdir=/etc/systemd/system \
        --localstatedir=/var \
        --with-flux-security \
        --enable-caliper && \
    make clean && \
    make && \
    sudo make install

# This is from the same src/test/docker/bionic/Dockerfile but in flux-sched
# Flux-sched deps
RUN sudo apt-get update
RUN sudo apt-get -qq install -y --no-install-recommends \
	libboost-graph-dev \
	libboost-system-dev \
	libboost-filesystem-dev \
	libboost-regex-dev \
	libyaml-cpp-dev \
	libedit-dev

ENV LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH

# Build Flux Sched	
# https://github.com/flux-framework/flux-sched/blob/master/src/test/docker/docker-run-checks.sh#L152-L158
RUN git clone --depth 1 https://github.com/flux-framework/flux-sched && \
    cd flux-sched && \
    ./autogen.sh && \
    PYTHON=/opt/conda/bin/python ./configure --prefix=/usr --sysconfdir=/etc \
       --with-systemdsystemunitdir=/etc/systemd/system \
       --localstatedir=/var \
       --with-flux-security \
       --enable-caliper && \
    make && \
    sudo make install && \
    ldconfig

RUN cp /opt/flux-sched/t/scripts/flux-tree* /usr/libexec/flux/cmd/
WORKDIR /opt/flux-core

# Don't forget to add the flux user!
RUN useradd -ms /bin/bash -u 1234 flux  
