#!/bin/bash

# Function to check if a conda environment exists
env_exists() {
    conda info --envs | grep -q "$1"
}

ENV_NAME="tetris_env"
PYTHON_VERSION="3.9"

# Check if the environment exists
if env_exists $ENV_NAME; then
    echo "Conda environment '$ENV_NAME' already exists. Reusing it."
else
    echo "Conda environment '$ENV_NAME' does not exist. Creating it."
    conda create -n $ENV_NAME python=$PYTHON_VERSION -y
fi

# Activate the virtual environment
source activate $ENV_NAME

# Ensure the environment is clean by reinstalling packages
pip install --upgrade pip
pip install numpy==1.19.5 tensorflow==2.5.0 pygame protobuf==3.20.*

# Run the tetris_dqn.py script
python main.py

# Deactivate the virtual environment
#conda deactivate
