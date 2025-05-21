# Tender Management System (TMS) - Comprehensive User Guide

This guide provides detailed instructions on using the Tender Management System (TMS), a comprehensive web-based procurement management system for FDA Ghana. The system handles tender generation, vendor management, framework agreements, ISO number management, task management via the ToDo system, and includes additional utilities like a breakfast ordering system.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Dashboard Navigation](#dashboard-navigation)
3. [Tender Management](#tender-management)
4. [Item Management](#item-management)
5. [Vendor Bid Management](#vendor-bid-management)
6. [Framework Agreements](#framework-agreements)
7. [ISO Number Management](#iso-number-management)
8. [ToDo System](#todo-system)
9. [User Management](#user-management)
10. [Breakfast Ordering System](#breakfast-ordering-system)
11. [Reports and Analytics](#reports-and-analytics)
12. [Tips and Troubleshooting](#tips-and-troubleshooting)

## Getting Started

### System Requirements
- Modern web browser (Chrome, Firefox, Edge recommended)
- Internet connection
- User credentials provided by your administrator

### Accessing the System
1. Open your web browser
2. Navigate to the TMS URL (for local installation: http://127.0.0.1:8000)
3. Enter your username and password
4. Click "Sign In"

### First-time Login
1. Use the temporary credentials provided by your administrator
2. You'll be prompted to change your password after first login
3. Complete your user profile with required information
4. Review the welcome dashboard for system announcements

## Dashboard Navigation

The TMS features a modern, responsive interface with:

### Main Navigation Menu
- **Dashboard** - Overview and quick access to all modules
- **Tender Generator** - Create and manage tenders
- **Vendors** - Manage vendor information
- **Items** - Track items for procurement
- **Framework** - Manage framework agreements
- **ISO** - ISO number management
- **ToDo** - Task management system
- **Shop** - Breakfast ordering system
- **Reports** - Generate reports and analytics
- **Admin** - Administrative functions (admin users only)

### Dashboard Widgets
- **Recent Activity** - Shows latest actions in the system
- **My Tasks** - Quick access to your assigned tasks
- **Upcoming Deadlines** - Shows approaching tender deadlines
- **Quick Links** - Fast access to commonly used features
- **System Announcements** - Important system-wide notices
- **ToDo Cards** - Your most urgent ToDo items

### User Menu (Top-right)
- **Profile** - Access and edit your user profile
- **Settings** - Personal preferences for the system
- **Help** - Access user guides and support resources
- **Logout** - Securely exit the system

## Tender Management

### Creating a New Tender

1. **Access Tender Generator**
   - Click "Tender Generator" in the main menu
   - Or click "New Tender" from the dashboard

2. **Enter Basic Tender Information**
   - Select the department requesting the tender
   - Choose the appropriate category
   - Enter a descriptive title for the tender
   - Select tender type (Open/Restricted/Direct)
   - Set submission deadline

3. **Generate Tender Number**
   - Click "Generate Tender Number"
   - The system automatically creates a unique tender reference
   - Format: TMS-YYYY-DEPT-XXX (e.g., TMS-2025-ICT-001)

4. **Add Additional Details**
   - Enter tender description and scope
   - Set estimated budget (optional)
   - Upload tender documents (Terms of Reference, etc.)
   - Specify evaluation criteria

5. **Finalize Tender Creation**
   - Review all entered information
   - Click "Create Tender" to save
   - New tender appears in tender list with "Draft" status

### Managing Existing Tenders

1. **View Tender List**
   - Click "Tenders" > "List All" in main menu
   - Use filters to narrow down by department, date, or status

2. **Tender Status Management**
   - Draft: Initial creation, not yet published
   - Published: Open for vendor bids
   - Evaluation: Bids under review
   - Awarded: Winner selected
   - Completed: Tender process concluded
   - Cancelled: Tender terminated

3. **Edit Tender Details**
   - Open tender from list
   - Click "Edit" button
   - Make necessary changes
   - Save changes

4. **Tender Document Management**
   - Click "Documents" tab in tender view
   - Upload additional documents
   - Download existing documents
   - Track document versions

5. **Tender Activity Timeline**
   - View chronological history of all tender actions
   - Each action recorded with timestamp and user
   - Export activity log if required

### Exporting Tender Data

1. **Export Single Tender**
   - Open tender details page
   - Click "Export" button
   - Select export format (PDF, Excel)
   - Download generated file

2. **Batch Export Multiple Tenders**
   - Go to Tenders List
   - Use checkboxes to select multiple tenders
   - Click "Export Selected"
   - Choose export format
   - Download consolidated report

## Item Management

### Adding Items to Tenders

1. **Access Item Management**
   - Open a tender from the list
   - Click "Items" button or tab
   - Click "Add Item" button

2. **Enter Item Details**
   - Item name (clear, specific description)
   - Quantity required
   - Unit of measure (e.g., Each, Box, Kg)
   - Technical specifications
   - Estimated unit price (optional)

3. **Additional Item Information**
   - Brand preferences (if any)
   - Manufacturer requirements
   - Quality standards required
   - Warranty expectations
   - Delivery requirements

4. **Item Documentation**
   - Upload technical specification documents
   - Add reference images if applicable
   - Include any compliance certificates required

5. **Save Item**
   - Review all entered information
   - Click "Save Item" to add to tender
   - Item appears in the tender's items list

### Managing Existing Items

1. **View Items List**
   - Open tender details
   - Click "Items" tab
   - View all items in tabular format

2. **Edit Item Details**
   - Click on item name or "Edit" button
   - Modify required fields
   - Save changes

3. **Remove Items**
   - Select item(s) using checkboxes
   - Click "Remove Selected" button
   - Confirm deletion

4. **Item Comparison**
   - Select multiple items
   - Click "Compare" button
   - View side-by-side comparison of specifications

## Vendor Bid Management

### Recording Vendor Bids

1. **Access Bid Management**
   - Open tender details
   - Click "Bids" tab
   - Click "Record New Bid" button

2. **Select Vendor**
   - Choose from registered vendors list
   - Or click "Add New Vendor" if not in system

3. **Enter Bid Details**
   - Submission date
   - Quoted prices for each item
   - Currency (GHS, USD, EUR)
   - Delivery timeline
   - Warranty offered
   - Payment terms

4. **Technical Evaluation**
   - Score technical aspects as per criteria
   - Add evaluator comments
   - Upload supporting evaluation documents

5. **Financial Evaluation**
   - Enter financial scores
   - System calculates comparative cost analysis
   - Currency conversion at current exchange rates

6. **Save Bid**
   - Review all information
   - Click "Save Bid" button
   - Bid appears in bids list

### Comparing and Evaluating Bids

1. **Bid Comparison View**
   - From tender's Bid tab, click "Compare Bids"
   - View all bids in side-by-side comparison
   - Sort by different criteria (price, score, etc.)

2. **Technical Evaluation Worksheet**
   - Click "Technical Evaluation" button
   - Score each bid against predefined criteria
   - Calculate technical scores

3. **Financial Evaluation Worksheet**
   - Click "Financial Evaluation" button
   - Review normalized price comparisons
   - Score financial aspects

4. **Combined Evaluation**
   - System calculates combined technical/financial scores
   - Ranks vendors based on total scores
   - Highlights recommended winner

### Selecting Winning Bid

1. **Review Evaluation Results**
   - Open tender's Bid tab
   - Click "Evaluation Summary" button
   - Review all scores and rankings

2. **Mark Winning Bid**
   - Select winning bid
   - Click "Mark as Winner" button
   - Enter justification comments

3. **Notification Process**
   - System generates award notification
   - Option to email vendors with results
   - Record notification dates

4. **Documentation**
   - Upload award decision documents
   - Record approval signatures
   - Complete audit trail of selection process

## Framework Agreements

### Creating Framework Agreements

1. **Access Framework Management**
   - From main menu, click "Framework"
   - Or from tender with winning bid, click "Create Agreement"

2. **Select Vendor**
   - Choose from list of vendors
   - Or select directly from winning bid

3. **Agreement Details**
   - Enter agreement title
   - Set start and end dates
   - Specify agreement scope
   - Add financial limits if applicable

4. **Item Pricing**
   - Add items covered by agreement
   - Set agreed prices
   - Specify price validity periods
   - Add volume discount tiers if applicable

5. **Terms and Conditions**
   - Enter or upload agreement terms
   - Specify delivery conditions
   - Add quality requirements
   - Include renewal options

6. **Finalize Agreement**
   - Review all information
   - Click "Create Agreement"
   - Agreement status set to "Active"

### Managing Existing Agreements

1. **View Agreements List**
   - From main menu, click "Framework" > "List All"
   - Filter by vendor, status, or date range

2. **Monitor Agreement Status**
   - Active: Currently valid and usable
   - Expiring Soon: Approaching end date
   - Expired: Past end date
   - Terminated: Ended before natural expiration

3. **Agreement Renewal**
   - Open agreement details
   - Click "Renew Agreement"
   - Set new validity period
   - Update pricing if required
   - Save renewed agreement

4. **Terminating Agreements**
   - Open agreement details
   - Click "Terminate Agreement"
   - Enter termination reason
   - Specify termination date
   - Save changes

## ISO Number Management

### Generating ISO Numbers

1. **Access ISO Generator**
   - From main menu, click "ISO" > "Generator"
   - Or click "New ISO" from dashboard

2. **Enter ISO Document Information**
   - Select division (ICT, Procurement, etc.)
   - Choose document type
   - Enter document title
   - Select document classification

3. **Generate ISO Number**
   - Click "Generate ISO Number"
   - System creates unique ISO reference
   - Format: ISO-DIV-YYYY-XXX (e.g., ISO-ICT-2025-001)

4. **Add Document Details**
   - Enter document description
   - Set review/revision schedule
   - Add document owner
   - Upload document file

5. **Save ISO Record**
   - Review all entered information
   - Click "Create ISO Record"
   - New ISO appears in the list

### Managing ISO Documents

1. **View ISO List**
   - From main menu, click "ISO" > "List All"
   - Filter by division, year, or status

2. **Update ISO Status**
   - Draft: Initial creation
   - Review: Under review
   - Approved: Officially endorsed
   - Published: Released for use
   - Obsolete: No longer valid

3. **Document Version Control**
   - Open ISO record
   - Click "Add New Version"
   - Upload updated document
   - Add version notes
   - Previous versions remain accessible

4. **ISO Document Search**
   - Use search box in ISO section
   - Search by number, title, or content
   - Advanced filters available

## ToDo System

### Accessing the ToDo System

1. **Navigate to ToDo Dashboard**
   - From main menu, click "ToDo"
   - Or click on ToDo widget from main dashboard
   - View your task summary and priority tasks

2. **ToDo Dashboard Features**
   - Overview of all your ToDo lists
   - Tasks grouped by priority
   - Upcoming deadlines highlighted
   - Quick task creation button
   - Calendar view toggle

### Creating and Managing ToDo Lists

1. **Create a New ToDo List**
   - From ToDo dashboard, click "New List"
   - Enter list name (e.g., "Tender Evaluation Committee")
   - Add optional description
   - Choose color coding (optional)
   - Click "Create List"

2. **View ToDo Lists**
   - From ToDo dashboard, see all your lists
   - Click on a list name to view contained tasks
   - Lists show completion percentage

3. **Edit ToDo List**
   - Open list view
   - Click "Edit List" button
   - Modify name, description, or color
   - Save changes

4. **Delete ToDo List**
   - Open list view
   - Click "Delete List"
   - Confirm deletion (warning: deletes all tasks in list)

### Creating and Managing Tasks

1. **Create a New Task**
   - From list view, click "Add Task"
   - Or from ToDo dashboard, click "Quick Add"
   - Enter task title

2. **Task Details**
   - Add detailed description
   - Set priority level:
     - Low (Blue)
     - Medium (Yellow)
     - High (Orange)
     - Critical (Red)
   - Set status:
     - Not Started
     - In Progress
     - Completed
     - Deferred
   - Set due date and time
   - Set progress percentage (0-100%)

3. **Additional Task Options**
   - Assign task to ToDo list
   - Add tags for easier filtering
   - Set recurring schedule (daily, weekly, monthly)
   - Add reminders

4. **Save Task**
   - Review all information
   - Click "Create Task"
   - Task appears in your ToDo list

5. **Edit Task**
   - Click on task title to open details
   - Click "Edit" button
   - Update any details
   - Save changes

6. **Update Task Status**
   - From task list, use quick status dropdown
   - Or open task and change status field
   - Update progress percentage as work advances

7. **Delete Task**
   - Open task details
   - Click "Delete" button
   - Confirm deletion

### Task Comments and Attachments

1. **Adding Comments**
   - Open task details
   - Scroll to Comments section
   - Type comment in text box
   - Click "Add Comment"
   - Comments appear in chronological order

2. **File Attachments**
   - Open task details
   - Click "Add Attachment" button
   - Select file from your computer
   - Add optional description
   - Click "Upload"
   - File appears in Attachments list

3. **Viewing Attachments**
   - Click on attachment name to download
   - Preview supported for images and PDFs

4. **Managing Attachments**
   - Delete by clicking "Remove" next to attachment
   - Replace by uploading new version

### Using Tags

1. **Creating Tags**
   - From ToDo dashboard, click "Manage Tags"
   - Click "Add New Tag"
   - Enter tag name and select color
   - Save new tag

2. **Adding Tags to Tasks**
   - When creating or editing a task
   - Select tags from dropdown list
   - Multiple tags can be added to a task

3. **Filtering by Tags**
   - From ToDo dashboard or list view
   - Click on tag name in sidebar
   - View only tasks with that tag
   - Combine multiple tags for advanced filtering

### Calendar View

1. **Accessing Calendar**
   - From ToDo dashboard, click "Calendar" tab
   - Or from main menu, "ToDo" > "Calendar"

2. **Calendar Features**
   - Month, week, and day views
   - Tasks shown on due dates
   - Color-coded by priority
   - Click on date to see all tasks due

3. **Creating Tasks from Calendar**
   - Click on a date
   - Click "Add Task" on popup
   - Complete task details
   - Due date pre-filled from calendar

4. **Task Management from Calendar**
   - Click on task in calendar
   - Quick options to change status
   - Click "Details" for full task view

### Exporting ToDo Data

1. **Access Export Function**
   - From ToDo dashboard, click "Export"
   - Or from main menu, "ToDo" > "Export"

2. **Export Options**
   - Select date range
   - Choose lists to include
   - Filter by status, priority, or tags
   - Select export format (Excel, CSV, PDF)

3. **Generate and Download**
   - Click "Generate Export"
   - Review preview if available
   - Click "Download" to save file

## User Management

### Managing Your Profile

1. **Accessing Your Profile**
   - Click your username in top-right corner
   - Select "My Profile" from dropdown

2. **Updating Personal Information**
   - Edit name, email, phone number
   - Upload profile picture
   - Update department information
   - Save changes

3. **Changing Password**
   - Click "Change Password" in profile
   - Enter current password
   - Enter and confirm new password
   - Click "Update Password"

4. **Notification Preferences**
   - Set email notification preferences
   - Choose which system events trigger notifications
   - Save preference changes

### Role-Based Access

The system has several user roles with different permissions:

1. **Basic User**
   - View assigned tenders and tasks
   - Submit information for assigned tasks
   - Access personal dashboard
   - Use ToDo system for personal tasks

2. **Procurement Officer**
   - All Basic User permissions
   - Create and edit tenders
   - Record vendor bids
   - Generate ISO numbers
   - Create framework agreements

3. **Department Manager**
   - All Procurement Officer permissions
   - Approve tenders for department
   - View department-wide reports
   - Delegate tasks to team members

4. **System Administrator**
   - All permissions in the system
   - User management
   - System configuration
   - Access to audit logs

## Breakfast Ordering System

### Browsing Available Items

1. **Access Shop Section**
   - From main menu, click "Shop"
   - Or click "Breakfast Shop" from dashboard

2. **Browse Categories**
   - View items by category:
     - Beverages (Hot)
     - Beverages (Cold)
     - Snacks
     - Meals
   - Use search box to find specific items

3. **View Item Details**
   - Click on item image or name
   - See full description, price, and availability
   - View nutritional information if available

### Placing Orders

1. **Adding Items to Cart**
   - Click "Add to Cart" button
   - Specify quantity
   - Add any special instructions
   - Item added to shopping cart

2. **Managing Shopping Cart**
   - Click cart icon in top-right
   - Review all items in cart
   - Adjust quantities or remove items
   - See order subtotal

3. **Checkout Process**
   - Click "Proceed to Checkout"
   - Confirm delivery location (office/desk number)
   - Select preferred delivery time
   - Add any order notes

4. **Payment Options**
   - Select payment method:
     - Department charge
     - Personal payment
     - Mobile money
   - Complete payment process
   - Receive order confirmation

5. **Order Tracking**
   - View order status in "My Orders" section
   - Statuses: Confirmed, Preparing, Ready for Pickup, Delivered
   - Receive notifications when order status changes

## Reports and Analytics

### Accessing Reports

1. **Navigate to Reports Section**
   - From main menu, click "Reports"
   - View available report categories

2. **Report Categories**
   - Tender Reports
   - Vendor Performance Reports
   - Financial Reports
   - ISO Document Reports
   - ToDo Productivity Reports
   - System Usage Reports

### Generating Reports

1. **Select Report Type**
   - Click desired report category
   - Choose specific report from list

2. **Set Report Parameters**
   - Select date range
   - Choose departments to include
   - Set other filtering criteria
   - Select grouping options

3. **Generate and View Report**
   - Click "Generate Report"
   - View results on screen
   - Interactive charts and tables available
   - Drill down for detailed information

4. **Export Report**
   - Click "Export" button
   - Choose format (Excel, PDF, CSV)
   - Download generated file
   - Option to schedule recurring reports

### Dashboard Analytics

1. **Main Dashboard Metrics**
   - Key performance indicators
   - Trend charts for tenders and procurements
   - Department activity comparisons
   - ToDo completion rates

2. **Custom Dashboards**
   - Create personalized dashboard views
   - Add/remove widgets
   - Set refresh intervals
   - Save custom views

## Tips and Troubleshooting

### Best Practices

1. **Regular Updates**
   - Update task status regularly in ToDo system
   - Keep tender information current
   - Review framework agreements before expiration

2. **Documentation**
   - Attach all relevant documents to tenders
   - Add detailed comments to tasks
   - Document bid evaluation decisions

3. **Efficiency Tips**
   - Use keyboard shortcuts (see Help > Shortcuts)
   - Set up saved searches for common filters
   - Create task templates for recurring processes

### Common Issues and Solutions

1. **Login Problems**
   - If unable to log in, try resetting password
   - Check for caps lock being on
   - Contact administrator if problems persist

2. **Missing Data**
   - Refresh browser if data seems incomplete
   - Check filters that may be hiding information
   - Verify your access permissions for that data

3. **Export Issues**
   - Try a different export format
   - Reduce data size by applying filters
   - Check download folder for completed exports

### Getting Help

1. **In-System Help**
   - Click "Help" in main menu
   - Search help topics
   - View video tutorials
   - Access quick reference guides

2. **Contact Support**
   - Email: procurement@fda.gov.gh
   - Phone: (+233)302233200
   - Internal extension: 1234

3. **Feedback and Suggestions**
   - Use "Feedback" button in footer
   - Submit enhancement requests
   - Report bugs or issues

---

© 2025 Artemis Technologies. All rights reserved.
This guide is provided exclusively for authorized users of the Tender Management System.
