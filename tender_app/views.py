from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import TenderTracker, Department
from .forms import RegisterForm

# Tender number generator view
@login_required
def tender_generator_view(request):
    tender_number = None
    error = None
    tender_description = None  # Variable to hold the description

    if request.method == "POST":
        try:
            # Get form inputs
            department_code = request.POST.get("department_code")
            category_code = request.POST.get("category_code")
            procurement_type = request.POST.get("procurement_type")
            tender_description = request.POST.get("tender_description")  # Get the description field

            prefix = "FDA"
            year = datetime.now().year

            # Retrieve or create a tracker for the current year
            tracker, created = TenderTracker.objects.get_or_create(
                year=year,
                defaults={'last_sequence': 0}  # Initialize sequence if new
            )

            # Increment the global sequence
            tracker.last_sequence += 1
            tracker.save()

            # Generate the tender number
            sequential_number = f"{tracker.last_sequence:04}"  # Zero-padded to 4 digits
            tender_number = f"{prefix}/{department_code}/{year}/{category_code}/{procurement_type}-{sequential_number}"

        except Exception as e:
            error = str(e)

    # Fetch department codes for the dropdown
    department_codes = Department.objects.values_list('code', flat=True)

    return render(request, "tender_generator.html", {
        "tender_number": tender_number,
        "error": error,
        "department_codes": department_codes,
        "tender_description": tender_description  # Pass the description to the template
    })

# Register view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('tender_generator')  # Redirect to a 'home' page after successful registration
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tender_generator')  # Redirect to a 'home' page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Home view (after login)
def home_view(request):
    return render(request, 'home.html')  # Create this template for your homepage
