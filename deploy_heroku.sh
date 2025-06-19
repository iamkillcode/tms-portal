#!/bin/bash
# Script to deploy the application to Heroku

echo "Beginning deployment to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null
then
    echo "Heroku CLI could not be found. Please install it first."
    exit 1
fi

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for Heroku deployment"
fi

# Create Heroku app if it doesn't exist
if ! heroku apps:info &> /dev/null; then
    echo "Creating Heroku app..."
    heroku create
fi

# Add Heroku PostgreSQL add-on
echo "Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:standard-0

# Set environment variables
echo "Setting environment variables..."
heroku config:set DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
heroku config:set DJANGO_SETTINGS_MODULE=tender.settings_heroku

# Deploy to Heroku
echo "Deploying to Heroku..."
git push heroku master

# Run migrations
echo "Running migrations..."
heroku run python manage.py migrate --settings=tender.settings_heroku

# Create superuser
echo "Creating superuser..."
heroku run python manage.py createsuperuser --settings=tender.settings_heroku

# Open the app in browser
echo "Opening app in browser..."
heroku open

echo "Deployment completed successfully!"
