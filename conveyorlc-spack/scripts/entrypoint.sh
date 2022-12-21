#!/bin/bash

cd /opt/spack-environment
. /opt/spack-environment/spack/share/spack/setup-env.sh
spack env activate .

cd /code/flux-restful-api

# Make sure the spack PYTHONPATH is merged with Nix
flux start uvicorn app.main:app --host=0.0.0.0 --port=5000
