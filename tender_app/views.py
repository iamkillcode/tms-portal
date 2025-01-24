from django.shortcuts import render, redirect
from datetime import datetime
import pandas as pd
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import TenderTracker, Department, Category, Tender, ActivityLog, ISODetail
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import CustomUserCreationForm, ISODetailForm
from django.views.generic.edit import UpdateView
from .forms import TenderUpdateForm


# Tender number generator view
@login_required
def tender_generator_view(request):
    # Get all departments and categories
    departments = Department.objects.all()
    categories = Category.objects.all()

    # Initialize context
    context = {
        "department_codes": [
            {"id": dept.code, "text": dept.code} for dept in departments
        ],
        "category_data": [{"id": cat.code, "text": cat.name} for cat in categories],
    }

    if request.method == "POST":
        try:
            department_code = request.POST.get("department_code")
            category_code = request.POST.get("category_code")
            tender_description = request.POST.get("tender_description")
            procurement_type = request.POST.get("procurement_type")
            lot_number = request.POST.get("lot_number")
            amendment = request.POST.get("amendment")
            call_off = request.POST.get("call_off")

            if not all(
                [department_code, category_code, tender_description, procurement_type]
            ):
                raise ValidationError("All required fields must be filled")

            department = Department.objects.get(code=department_code)
            year = datetime.now().year
            sequence = TenderTracker.get_next_sequence(year)

            # Build tender number with proper formatting
            tender_number = f"FDA/{department_code}/{year}/{category_code}/{procurement_type}-{sequence:04d}"

            # Add optional components
            if lot_number:
                tender_number += f" ({lot_number})"
            if amendment:
                tender_number += f" ({amendment})"
            if call_off:
                tender_number += f" ({call_off})"

            # Create tender record
            tender = Tender.objects.create(
                tender_number=tender_number,
                description=tender_description,
                department=department,
                status="Pending",
                user=request.user,
                lot_number=lot_number,
                amendment=bool(amendment),
                call_off=bool(call_off),
            )

            # Create activity log
            ActivityLog.objects.create(
                officer=request.user,
                activity_description=f"Generated tender number {tender_number}",
                tender=tender,
            )

            context["tender_number"] = tender_number
            context["tender_description"] = tender_description
            messages.success(
                request, f"Successfully generated tender number: {tender_number}"
            )

        except ValidationError as e:
            messages.error(request, str(e))
        except Department.DoesNotExist:
            messages.error(request, "Invalid department selected")
        except Exception as e:
            messages.error(request, f"Error generating tender number: {str(e)}")

    return render(request, "tender_generator.html", context)


# ISO number generator view
@login_required
def generate_iso_number(request):
    if request.method == "POST":
        form = ISODetailForm(user=request.user, data=request.POST)
        if form.is_valid():
            tender = form.cleaned_data["tender"]
            iso_detail = form.save(commit=False)
            iso_detail.user = request.user
            iso_detail.division_name = tender.department.name
            iso_detail.department_name = tender.department.code
            iso_detail.procurement_type = form.cleaned_data["procurement_type"]
            iso_detail.year = datetime.now().year

            # The generate_iso_number method will be called automatically in save()
            iso_detail.save()

            messages.success(
                request, f"ISO Number {iso_detail.iso_number} generated successfully"
            )
            return redirect("tender_number_list")
    else:
        form = ISODetailForm(user=request.user)

    return render(request, "iso_number_generator.html", {"form": form})


@login_required
def iso_number_list_view(request):
    iso_numbers = (
        ISODetail.objects.filter(user=request.user)
        .select_related("user")
        .order_by("-created_at")
    )
    return render(
        request,
        "iso_number_list.html",
        {
            "iso_numbers": iso_numbers,
        },
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Tender


@login_required
def tender_number_list_view(request):
    tenders = Tender.objects.all().order_by("-created_at")
    context = {
        "tenders": tenders,
    }
    print(f"Number of tenders found: {tenders.count()}")  # Debug
    return render(request, "tender_number_list.html", context)

    return render(
        request,
        "tender_generator.html",
        {
            "tender_number": tender_number,
            "error": error,
            "department_codes": department_codes,
            "tender_description": tender_description,  # Pass the description to the template
            "category_data": category_data,
        },
    )


# Register view
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # Use the updated form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(
                "tender_generator"
            )  # Redirect to tender generator after registration
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(
                "tender_generator"
            )  # Redirect to a 'home' page after successful login
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


# Home view (after login)
def home_view(request):
    return render(request, "home.html")  # Create this template for your homepage


def custom_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def create_iso_detail(request):
    if request.method == "POST":
        form = ISODetailForm(user=request.user, data=request.POST)
        if form.is_valid():
            iso_detail = form.save(commit=False)
            iso_detail.user = request.user
            iso_detail.division_name = iso_detail.tender.department.name
            iso_detail.department_name = iso_detail.tender.department.code
            iso_detail.year = datetime.now().year
            iso_detail.save()
            messages.success(
                request,
                f"ISO Detail created successfully with ISO number {iso_detail.iso_number}",
            )
            return redirect("iso_number_list")
    else:
        form = ISODetailForm(user=request.user)
    return render(request, "create_iso_detail.html", {"form": form})


class TenderUpdateView(UpdateView):
    model = Tender
    form_class = TenderUpdateForm
    template_name = "tender_update.html"
    success_url = "/tender-number-list/"  # Redirect to tender list after update

    def form_valid(self, form):
        messages.success(self.request, "Tender updated successfully")
        return super().form_valid(form)


def redirect_to_home(request):
    return redirect("home")
