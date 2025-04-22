#!/usr/bin/env python3
"""
Fix script specifically for CureStock database deployment on Render.
This script directly uses the known database credentials.
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

# Known database URLs for curestock_1
INTERNAL_DB_URL = "postgresql://curestock_1_user:30ojM7FOojsrncsOMGJcmkaZ9icLuN2Y@dpg-d03trh6uk2gs73cldm1g-a/curestock_1"
EXTERNAL_DB_URL = "postgresql://curestock_1_user:30ojM7FOojsrncsOMGJcmkaZ9icLuN2Y@dpg-d03trh6uk2gs73cldm1g-a.oregon-postgres.render.com/curestock_1"

def setup_environment():
    """Set up the environment with the correct database URL"""
    logger.info("Setting up environment...")
    
    # Set RENDER environment variable
    os.environ["RENDER"] = "true"
    logger.info("Set RENDER=true")
    
    # Set the database URL - try both internal and external URLs
    current_url = os.environ.get("DATABASE_URL")
    
    if current_url:
        logger.info(f"DATABASE_URL is already set: {current_url[:20]}...")
    else:
        # Try external URL first
        os.environ["DATABASE_URL"] = EXTERNAL_DB_URL
        logger.info(f"Set DATABASE_URL to external database URL")
    
    # Set Django settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    logger.info("Set DJANGO_SETTINGS_MODULE=myproject.settings")
    
    return True

def setup_django():
    """Set up Django"""
    try:
        logger.info("Setting up Django...")
        django.setup()
        logger.info(f"Django version: {django.get_version()}")
        return True
    except Exception as e:
        logger.error(f"Error setting up Django: {e}")
        logger.error(traceback.format_exc())
        return False

def test_database_connection():
    """Test database connection with both URLs if needed"""
    logger.info("Testing database connection...")
    
    try:
        from django.db import connections
        from django.db.utils import OperationalError
        
        # Try with current URL
        conn = connections['default']
        try:
            conn.ensure_connection()
            if conn.is_usable():
                logger.info("Database connection is working!")
                return True
        except OperationalError as e:
            logger.warning(f"Could not connect with current DATABASE_URL: {e}")
        
        # If current URL failed, try the internal URL
        if os.environ.get("DATABASE_URL") != INTERNAL_DB_URL:
            logger.info("Trying internal database URL...")
            os.environ["DATABASE_URL"] = INTERNAL_DB_URL
            
            # Reset connection
            connections.close_all()
            conn = connections['default']
            
            try:
                conn.ensure_connection()
                if conn.is_usable():
                    logger.info("Database connection is working with internal URL!")
                    return True
            except OperationalError as e:
                logger.warning(f"Could not connect with internal DATABASE_URL: {e}")
        
        # If internal URL failed, try the external URL
        if os.environ.get("DATABASE_URL") != EXTERNAL_DB_URL:
            logger.info("Trying external database URL...")
            os.environ["DATABASE_URL"] = EXTERNAL_DB_URL
            
            # Reset connection
            connections.close_all()
            conn = connections['default']
            
            try:
                conn.ensure_connection()
                if conn.is_usable():
                    logger.info("Database connection is working with external URL!")
                    return True
            except OperationalError as e:
                logger.error(f"Could not connect with external DATABASE_URL: {e}")
        
        logger.error("All database connection attempts failed!")
        return False
        
    except Exception as e:
        logger.error(f"Unexpected error testing database connection: {e}")
        logger.error(traceback.format_exc())
        return False

def run_migrations():
    """Run migrations"""
    try:
        logger.info("Running migrations...")
        from django.core.management import call_command
        
        # Check current migration status
        logger.info("Current migration status:")
        call_command('showmigrations')
        
        # Apply migrations
        logger.info("Applying migrations...")
        call_command('migrate', verbosity=2, interactive=False)
        
        # Verify migrations were applied
        logger.info("Migration status after applying migrations:")
        call_command('showmigrations')
        
        return True
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        logger.error(traceback.format_exc())
        return False

def main():
    """Main function"""
    logger.info("=" * 60)
    logger.info("CURESTOCK DATABASE FIX SCRIPT")
    logger.info("=" * 60)
    
    # Set up environment
    if not setup_environment():
        logger.error("Failed to set up environment!")
        sys.exit(1)
    
    # Set up Django
    if not setup_django():
        logger.error("Failed to set up Django!")
        sys.exit(1)
    
    # Test database connection
    if not test_database_connection():
        logger.error("Failed to connect to database!")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        logger.error("Failed to run migrations!")
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("CureStock database fix completed successfully!")
    logger.info("=" * 60)
    logger.info("You should now be able to access your application without database errors.")
    logger.info("=" * 60)

if __name__ == "__main__":
    main() 