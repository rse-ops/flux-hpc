FROM ghcr.io/flux-framework/flux-k8s-nio-data as base   
FROM ubuntu:22.04 AS builder
ENV DEBIAN_FRONTEND=noninteractive
COPY --from=base /NiO-fcc-supertwist111-supershift000-S8.h5 /NiO-fcc-supertwist111-supershift000-S8.h5

# docker build -f Dockerfile.spack -t ghcr.io/rse-ops/qmcpack:flux .

RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install \
    autotools-dev \
    autoconf \
    automake \
    cmake \
    git \
    python3 \
    dnsutils \
    libatomic1 \
    libnuma-dev \
    libgomp1 \
    openssh-server \
    openssh-client \
    apt-utils \
    gcc \
    unzip \
    gfortran \
    g++ \
    build-essential \
    software-properties-common

RUN mkdir /opt/spack-environment \
    &&  (echo "spack:" \
    &&   echo "  specs:" \
    &&   echo "  - flux-sched" \
    &&   echo "  - flux-core" \
    &&   echo "  - pmix@4.2.2" \
    &&   echo "  - flux-pmix" \
    &&   echo "  - qmcpack" \
    &&   echo "  concretizer:" \
    &&	 echo "    unify: true" \
    &&   echo "  config:" \
    &&   echo "    install_tree: /opt/software" \
    &&   echo "  view: /opt/view") > /opt/spack-environment/spack.yaml
    
RUN cd /opt/spack-environment \
    && git clone --depth 1 --branch v0.22.1 https://github.com/spack/spack.git \
    && . spack/share/spack/setup-env.sh \
    && spack env activate . \
    && spack external find openssh \
    && spack external find cmake \
    && spack install --reuse --fail-fast \
    && spack gc -y

# Modifications to the environment that are necessary to run
RUN cd /opt/spack-environment \
    && . spack/share/spack/setup-env.sh \
    && spack env activate --sh -d . >> /etc/profile.d/z10_spack_environment.sh

WORKDIR /opt
EXPOSE 22

FROM ubuntu:22.04
COPY --from=base /NiO-fcc-supertwist111-supershift000-S8.h5 /NiO-fcc-supertwist111-supershift000-S8.h5
COPY --from=builder /opt/spack-environment /opt/spack-environment
COPY --from=builder /opt/software /opt/software
COPY --from=builder /opt/view /opt/view
COPY --from=builder /etc/profile.d/z10_spack_environment.sh /etc/profile.d/z10_spack_environment.sh

RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install --no-install-recommends \
    libatomic1 \
    libnuma-dev \
    libgomp1 \
    python3-dev \
    ca-certificates \
    openssh-server \
    openssh-client \
    dnsutils \
    curl \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
    
# Finally, install oras for saving artifacts
RUN export VERSION="1.2.0" && \
    curl -LO "https://github.com/oras-project/oras/releases/download/v${VERSION}/oras_${VERSION}_linux_amd64.tar.gz" && \
    mkdir -p oras-install/ && \
    tar -zxf oras_${VERSION}_*.tar.gz -C oras-install/ && \
    mv oras-install/oras /usr/local/bin/ && \
    rm -rf oras_${VERSION}_*.tar.gz oras-install/

COPY ./NiO/nio_data.tgz /coral2/NiO/nio_data.tgz
RUN cd /coral2/NiO/ && tar -xzvf nio_data.tgz && \
   mv /NiO-fcc-supertwist111-supershift000-S8.h5 /coral2/NiO/
