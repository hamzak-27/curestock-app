#!/bin/bash
# Script to run migrations manually on Render
# Make this file executable before use: chmod +x run_migrations.sh

echo "=== Starting manual migration process ==="

# Check if running in production environment
if [ -z "$RENDER" ]; then
    echo "Error: This script is intended to be run in a Render environment."
    echo "If you're running this locally, try: python manage.py migrate"
    exit 1
fi

# Check for database URL
if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL environment variable is not set."
    exit 1
fi

echo "=== Checking migration status ==="
python manage.py showmigrations

echo "=== Running migrations ==="
python manage.py migrate --noinput --verbosity 2

echo "=== Verifying migrations ==="
python manage.py showmigrations

echo "=== Migration process completed ===" 