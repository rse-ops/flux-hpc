#!/bin/bash

HERE=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

eval "$(conda shell.bash activate /opt/conda/envs/moldesign-demo)"
python3 ${HERE}/0_molecular-design-with-parsl.py $@
