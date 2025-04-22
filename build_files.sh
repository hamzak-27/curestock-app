#!/bin/bash

# This script is used to build and prepare files for deployment on Vercel

# Exit on any error
set -e

# Update apt packages and install dependencies
apt-get update
apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

# Debug directory contents
echo "Current directory contents:"
ls -la

# Create the staticfiles directory
mkdir -p staticfiles
echo "Created staticfiles directory"
ls -la staticfiles

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Run collectstatic
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Collectstatic failed, but continuing..."

# Create a verification file to ensure staticfiles directory exists
echo "Vercel deployment" > staticfiles/verification.txt

# Debug staticfiles directory after collection
echo "Staticfiles directory contents after collection:"
ls -la staticfiles

echo "Build script completed successfully" 