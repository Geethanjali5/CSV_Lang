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

# Step 2: Run the tests
echo "Running the tests..."
python3 ../test.py "$1"
