from myproject.wsgi import application
# This is a simple index file that Vercel can use as an entry point

def handler(request, **kwargs):
    return application(request, **kwargs) 