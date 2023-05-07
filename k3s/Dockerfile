ARG tag=focal
FROM ubuntu:${tag}
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# See https://github.com/k3s-io/k3s/blob/master/package/Dockerfile
# We needed k3s in ubuntu with flux
# docker build -t test .

# Dependencies for environment
RUN apt-get update && apt-get install -y ca-certificates \
    tar zstd wget tzdata libseccomp-dev curl git \
    gcc pkg-config build-essential \
    # This is needed for building k3s
    libbtrfs-dev btrfs-progs \
    software-properties-common && \
    add-apt-repository --yes ppa:rmescandon/yq && \
    apt-get update && \
    apt-get install yq -y

# Install Go (this version is checked in ./validate)
RUN wget https://go.dev/dl/go1.20.3.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.20.3.linux-amd64.tar.gz  

# This builds k3s
WORKDIR /src
RUN git clone --depth 1 https://github.com/k3s-io/k3s && \
    cd k3s && \
    git checkout b32bf495417b7d9f66604b83dca4e2f01f33bc8c && \
    export PATH=/usr/local/go/bin:$PATH && \
    pushd ./scripts && \
    ./download && \
    ./validate && \
    ./build && \
    # Remove line that tries to upload to s3
    sed -i '$ d' ./package-cli && \
    ./package-cli && \
    popd

# Move into bins and uninstall go and finalize stuffs
RUN mkdir -p /lib/modules /lib/firmware && \
    mv bin/* /usr/local/bin && \
    mv dist/artifacts/k3s /usr/local/bin && \
    rm -rf /usr/local/go && \
    echo 'hosts: files dns' > /etc/nsswitch.conf && \
    echo "PRETTY_NAME=\"K3s develop\"" > /etc/os-release && \
    chmod 1777 /tmp

VOLUME /var/lib/kubelet
VOLUME /var/lib/rancher/k3s
VOLUME /var/lib/cni
VOLUME /var/log
ENV PATH="$PATH:/usr/local/bin/aux"
ENV CRI_CONFIG_FILE="/var/lib/rancher/k3s/agent/etc/crictl.yaml"

ENV PATH=/opt/conda/bin:$PATH
ENV LANG=C.UTF-8

# This first section from src/test/docker/bionic/Dockerfile in flux-core
# https://github.com/flux-framework/flux-core/blob/master/src/test/docker/bionic/Dockerfile
RUN apt-get update && \
    apt-get -qq install -y --no-install-recommends \
        apt-utils && \
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
# Compilers, autotools
    apt-get update && \
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
        g++-8

# Python - instead of a system python we install mamba
RUN /bin/bash -c "curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh > mambaforge.sh && \
    bash mambaforge.sh -b -p /opt/conda && \
    rm mambaforge.sh" && \
    export PATH=/opt/conda/bin:$PATH  && \
    pip install --upgrade --ignore-installed \
        "markupsafe==2.0.0" \
        coverage cffi ply six pyyaml "jsonschema>=2.6,<4.0" \
        sphinx sphinx-rtd-theme sphinxcontrib-spelling

# Other deps
RUN apt-get -qq install -y --no-install-recommends \
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
# Testing utils and libs
    apt-get -qq install -y --no-install-recommends \
        faketime \
        libfaketime \
        pylint \
        cppcheck \
        enchant \
        aspell \
        aspell-en && \
    locale-gen en_US.UTF-8 && \
    # NOTE: luaposix installed by rocks due to Ubuntu bug: #1752082 https://bugs.launchpad.net/ubuntu/+source/lua-posix/+bug/1752082
    luarocks install luaposix
    
# Install caliper by hand for now
RUN mkdir -p /opt/caliper && \
    cd /opt/caliper && \
    wget -O - https://github.com/LLNL/Caliper/archive/v1.7.0.tar.gz | tar xvz --strip-components 1 && \
    mkdir build && \
    cd build && \
    CC=gcc CXX=g++ cmake .. -DCMAKE_INSTALL_PREFIX=/usr && \
    make -j 4 && \
    make install && \
    cd ../.. && \
    rm -rf caliper

# Install openpmix, prrte
RUN mkdir -p /opt/prrte && cd /opt/prrte && \
    git clone https://github.com/openpmix/openpmix.git && \
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

# Manually create the fluxuser
RUN useradd -u 1000 -d /home/fluxuser -m fluxuser && \
    printf "fluxuser ALL= NOPASSWD: ALL\\n" >> /etc/sudoers && \
    export FLUX_SECURITY_VERSION=0.8.0 && \
    cd /opt && \
    CCACHE_DISABLE=1 && \
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
    rm -rf flux-security-* && \
# Add configured user to image with sudo access:
    set -x && \
# Setup MUNGE directories & key
    mkdir -p /var/run/munge && \
    dd if=/dev/urandom bs=1 count=1024 > /etc/munge/munge.key && \
    chown -R munge /etc/munge/munge.key /var/run/munge && \
    chmod 600 /etc/munge/munge.key

# Build flux core
# This I added and copied how to build with caliper / flux security enabled
# https://github.com/flux-framework/flux-core/blob/master/src/test/docker/docker-run-checks.sh#L185-L191
RUN git clone --depth 1 -b disable-sign-id-check https://github.com/researchapps/flux-core && \
    cd flux-core && \
    ./autogen.sh && \
    PYTHON=/opt/conda/bin/python PYTHON_PREFIX=PYTHON_EXEC_PREFIX=/opt/conda/lib/python3.8/site-packages ./configure --prefix=/usr --sysconfdir=/etc \
        --with-systemdsystemunitdir=/etc/systemd/system \
        --localstatedir=/var \
        --with-flux-security \
        --enable-caliper && \
    make clean && \
    make && \
    make install

# This is from the same src/test/docker/bionic/Dockerfile but in flux-sched
# Flux-sched
RUN apt-get -qq install -y --no-install-recommends \
	libboost-graph-dev \
	libboost-system-dev \
	libboost-filesystem-dev \
	libboost-regex-dev \
	libyaml-cpp-dev \
	libedit-dev && \
    export LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH && \
# https://github.com/flux-framework/flux-sched/blob/master/src/test/docker/docker-run-checks.sh#L152-L158
    git clone --depth 1 https://github.com/flux-framework/flux-sched && \
    cd flux-sched && \
    ./autogen.sh && \
    PYTHON=/opt/conda/bin/python ./configure --prefix=/usr --sysconfdir=/etc \
       --with-systemdsystemunitdir=/etc/systemd/system \
       --localstatedir=/var \
       --with-flux-security \
       --enable-caliper && \
    make && \
    sudo make install && \
    ldconfig && \
    rm -rf /var/lib/apt/lists/*
