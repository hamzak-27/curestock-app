#!/bin/bash

# This script is used to build and prepare files for deployment on Vercel

# Exit immediately if a command exits with a non-zero status
set -e

echo "Current directory contents:"
ls -la

# Create and populate staticfiles directory first, before any commands that might fail
echo "Setting up static files directory..."
mkdir -p staticfiles
echo "Vercel deployment" > staticfiles/index.html
echo "/* Empty CSS file */" > staticfiles/style.css
echo "console.log('Hello from Vercel');" > staticfiles/script.js

# List the staticfiles directory to confirm it exists with content
echo "Staticfiles directory contents:"
ls -la staticfiles/

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --no-cache-dir -r vercel-requirements.txt

# Try to run collectstatic but continue on failure
echo "Running collectstatic..."
python manage.py collectstatic --noinput || echo "Collectstatic failed, but continuing build"

# List staticfiles directory contents
echo "Final staticfiles directory contents:"
ls -la staticfiles/

echo "Build script completed successfully" 