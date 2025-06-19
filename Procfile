web: gunicorn tender.wsgi:application --log-file - --env DJANGO_SETTINGS_MODULE=tender.settings_heroku
release: python manage.py migrate --settings=tender.settings_heroku
