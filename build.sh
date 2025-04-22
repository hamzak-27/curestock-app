#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Starting build process ==="

# Install dependencies
echo "=== Installing Python requirements ==="
pip install -r requirements.txt

# Collect static files
echo "=== Running collectstatic ==="
python manage.py collectstatic --no-input

# Run migrations automatically during build
echo "=== Running migrations ==="
echo "Database URL exists: $DATABASE_URL"
python manage.py migrate

# Make sure app.py is readable
echo "=== Setting up app.py ==="
chmod +x app.py
ls -la app.py

echo "=== Build process completed ===" 