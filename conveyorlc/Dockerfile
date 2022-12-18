ARG ubuntu_version=20.04
FROM ghcr.io/rse-ops/flux-spack:ubuntu-${ubuntu_version}

RUN touch /etc/apt/apt.conf.d/99verify-peer.conf \
    && echo >>/etc/apt/apt.conf.d/99verify-peer.conf "Acquire { https::Verify-Peer false }"

ENV USER=flux
ENV EDITOR=vim
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/home/flux/.nix-profile/bin:$PATH

RUN sudo apt-get update && \
    sudo apt-get install -y \
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

# install nix as flux (note this is a single user install)
# add --daemon for multi-user, but then you need to setup flux's home
# https://nixos.org/manual/nix/stable/installation/multi-user.html
USER flux
WORKDIR /code
COPY ./ /code
RUN /bin/bash -c "sh <(curl -L https://nixos.org/nix/install)" && \
    /bin/bash /code/scripts/init-home.sh /home/flux && \
    cp /code/nix/config.nix /home/flux/.config/nixpkgs/config.nix

# Install cachix (binary cache)
RUN nix-env -iA cachix -f https://cachix.org/api/v1/install && \
    cachix use rseops && \
    sudo chown -R flux /code 

WORKDIR /code/nix

# The flake.nix defines our development shell
RUN nix develop -c micromamba create --prefix /home/flux/mamba -f /code/environment.yaml
