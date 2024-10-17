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

# Step 3: Run all the sample programs
echo "Lexing Sample Program 1"
python3 ../scanner.py ../sample_programs/Program1.csvlang

echo "Lexing Sample Program 2"
python3 ../scanner.py ../sample_programs/Program2.csvlang

echo "Lexing Sample Program 3"
python3 ../scanner.py ../sample_programs/Program3.csvlang

echo "Lexing Sample Program 4"
python3 ../scanner.py ../sample_programs/Program4.csvlang

echo "Lexing Sample Program 5"
python3 ../scanner.py ../sample_programs/Program5.csvlang
