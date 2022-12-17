#!/usr/bin/env bash

. /etc/profile.d/z10_spack_environment.sh 

install_branch=${INSTALL_BRANCH}
install_repo=${INSTALL_REPO:-flux-framework/flux-restful-api}

# If we are given a custom branch to install, do that first
if [[ ! -z ${install_branch} ]]; then
    cd /tmp
    printf "Custom install of https://github.com:${install_repo}@${install_branch}"
    rm -rf /code
    git clone -b ${install_branch} https://github.com/${install_repo} /code
fi

# We always need to start in this PWD
cd /code
flux start uvicorn app.main:app --host=${HOST} --port=${PORT}
