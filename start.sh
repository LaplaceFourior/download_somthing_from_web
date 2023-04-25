#!/bin/bash

echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated."

# Check if required packages are already installed
required_packages=$(cat requirements.txt)
installed_packages=$(pip freeze)
missing_packages=""
for package in $required_packages; do
    if ! echo "$installed_packages" | grep -q "$package"; then
        missing_packages="$missing_packages $package"
    fi
done

if [ -n "$missing_packages" ]; then
    echo "Installing required packages..."
    pip install $missing_packages
else
    echo "Required packages already installed."
fi

echo "Packages installed."
echo "Starting application..."
python3 main.py &