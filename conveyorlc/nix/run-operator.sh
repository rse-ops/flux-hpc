#!/bin/bash

echo $PWD

. /root/.nix-profile/etc/profile.d/nix.sh

NIX_PATH=$PATH
NIX_PYTHONPATH=$PYTHONPATH

. /etc/profile.d/z10_spack_environment.sh

export PATH=/home/flux/.nix-profile/bin:$PATH:$NIX_PATH
export PYTHONPATH=$PYTHONPATH:/opt/view/lib/python3.10/site-packages:$NIX_PYTHONPATH

# Hard coded environment just for example
export CONVEYORLCHOME=/nix/store/c65k6cyi3qid4kiyyr85dzvcijfaw16w-conveyorlc-1.1.2-1/
export LBindData=$CONVEYORLCHOME/data
export PATH=$CONVEYORLCHOME/bin:/nix/store/g36nfns6bm8gqwabxqv4d3w8z043x71g-openbabel-2.4.1/bin:$PATH
export AMBERHOME=/home/fluxuser/mamba/
export PATH=$AMBERHOME/bin/:$PATH

# Make sure the spack PYTHONPATH is merged with Nix
export PYTHONPATH=$PYTHONPATH:/opt/view/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-pyrsistent-0.18.1-4y45yicct333hekudm6spwmfo4zurvir/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-attrs-22.1.0-6l7qhin5aaqyev56skpsvruxox2ywn3s/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-pycparser-2.21-7seqp6a5ivvr4t3xygon2ttiyh55bbm6/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-pyyaml-6.0-ayf2ig4btgiev7ir675l7oywhvgl7rhs/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-jsonschema-4.16.0-6zl5yjunrcsn4zpywynn5oph32iqlvou/lib/python3.10/site-packages:/opt/software/linux-ubuntu20.04-x86_64/gcc-9.4.0/py-cffi-1.15.0-gyk2my27jc3b5gno4zcqtm3riumyl4vp/lib/python3.10/site-packages;

cd /code/examples
exec CDT1Receptor --input  pdb.list --output out --version 16 --spacing 1.4 --minimize on --forceRedo on

