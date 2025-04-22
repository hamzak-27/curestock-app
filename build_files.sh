#!/bin/bash

# This script is used to build and prepare files for deployment on Vercel

# Print commands before execution and exit on error
set -ex

echo "Current directory contents:"
ls -la

# Create public directory for Vercel
echo "Creating public directory structure..."
mkdir -p public
cp -r staticfiles/* public/ 2>/dev/null || true

# Add default files to public directory
echo "<h1>CureStock App</h1><p>Vercel Deployment</p>" > public/index.html
echo "body { font-family: Arial; }" > public/style.css
echo "console.log('Vercel deployment');" > public/script.js

echo "Public directory created with contents:"
ls -la public/

# Install Python dependencies 
echo "Installing Python dependencies..."
pip install --no-cache-dir -r vercel-requirements.txt

# Try to run collectstatic but continue on failure
echo "Running collectstatic to public directory..."
python manage.py collectstatic --noinput --settings=myproject.settings || echo "Collectstatic failed, continuing..."

# Ensure the public folder has content even if collectstatic fails
echo "Ensuring public directory has content..."
ls -la public/ || echo "Public directory listing failed"

# Copy public directory to staticfiles as backup
echo "Copying public directory to staticfiles..."
mkdir -p staticfiles
cp -r public/* staticfiles/ 2>/dev/null || true

echo "Final staticfiles directory contents:"
ls -la staticfiles/

echo "Build script completed successfully" 