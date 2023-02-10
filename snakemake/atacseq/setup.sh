#!/bin/bash

set -eEu -o pipefail

# Setup the mamba environment with snakedeploy
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
mv bin/micromamba /usr/local/bin && rmdir bin
which micromamba
mkdir -p /opt/micromamba/envs
micromamba create --prefix /opt/micromamba/envs/snakemake -f environment.yaml
micromamba shell init --shell=bash --prefix=/opt/micromamba
