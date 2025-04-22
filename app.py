"""
Entry point for Render deployment.
This file redirects to the Django WSGI application.
"""

import os
import sys

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
os.environ["RENDER"] = "1"

# Ensure DATABASE_URL is available if set
if "DATABASE_URL" in os.environ:
    print("Database URL is configured")

# Import the Django WSGI application
from myproject.wsgi import application as django_application

# Make the application available as 'app' for Render
app = django_application 