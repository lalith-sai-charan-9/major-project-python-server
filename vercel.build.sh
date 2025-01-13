#!/bin/bash

# Install Python 3.10
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh -o miniforge.sh
bash miniforge.sh -b -p $HOME/conda
export PATH="$HOME/conda/bin:$PATH"
conda create -n myenv python=3.10 -y
source $HOME/conda/bin/activate myenv

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads
