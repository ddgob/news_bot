#!/bin/bash

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install Miniconda or Anaconda first."
    exit 1
fi

# Create the Conda environment
echo "Creating the Conda environment..."
conda env create -f conda.yaml

# Activate the Conda environment
echo "Activating the Conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate rpa_env