#!/bin/bash

# Build script for Vercel Django deployment
echo "Building the project..."

# Explicitly create staticfiles directory
mkdir -p staticfiles

# Install requirements
pip install -r requirements.txt

# Create a placeholder file to ensure staticfiles exists
echo "This is a placeholder to ensure the staticfiles directory exists" > staticfiles/placeholder.txt

echo "Build completed." 