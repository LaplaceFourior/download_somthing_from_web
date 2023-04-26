#!/bin/bash

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null
then
    echo "Installing virtualenv..."
    pip install virtualenv
else
    echo "virtualenv already installed."
fi

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]
then
    virtualenv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated."

# Check if required packages are already installed
required_packages=$(cat requirements/LinuxOrMacos.txt)
installed_packages=$(pip freeze)
missing_packages=""
for package in $required_packages
do
    if ! echo "$installed_packages" | grep -q "$package"
    then
        missing_packages="$missing_packages $package"
    fi
done

# Install missing packages
if [ -n "$missing_packages" ]
then
    echo "Installing required packages..."
    pip install $missing_packages
else
    echo "Required packages already installed."
fi

# Start application
echo "Packages installed."
echo "Starting application..."
python3 main.py &