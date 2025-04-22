#!/bin/bash

# Build script for Vercel Django deployment

echo "Building the project..."
# Try to find Python in standard locations
which python3 || echo "Python3 not found"
python3 -m pip install --upgrade pip || echo "Failed to upgrade pip"
python3 -m pip install -r requirements.txt || echo "Failed to install requirements"

echo "Collecting static files..."
python3 manage.py collectstatic --noinput || echo "Failed to collect static files"

echo "Make migrations..."
python3 manage.py makemigrations || echo "Failed to make migrations"

echo "Migrate database..."
python3 manage.py migrate || echo "Failed to migrate"

echo "Build completed." 