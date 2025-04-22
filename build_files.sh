#!/bin/bash

# Build script for Vercel Django deployment

echo "Building the project..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Make migrations..."
python manage.py makemigrations

echo "Migrate database..."
python manage.py migrate

echo "Build completed." 