#!/usr/bin/env python3
"""
Script to diagnose and fix database connection issues on Render.
Run this script directly on Render through the shell access.
"""

import os
import sys
import logging
import traceback
import django

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check environment variables and Django setup"""
    logger.info("Checking environment...")
    
    # Check if RENDER environment is set
    if not os.environ.get('RENDER'):
        logger.warning("RENDER environment variable not set. Setting it now.")
        os.environ['RENDER'] = "1"
    
    # Check DATABASE_URL
    if 'DATABASE_URL' in os.environ:
        db_url = os.environ.get('DATABASE_URL')
        masked_url = f"{db_url[:20]}..." if db_url and len(db_url) > 20 else db_url
        logger.info(f"DATABASE_URL is set: {masked_url}")
    else:
        logger.error("DATABASE_URL environment variable not set!")
        logger.info("Available environment variables:")
        for key in sorted(os.environ.keys()):
            if key.startswith("DATABASE") or key in ["RENDER", "DEBUG"]:
                logger.info(f"  - {key}: {os.environ[key]}")
        
        return False
    
    return True

def setup_django():
    """Set up Django environment"""
    try:
        logger.info("Setting up Django...")
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
        django.setup()
        logger.info(f"Django version: {django.get_version()}")
        return True
    except Exception as e:
        logger.error(f"Error setting up Django: {e}")
        logger.error(traceback.format_exc())
        return False

def check_database_connection():
    """Check database connection"""
    try:
        logger.info("Checking database connection...")
        from django.db import connections
        from django.db.utils import OperationalError
        
        conn = connections['default']
        conn.ensure_connection()
        if conn.is_usable():
            logger.info("Database connection is working!")
            return True
        else:
            logger.error("Database connection is not usable.")
            return False
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking database connection: {e}")
        logger.error(traceback.format_exc())
        return False

def run_migrations():
    """Run migrations"""
    try:
        logger.info("Running migrations...")
        from django.core.management import call_command
        
        # Show migration status
        logger.info("Current migration status:")
        call_command('showmigrations')
        
        # Run migrations
        logger.info("Applying migrations...")
        call_command('migrate', verbosity=2, interactive=False)
        
        # Show migration status again
        logger.info("Migration status after applying migrations:")
        call_command('showmigrations')
        
        return True
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        logger.error(traceback.format_exc())
        return False

def check_tables():
    """Check if tables exist in the database"""
    try:
        logger.info("Checking database tables...")
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = [row[0] for row in cursor.fetchall()]
            
            logger.info(f"Found {len(tables)} tables in the database:")
            for table in sorted(tables):
                logger.info(f"  - {table}")
            
            # Check for specific app tables
            app_tables = [t for t in tables if t.startswith('myapp_')]
            logger.info(f"Found {len(app_tables)} tables for 'myapp':")
            for table in sorted(app_tables):
                logger.info(f"  - {table}")
            
            if 'myapp_call' not in tables:
                logger.warning("The 'myapp_call' table is missing!")
            
        return True
    except Exception as e:
        logger.error(f"Error checking tables: {e}")
        logger.error(traceback.format_exc())
        return False

def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("RENDER DATABASE SETUP AND DIAGNOSTICS")
    logger.info("=" * 60)
    
    # Check environment
    if not check_environment():
        logger.error("Environment check failed!")
        sys.exit(1)
    
    # Setup Django
    if not setup_django():
        logger.error("Django setup failed!")
        sys.exit(1)
    
    # Check database connection
    if not check_database_connection():
        logger.error("Database connection failed!")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        logger.error("Running migrations failed!")
        sys.exit(1)
    
    # Check tables
    if not check_tables():
        logger.error("Checking tables failed!")
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("Database setup and diagnostics completed successfully!")
    logger.info("=" * 60)

if __name__ == "__main__":
    main() 