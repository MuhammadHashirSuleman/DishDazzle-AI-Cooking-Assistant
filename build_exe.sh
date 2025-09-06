#!/bin/bash

# Build script for DishDazzle

echo "Building DishDazzle executable..."

# Check if PyInstaller is installed
pip show pyinstaller > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Create executable
pyinstaller --onefile --windowed --name DishDazzle src/main.py

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "Build successful! Executable created in dist/ directory."
    
    # Copy necessary files
    echo "Copying configuration files..."
    mkdir -p dist/config
    cp config/config.json dist/config/
    
    echo "Done! You can find the executable in the dist/ directory."
else
    echo "Build failed. Please check the error messages above."
fi