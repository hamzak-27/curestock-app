#!/usr/bin/env python3
"""
Script to reset and apply migrations to a PostgreSQL database on Render.
This can be run manually if migrations are not being applied correctly.
"""

import os
import sys
import logging
import subprocess
import django
from django.conf import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def setup_django():
    logger.info("Setting up Django...")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    os.environ["RENDER"] = "1"
    django.setup()
    logger.info(f"Django version: {django.get_version()}")
    
def check_database_connection():
    """Verify database connection"""
    logger.info("Checking database connection...")
    if 'DATABASE_URL' not in os.environ:
        logger.error("DATABASE_URL not set in environment variables")
        return False
    
    try:
        from django.db import connections
        from django.db.utils import OperationalError
        
        conn = connections['default']
        conn.cursor()
        logger.info("Database connection successful")
        return True
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        return False

def reset_migrations():
    """Reset and apply migrations"""
    logger.info("Resetting and applying migrations...")
    
    # Step 1: Show current migration state
    logger.info("Current migration state:")
    subprocess.run([sys.executable, "manage.py", "showmigrations"])
    
    # Step 2: Apply migrations
    logger.info("Applying migrations...")
    try:
        result = subprocess.run(
            [sys.executable, "manage.py", "migrate", "--noinput", "--verbosity", "2"],
            capture_output=True,
            text=True
        )
        logger.info(f"Migration stdout: {result.stdout}")
        if result.stderr:
            logger.warning(f"Migration stderr: {result.stderr}")
        
        # Step 3: Verify migrations
        logger.info("Verifying migrations...")
        subprocess.run([sys.executable, "manage.py", "showmigrations"])
        
    except Exception as e:
        logger.error(f"Error applying migrations: {e}")
        return False
    
    return True

def main():
    """Main function"""
    logger.info("Starting database migration script...")
    
    # Setup Django
    setup_django()
    
    # Check database connection
    if not check_database_connection():
        logger.error("Failed to connect to database. Exiting.")
        sys.exit(1)
    
    # Reset and apply migrations
    if reset_migrations():
        logger.info("Migration process completed successfully")
    else:
        logger.error("Migration process failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 