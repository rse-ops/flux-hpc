ARG ubuntu_version=20.04
FROM ghcr.io/rse-ops/flux-spack:ubuntu-${ubuntu_version}

RUN touch /etc/apt/apt.conf.d/99verify-peer.conf \
    && echo >>/etc/apt/apt.conf.d/99verify-peer.conf "Acquire { https::Verify-Peer false }"

ENV USER=root
ENV EDITOR=vim
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/home/flux/.nix-profile/bin:$PATH

RUN apt-get update && \
    apt-get install -y \
        ca-certificates \
        bash-completion \
        build-essential \
        curl \
        cmake \
        gnupg \
        htop \
        jq \
        less \
        lsb-release \
        lsof \
        man-db \
        nano \
        ssl-cert \
        sudo \
        unzip \
        xz-utils \
        dnsutils \
        iputils-ping \
        zip

# https://nixos.org/manual/nix/stable/installation/multi-user.html
WORKDIR /code/scripts
COPY ./scripts/init-home.sh /code/scripts/init-home.sh
COPY ./nix/config.nix /home/flux/.config/nixpkgs/config.nix
COPY ./nix/flake.nix /code/nix/flake.nix
RUN /bin/bash -c "sh <(curl -L https://nixos.org/nix/install) --daemon" && \
    /bin/bash /code/scripts/init-home.sh /home/flux && \
    /bin/bash /code/scripts/init-home.sh /root

# Install cachix (binary cache)
RUN . /root/.nix-profile/etc/profile.d/nix.sh && \
    nix-env -iA cachix -f https://cachix.org/api/v1/install && \
    cachix use rseops

COPY ./environment.yaml /code/environment.yaml
WORKDIR /code/nix

# The flake.nix defines our development shell
RUN . /root/.nix-profile/etc/profile.d/nix.sh && \
    nix develop -c micromamba create --prefix /home/flux/mamba -f /code/environment.yaml

# Install extra bits for restful server - ensure we install to same spack root
WORKDIR /code
RUN . /etc/profile.d/z10_spack_environment.sh && \
    git clone --depth 1 https://github.com/flux-framework/flux-restful-api /code/flux-restful-api && \
    cd /code/flux-restful-api && \
    python3 -m ensurepip && \
    python3 -m pip install -r requirements.txt

# Tokens for development
ENV FLUX_USER=fluxuser
ENV FLUX_TOKEN=12345
ENV FLUX_REQUIRE_AUTH="true"

# Server level option flags
ENV FLUX_OPTION_FLAGS="-ompi=openmpi@5"

# No token required for development
EXPOSE 5000
WORKDIR /code/flux-restful-api
COPY ./scripts/entrypoint.sh /code/scripts/entrypoint.sh
COPY ./nix/run.sh ./nix/run-operator.sh /code/nix/
COPY ./examples /code/examples
ENTRYPOINT /bin/bash /code/scripts/entrypoint.sh
