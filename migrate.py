#!/usr/bin/env python
import os
import sys
import subprocess

"""
This script handles database migrations for the PostgreSQL database.
"""

if __name__ == "__main__":
    # Set up Django environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    
    # Force the DATABASE_URL to be used
    os.environ["VERCEL"] = "1"
    
    # Run migrations
    print("Running migrations...")
    subprocess.call(["python", "manage.py", "migrate"])
    
    print("Creating superuser if needed...")
    # Use environment variables for superuser credentials if available
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "adminpassword")
    
    # Check if superuser exists
    try:
        from django.contrib.auth.models import User
        import django
        django.setup()
        
        if not User.objects.filter(username=username).exists():
            print(f"Creating superuser {username}...")
            User.objects.create_superuser(username, email, password)
            print("Superuser created successfully!")
        else:
            print("Superuser already exists.")
    except Exception as e:
        print(f"Error creating superuser: {e}")
    
    print("Migration process completed.") 