#!/bin/bash

# Script to install Python and run the scanner script

# Function to install Python on macOS using Homebrew
install_python_mac() {
    if ! command -v brew &> /dev/null
    then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    echo "Installing Python3 with Homebrew..."
    brew install python3
}

# Function to install Python on Linux using apt
install_python_linux() {
    echo "Python3 not found. Installing Python3..."
    sudo apt update
    sudo apt install -y python3 python3-pip
}

# Step 1: Detect the OS and install Python3 if not found
if ! command -v python3 &> /dev/null
then
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        install_python_linux
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        install_python_mac
    else
        echo "Unsupported OS. Please install Python3 manually."
        exit 1
    fi
else
    echo "Python3 is already installed."
fi

# Step 2: Install argparse if needed (should be part of standard library)
python3 -m pip install argparse

# Step 3: Install pandas
python3 -m pip3 install pandas

# Step 4: Run all the sample programs
printf "\nGenerating Code for Sample Program 1\n"
python3 optimised_code_generator.py sample_programs/programming_assignment_4/Program1.csvlang

echo "Generating Code for Sample Program 2"
python3 optimised_code_generator.py sample_programs/programming_assignment_4/Program2.csvlang

echo "Generating Code foring Sample Program 3"
python3 optimised_code_generator.py sample_programs/programming_assignment_4/Program3.csvlang

echo "Generating Code for Sample Program 4"
python3 optimised_code_generator.py sample_programs/programming_assignment_4/Program4.csvlang
