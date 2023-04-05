#!/bin/bash

# Modified from 
# https://github.com/LLNL/weave-demos/blob/main/ball_bounce/setup.sh
# to install to the system python 3 environment alongside Flux

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m ipykernel install --name ball-bounce-demo

# Creating folders for data and images

mkdir ./01_baseline_simulation/baseline/data/
mkdir ./01_baseline_simulation/baseline/images/
mkdir ./01_baseline_simulation/num_res/data/
mkdir ./01_baseline_simulation/num_res/images/
mkdir ./03_simulation_ensembles/data/
mkdir ./04_manage_data/data/
mkdir ./05_post-process_data/images/
mkdir ./06_surrogate_model/data/
mkdir ./06_surrogate_model/images/


echo "Setup complete!"
