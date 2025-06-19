import os
import sys

# Build path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the app to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure application for Heroku
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tender.settings')
application = get_wsgi_application()

# Whitenoise configuration for static files on Heroku
from whitenoise import WhiteNoise
application = WhiteNoise(application)
application.add_files(os.path.join(BASE_DIR, 'static'), prefix='static/')
application.add_files(os.path.join(BASE_DIR, 'staticfiles'), prefix='staticfiles/')
application.add_files(os.path.join(BASE_DIR, 'media'), prefix='media/')
