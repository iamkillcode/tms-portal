# PowerShell script to deploy the application to Heroku

Write-Host "Beginning deployment to Heroku..." -ForegroundColor Green

# Check if Heroku CLI is installed
if (!(Get-Command heroku -ErrorAction SilentlyContinue)) {
    Write-Host "Heroku CLI could not be found. Please install it first." -ForegroundColor Red
    exit 1
}

# Check if git is initialized
if (!(Test-Path .git)) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit for Heroku deployment"
}

# Create Heroku app if it doesn't exist
try {
    heroku apps:info
} 
catch {
    Write-Host "Creating Heroku app..." -ForegroundColor Yellow
    heroku create
}

# Add Heroku PostgreSQL add-on
Write-Host "Adding PostgreSQL database..." -ForegroundColor Yellow
heroku addons:create heroku-postgresql:standard-0

# Set environment variables
Write-Host "Setting environment variables..." -ForegroundColor Yellow
$secret_key = & python -c "import secrets; print(secrets.token_urlsafe(50))"
heroku config:set DJANGO_SECRET_KEY=$secret_key
heroku config:set DJANGO_SETTINGS_MODULE=tender.settings_heroku

# Deploy to Heroku
Write-Host "Deploying to Heroku..." -ForegroundColor Yellow
git push heroku master

# Run migrations
Write-Host "Running migrations..." -ForegroundColor Yellow
heroku run python manage.py migrate --settings=tender.settings_heroku

# Create superuser
Write-Host "Creating superuser..." -ForegroundColor Yellow
heroku run python manage.py createsuperuser --settings=tender.settings_heroku

# Open the app in browser
Write-Host "Opening app in browser..." -ForegroundColor Yellow
heroku open

Write-Host "Deployment completed successfully!" -ForegroundColor Green
