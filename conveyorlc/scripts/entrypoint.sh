#!/bin/bash

# number workers: 2
# workdir: /code/examples

. /root/.nix-profile/etc/profile.d/nix.sh

NIX_PATH=$PATH
NIX_PYTHONPATH=$PYTHONPATH

. /etc/profile.d/z10_spack_environment.sh

export PATH=/home/flux/.nix-profile/bin:$PATH:$NIX_PATH
export PYTHONPATH=$PYTHONPATH:/opt/view/lib/python3.10/site-packages:$NIX_PYTHONPATH

# Make sure the spack PYTHONPATH is merged with Nix
flux start uvicorn app.main:app --host=0.0.0.0 --port=5000
