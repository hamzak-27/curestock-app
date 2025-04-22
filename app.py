"""
Entry point for Render deployment.
This file redirects to the Django WSGI application.
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
os.environ["RENDER"] = "1"

# Ensure DATABASE_URL is available if set
if "DATABASE_URL" in os.environ:
    logger.info(f"Database URL is configured: {os.environ['DATABASE_URL'][:20]}...")
else:
    logger.warning("DATABASE_URL not found in environment variables")

# Set up Django
import django
django.setup()

# Run migrations on startup - critical for initial setup
try:
    logger.info("Attempting to run migrations on startup")
    from django.core.management import call_command
    
    # Check migration status
    logger.info("Current migration status:")
    call_command('showmigrations')
    
    # Apply migrations
    logger.info("Applying migrations...")
    call_command('migrate', interactive=False, verbosity=2)
    
    logger.info("Migrations completed successfully")
except Exception as e:
    logger.error(f"Error running migrations: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())

# Import the Django WSGI application
from myproject.wsgi import application as django_application

# Make the application available as 'app' for Render
app = django_application 