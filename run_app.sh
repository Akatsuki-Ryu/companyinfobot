#!/bin/bash

# Name of the Conda environment
ENV_NAME="company"

# Check if the Conda environment exists
if ! conda info --envs | grep -q $ENV_NAME; then
    echo "Creating Conda environment: $ENV_NAME"
    conda create -n $ENV_NAME python=3.10 -y
else
    echo "Conda environment $ENV_NAME already exists"
fi

# Activate the Conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

# Uninstall existing packages to avoid conflicts
echo "Uninstalling existing packages"
pip uninstall -y flask werkzeug selenium webdriver_manager

# Install or update required packages
echo "Installing/updating required packages"
pip install -r requirements.txt

# Run the Flask application
echo "Starting the Flask application"
python main.py