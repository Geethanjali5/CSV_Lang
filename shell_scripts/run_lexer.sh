#!/bin/bash

# Script to install Python and run the scanner script

# Step 1: Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 not found. Installing Python3..."

    # Update package list
    sudo apt update

    # Install Python3
    sudo apt install -y python3 python3-pip
else
    echo "Python3 is already installed."
fi

# Step 2: Install argparse if needed (should be part of standard library)
python3 -m pip install argparse

# Step 3: Run the scanner script
if [ -f "$1" ]; then
    echo "Running scanner script with file: $1"
    python3 ../scanner.py "$1"
else
    echo "Error: File $1 not found. Please provide a valid path to the CSV Lang source code."
    exit 1
fi