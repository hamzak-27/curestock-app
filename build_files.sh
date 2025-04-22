#!/bin/bash

# This script is used to build and prepare the static files for Render deployment

# Exit immediately if a command exits with a non-zero status
set -e

echo "=== Starting build process ==="
echo "Current directory contents:"
ls -la

# Create staticfiles directory if it doesn't exist
echo "=== Setting up staticfiles directory ==="
mkdir -p staticfiles

# Create an empty .keep file to ensure the directory is included in git
touch staticfiles/.keep

# Install Python dependencies
echo "=== Installing Python requirements ==="
pip install --no-cache-dir -r requirements.txt 

# Run collectstatic
echo "=== Running collectstatic ==="
python manage.py collectstatic --noinput

# Display final staticfiles directory contents
echo "=== Final staticfiles directory contents ==="
ls -la staticfiles/

echo "=== Build process completed ===" 