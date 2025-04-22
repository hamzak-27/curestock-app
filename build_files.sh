#!/bin/bash

# Build script for Vercel Django deployment

echo "Building the project..."
# Use absolute path to Python in Vercel environment
/opt/conda/bin/python -m pip install --upgrade pip
/opt/conda/bin/pip install -r requirements.txt

echo "Collecting static files..."
/opt/conda/bin/python manage.py collectstatic --noinput

echo "Make migrations..."
/opt/conda/bin/python manage.py makemigrations

echo "Migrate database..."
/opt/conda/bin/python manage.py migrate

echo "Build completed." 