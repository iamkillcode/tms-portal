web: gunicorn tender.wsgi:application --log-file - --env DJANGO_SETTINGS_MODULE=tender.settings_heroku --env WHITENOISE_ENABLED=true
release: python manage.py migrate --settings=tender.settings_heroku && python manage.py collectstatic --noinput --settings=tender.settings_heroku
