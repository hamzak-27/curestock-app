#!/bin/bash

# This script is used to build and prepare files for deployment on Vercel

# Exit immediately if a command exits with a non-zero status
set -e

echo "Current directory contents:"
ls -la

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install --no-cache-dir -r vercel-requirements.txt

# Create and populate staticfiles directory
echo "Setting up static files..."
mkdir -p staticfiles
touch staticfiles/.vercel_build_output

# Create a simple CSS file to verify static files are working
echo "Creating CSS file..."
cat > staticfiles/style.css << 'EOL'
/* Basic styles */
body {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
}

.container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
}
EOL

# Try to run collectstatic but continue on failure
echo "Running collectstatic..."
python manage.py collectstatic --noinput || echo "Collectstatic failed, but continuing build"

# List staticfiles directory contents
echo "Staticfiles directory contents:"
ls -la staticfiles/

echo "Build script completed successfully" 