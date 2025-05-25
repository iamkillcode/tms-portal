# Consolidated CSS Structure

This directory contains the consolidated and organized CSS files for the Tender Management System.

## Files

- **main.css** - Core styles used across the entire application
- **admin.css** - Styles specific to the Django admin interface
- **tender.css** - Styles specific to tender management functionality
- **shop.css** - Styles specific to the breakfast shop functionality

## Usage

Include these files in templates as needed. The main.css should always be included first as it contains the core styles and variables used by other CSS files.

```html
<!-- Always include main.css first -->
<link rel="stylesheet" href="{% static 'css/consolidated/main.css' %}">

<!-- Then include module-specific CSS as needed -->
<link rel="stylesheet" href="{% static 'css/consolidated/tender.css' %}">
```

## CSS Organization

- **Variables** - Color schemes and key measurements are defined using CSS variables in main.css
- **Layout** - Core layout styles (body, container structure)
- **Components** - Reusable UI components (cards, buttons, etc)
- **Module-specific** - Styles that only apply to specific modules

## Benefits of Consolidation

- Reduced file size through elimination of duplicated styles
- Consistent look and feel through shared variables
- Better organization for easier maintenance
- Modular structure allows loading only necessary CSS
