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

# Run migrations during build
echo "=== Running migrations ==="
if [ -n "$DATABASE_URL" ]; then
    echo "Database URL exists, running migrations"
    
    # Show migration plan first for debugging
    echo "=== Current migration status ==="
    python manage.py showmigrations
    
    # Run migrations with verbosity for debugging
    echo "=== Applying migrations ==="
    python manage.py migrate --noinput --verbosity 2
    
    # Verify migrations were applied
    echo "=== Verifying migrations ==="
    python manage.py showmigrations
    echo "=== Migrations completed ==="
else
    echo "DATABASE_URL not set, skipping migrations"
fi

# Make script files executable in Unix/Linux environments
if [ "$(uname)" != "Windows_NT" ]; then
    echo "=== Making helper scripts executable ==="
    chmod +x run_migrations.sh reset_migrations.py deploy_helpers.py
fi

echo "=== Build process completed ===" 