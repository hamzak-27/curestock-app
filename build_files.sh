#!/bin/bash

# Build script for Vercel Django deployment
echo "Building the project..."
pip install -r requirements.txt

echo "Collecting static files..."
mkdir -p staticfiles
python manage.py collectstatic --noinput

echo "Build completed." 