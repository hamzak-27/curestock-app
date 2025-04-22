import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
import django
from django.core.management import call_command

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
# Set Render environment flag
os.environ["RENDER"] = "1"
application = get_wsgi_application()

def handler(request, **kwargs):
    try:
        # Special path for migrations
        if request.path == '/api/migrate' or request.path == '/migrate':
            return run_migrations(request)
        
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

def run_migrations(request):
    """Run database migrations and return results"""
    try:
        # Get an optional secret key from query params for basic security
        secret = request.GET.get('secret', '')
        env_secret = os.environ.get('MIGRATION_SECRET', '')
        
        # If a secret is set in environment, verify it
        if env_secret and secret != env_secret:
            return HttpResponse('Unauthorized: Invalid secret', status=401)
        
        # Run migrations
        output = []
        
        def capture_output(msg, **options):
            output.append(msg)
        
        # Configure Django for command
        if not django.apps.ready:
            django.setup()
            
        # Run migration with output capture
        call_command('migrate', interactive=False, stdout=capture_output)
        
        # Return results
        return HttpResponse(
            f"<h1>Migrations Complete</h1><pre>{''.join(output)}</pre>",
            content_type='text/html'
        )
        
    except Exception as e:
        return HttpResponse(
            f"<h1>Migration Error</h1><pre>{str(e)}\n\n{traceback.format_exc()}</pre>",
            content_type='text/html',
            status=500
        ) 