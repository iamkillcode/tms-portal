"""
WSGI config for tender project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Get base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the app to the Python path
sys.path.append(BASE_DIR)

# Set default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tender.settings')

# Get WSGI application
application = get_wsgi_application()

# Configure WhiteNoise for static files if in production
# This is activated by setting an environment variable
if os.environ.get('WHITENOISE_ENABLED', '').lower() in ('true', '1', 't'):
    try:
        from whitenoise import WhiteNoise
        application = WhiteNoise(application)
        application.add_files(os.path.join(BASE_DIR, 'static'), prefix='static/')
        application.add_files(os.path.join(BASE_DIR, 'staticfiles'), prefix='staticfiles/')
        application.add_files(os.path.join(BASE_DIR, 'media'), prefix='media/')
    except ImportError:
        print("WhiteNoise not installed, static files may not be served correctly in production")
