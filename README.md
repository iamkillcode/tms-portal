# Tender Management System (TMS)

A comprehensive web-based procurement management system developed for FDA Ghana. This system handles tender generation, vendor management, framework agreements, ISO number management, and includes additional utilities like a breakfast ordering system.

## System Overview

TMS streamlines the entire procurement process, from tender generation through vendor bidding to contract management. The system is built with Django and Bootstrap, providing a modern, responsive interface for procurement officers and administrators.

## Core Features

### 1. Tender Management
- Automated tender number generation
- Department and category-based classification
- Full tender lifecycle tracking
- Document reference management
- Export tender data to Excel

### 2. Item Management
- Detailed item specifications
- Quantity and unit tracking
- Brand and manufacturer information
- Technical specifications documentation

### 3. Vendor Bid Management
- Multiple vendor bid support
- Technical and financial scoring
- Automated winner selection
- Price comparison and analysis
- Currency support (GHS, USD, EUR)

### 4. Framework Agreements
- Agreement tracking with vendors
- Start and end date management
- Status tracking (Active/Expired/Terminated)
- Terms and conditions documentation

### 5. ISO Number Management
- ISO number generation and tracking
- Division-based categorization
- ISO document lifecycle management

### 6. User Management
- Role-based access control
- User profile management
- Activity tracking
- Secure authentication

## Technology Stack

- **Backend:** Django 4.x
- **Frontend:** Bootstrap 5.x
- **Database:** SQLite (can be configured for PostgreSQL)
- **Excel Integration:** openpyxl
- **Authentication:** Django built-in auth

## Installation

1. Clone the repository:
```powershell
git clone <repository-url>
cd tms-portal
```

2. Create and activate a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Set up the environment:
```powershell
# Copy example environment file
Copy-Item .env.example .env
# Edit .env with your settings
notepad .env
```

5. Run migrations:
```powershell
python manage.py migrate
```

6. Create initial data:
```powershell
# Create superuser
python manage.py createsuperuser

# Load initial data
python manage.py loaddata initial_data.json
```

7. Collect static files:
```powershell
python manage.py collectstatic
```

8. Start the development server:
```powershell
python manage.py runserver
```

9. Access the system:
- Main interface: http://127.0.0.1:8000
- Admin interface: http://127.0.0.1:8000/admin

## Usage Guide

### 1. Tender Management
#### Creating Tenders
1. Navigate to "Tender Generator"
2. Select department and category
3. Fill in tender details
4. Submit to generate unique tender number

#### Managing Items
1. Access tender from the list
2. Click "Items" button
3. Add items with detailed specifications:
   - Item name and description
   - Quantity and unit of measure
   - Brand and manufacturer details
   - Technical specifications

#### Vendor Bids
1. Select an item from tender
2. Click "Manage Bids"
3. Record vendor bids:
   - Unit price and currency
   - Technical and financial scores
   - Supporting documentation
4. Mark winning bids

#### Framework Agreements
1. Access tender's agreements section
2. Create agreement with winning vendor
3. Specify:
   - Agreement duration
   - Terms and conditions
   - Pricing details
4. Monitor agreement status

### 2. ISO Number Management
1. Navigate to "ISO Generator"
2. Select division and document type
3. Fill required details
4. Generate ISO number
5. Track ISO document lifecycle

### 3. Additional Features
#### Breakfast Ordering System
1. Access Shop section
2. Browse available items
3. Add items to cart
4. Submit order

#### Reports and Analytics
1. Access Reports section
2. Select report type
3. Set parameters
4. Generate and export reports

## Project Structure

```
tms-portal/
├── tender/                  # Project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── tender_app/             # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin interface customization
│   ├── urls.py            # App URL patterns
│   ├── utils.py           # Utility functions
│   ├── migrations/        # Database migrations
│   └── templates/         # App-specific templates
├── templates/              # Global templates
│   ├── base.html          # Base template
│   └── admin/             # Admin template overrides
├── static/                # Static files
│   └── css/              # CSS files
│       ├── main.css      # Main styling
│       ├── auth.css      # Authentication styling
│       └── tender.css    # Tender-specific styling
├── staticfiles/           # Collected static files
├── breakfast_items/       # Media files for breakfast items
├── manage.py             # Django management script
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Key URLs

### Tender Management
- `/tender-generator/` - Generate new tenders
- `/tenders/list/` - List all tenders
- `/tenders/<id>/items/` - Manage tender items
- `/tenders/<id>/agreements/` - Manage framework agreements
- `/tenders/activity/` - View tender activity

### ISO Management
- `/iso-generator/` - Generate new ISO numbers
- `/iso/list/` - List all ISO numbers
- `/iso/<id>/` - ISO number details

### User Management
- `/login/` - User login
- `/register/` - New user registration
- `/dashboard/` - User dashboard

### Additional Services
- `/shop/` - Breakfast ordering system
- `/reports/` - System reports
- `/search/` - Global search functionality

## Configuration

Key settings in `tender/settings.py`:
- Database configuration (SQLite default, PostgreSQL ready)
- Static/Media files configuration
- Authentication settings
- Email configuration
- Security settings
- Timezone settings (default: UTC)

## Security Features

- CSRF protection
- Authentication required for all views
- Password validation
- Session security
- XSS protection

## API Documentation

Internal APIs for:
- Tender number generation
- ISO number generation
- Framework agreement management
- Vendor bid processing

## Dependencies

- Python 3.11+
- Django 4.x
- Bootstrap 5.3.0
- Other dependencies listed in requirements.txt

## Development

### Running Tests
```powershell
python manage.py test
```

### Code Style
The project follows PEP 8 guidelines. Run checks with:
```powershell
flake8 .
```

### Making Migrations
After model changes:
```powershell
python manage.py makemigrations
python manage.py migrate
```

## Support

For support or queries:
- Email: procurement@fda.gov.gh
- Phone: (+233)302233200
- Address: Nelson Mandela Avenue, Accra

## License
Copyright © 2025 Artemis Techologies. All rights reserved

## Contributors

- Emmanuel Oppong (killcode)
- Elliot Sarpong Menkah
- Procurement Unit
- External Contributors (See GitHub contributors)
