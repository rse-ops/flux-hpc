#!/bin/bash

cd /opt/spack-environment
. /opt/spack-environment/spack/share/spack/setup-env.sh
spack env activate .

cd /code/examples

export CONVEYORLCHOME=$(spack find --format "{prefix}" conveyorlc)
export LBindData=$CONVEYORLCHOME/data
export AMBERHOME=/opt/conda

CDT1Receptor --input  pdb.list --output out --version 16 --spacing 1.4 --minimize on --forceRedo on
