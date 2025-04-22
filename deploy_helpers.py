#!/usr/bin/env python3
"""
Deployment helper functions for the CureStock application on Render.
These functions can be run manually to troubleshoot deployment issues.
"""

import os
import sys
import logging
import django
from django.core.management import call_command

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def setup_django():
    """Set up Django environment"""
    logger.info("Setting up Django environment...")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    os.environ["RENDER"] = "1"
    django.setup()
    logger.info(f"Django version: {django.get_version()}")

def run_migrations():
    """Run Django migrations"""
    setup_django()
    
    logger.info("Running migrations...")
    try:
        # Show migration status before
        logger.info("Migration status before:")
        call_command('showmigrations')
        
        # Run migrations
        logger.info("Applying migrations...")
        call_command('migrate', verbosity=2, interactive=False)
        
        # Show migration status after
        logger.info("Migration status after:")
        call_command('showmigrations')
        
        logger.info("Migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def reset_db_tables(app_name='myapp'):
    """
    Reset database tables for a specific app
    WARNING: This will delete all data in the specified app's tables
    """
    setup_django()
    
    logger.warning(f"⚠️ About to reset database tables for app: {app_name}")
    confirm = input(f"This will DELETE ALL DATA for app {app_name}. Type 'yes' to continue: ")
    
    if confirm.lower() != 'yes':
        logger.info("Operation cancelled")
        return
    
    try:
        # Fake unapplying migrations
        logger.info(f"Unapplying migrations for {app_name}...")
        call_command('migrate', app_name, 'zero', fake=True)
        
        # Apply migrations again
        logger.info(f"Reapplying migrations for {app_name}...")
        call_command('migrate', app_name, verbosity=2)
        
        logger.info(f"Reset completed for {app_name}")
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy_helpers.py [command]")
        print("Available commands:")
        print("  migrate - Run database migrations")
        print("  reset_tables - Reset database tables (will delete all data)")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "migrate":
        run_migrations()
    elif command == "reset_tables":
        reset_db_tables()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1) 