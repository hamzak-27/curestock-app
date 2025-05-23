import os
import sys
import traceback
from myproject.wsgi import application
# This is a simple index file that Vercel can use as an entry point

def handler(request, **kwargs):
    try:
        return application(request, **kwargs)
    except Exception as e:
        # Create a detailed error response
        error_response = f"""
        <html>
        <head><title>Server Error</title></head>
        <body>
            <h1>Server Error (500)</h1>
            <h2>Error Details:</h2>
            <pre>{str(e)}</pre>
            
            <h2>Traceback:</h2>
            <pre>{traceback.format_exc()}</pre>
            
            <h2>Environment:</h2>
            <pre>
            DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'Not set')}
            ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS', 'Not set')}
            DATABASE_URL exists: {'Yes' if os.environ.get('DATABASE_URL') else 'No'}
            OPENAI_API_KEY exists: {'Yes' if os.environ.get('OPENAI_API_KEY') else 'No'}
            DEBUG: {os.environ.get('DEBUG', 'Not set')}
            Python version: {sys.version}
            </pre>
        </body>
        </html>
        """
        
        # Create a response with status code 500
        from django.http import HttpResponse
        return HttpResponse(error_response, content_type='text/html', status=500) 