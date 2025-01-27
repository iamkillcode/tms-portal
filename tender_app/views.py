from django.shortcuts import render, redirect
from datetime import datetime
import pandas as pd
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib import messages
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import TemplateView, ListView, DetailView
from .models import (
    TenderTracker,
    Department,
    Category,
    Tender,
    SystemActivityLog,
    ISODetail,
    UserProfile,
)
from .forms import (
    CustomUserCreationForm,
    ISODetailForm,
    TenderUpdateForm,
    UserProfileForm,
    TenderFilterForm,
    TenderForm,
)
from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods


def get_client_ip(request):
    """Get the client's IP address from the request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


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
            SystemActivityLog.objects.create(
                user=request.user,
                action="generate",
                target_model="tender",
                target_id=tender.id,
                description=f"Generated tender number {tender_number}",
                ip_address=get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
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
            return redirect("iso_number_list")
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


# Register view with admin approval
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Require admin approval
            user.save()

            # Create user profile without department
            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data.get("full_name"),
                phone_number=form.cleaned_data.get("phone_number"),
            )

            messages.success(request, "Registration successful. Await admin approval.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/register.html", {"form": form})


# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Account not activated. Await admin approval.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# Home view with dashboard
@login_required
def home_view(request):
    tender_count = Tender.objects.count()
    user_count = User.objects.filter(is_active=True).count()
    recent_activity = SystemActivityLog.objects.filter(target_model="tender").order_by(
        "-timestamp"
    )[:5]
    return render(
        request,
        "home.html",
        {
            "tender_count": tender_count,
            "user_count": user_count,
            "recent_activity": recent_activity,
        },
    )


# User profile view
@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, "profile.html", {"form": form})


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


class TenderUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for editing an existing tender.
    """

    model = Tender
    form_class = TenderForm
    template_name = "tender/form.html"

    def get_success_url(self):
        """Get URL to redirect to after successful edit."""
        return reverse_lazy("tender_detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        """Get the tender object and check permissions."""
        tender = super().get_object(queryset)
        user = self.request.user

        # Check if user has permission to edit this tender
        if user.profile.role != "admin" and user != tender.user:
            raise PermissionDenied("You don't have permission to edit this tender.")

        return tender

    def form_valid(self, form):
        """Handle valid form submission."""
        response = super().form_valid(form)

        # Log activity
        SystemActivityLog.objects.create(
            user=self.request.user,
            action="update",
            target_model="tender",
            target_id=self.object.id,
            description=f"Updated tender {self.object.tender_number}",
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
        )

        messages.success(self.request, "Tender updated successfully.")
        return response

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(
            self.request,
            "There was an error updating the tender. Please check the form and try again.",
        )
        return super().form_invalid(form)


class TenderDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a tender.
    """

    model = Tender
    success_url = reverse_lazy("tender_list")
    template_name = "tender/delete.html"

    def get_object(self, queryset=None):
        """Get the tender object and check permissions."""
        tender = super().get_object(queryset)
        user = self.request.user

        # Only admins can delete tenders
        if user.profile.role != "admin":
            raise PermissionDenied("You don't have permission to delete tenders.")

        return tender

    def delete(self, request, *args, **kwargs):
        """Handle tender deletion."""
        tender = self.get_object()
        tender_number = tender.tender_number

        # Log activity before deletion
        SystemActivityLog.objects.create(
            user=self.request.user,
            action="delete",
            target_model="tender",
            target_id=tender.id,
            description=f"Deleted tender {tender_number}",
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
        )

        messages.success(request, f"Tender {tender_number} deleted successfully.")
        return super().delete(request, *args, **kwargs)


class TenderCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new tender.
    """

    model = Tender
    form_class = TenderForm
    template_name = "tender/form.html"
    success_url = reverse_lazy("tender_list")

    def form_valid(self, form):
        """Handle valid form submission."""
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Log activity
        SystemActivityLog.objects.create(
            user=self.request.user,
            action="create",
            target_model="tender",
            target_id=self.object.id,
            description=f"Created tender {self.object.tender_number}",
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
        )

        messages.success(self.request, "Tender created successfully.")
        return response

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(
            self.request,
            "There was an error creating the tender. Please check the form and try again.",
        )
        return super().form_invalid(form)


class HomeView(LoginRequiredMixin, TemplateView):
    """
    View for the home page dashboard.
    Shows statistics and recent activity for the logged-in user.
    """

    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Get context data for the home page."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get tender statistics
        context["total_tenders"] = Tender.objects.count()
        context["pending_tenders"] = Tender.objects.filter(status="pending").count()
        context["completed_tenders"] = Tender.objects.filter(status="completed").count()
        context["user_tenders"] = Tender.objects.filter(user=user).count()

        # Get recent activities
        if user.profile.role == "admin":
            # Admins see all activities
            activities = SystemActivityLog.objects.filter(
                target_model="tender"
            ).order_by("-timestamp")[:10]
        else:
            # Users see activities related to their department
            activities = SystemActivityLog.objects.filter(
                target_model="tender",
                target_id__in=Tender.objects.filter(
                    department=user.profile.department
                ).values_list("id", flat=True),
            ).order_by("-timestamp")[:10]

        context["recent_activities"] = activities
        return context


class RegisterView(CreateView):
    """
    View for user registration.
    Creates a new user account and profile.
    """

    template_name = "auth/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """Handle valid form submission."""
        response = super().form_valid(form)
        user = form.save()

        # Log the user in
        login(self.request, user)

        messages.success(
            self.request,
            "Your account has been created successfully. Please wait for admin approval.",
        )

        return response

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(
            self.request,
            "There was an error with your registration. Please check the form and try again.",
        )
        return super().form_invalid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    """
    View for user profile management.
    Allows users to update their profile information.
    """

    template_name = "profile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        """Get the user's profile."""
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """Get context data for the profile page."""
        context = super().get_context_data(**kwargs)

        # Get user's recent activities
        context["recent_activities"] = SystemActivityLog.objects.filter(
            target_model="user", target_id=self.request.user.id
        ).order_by("-timestamp")[:10]

        return context

    def form_valid(self, form):
        """Handle valid form submission."""
        response = super().form_valid(form)
        messages.success(self.request, "Profile updated successfully.")
        return response

    def form_invalid(self, form):
        """Handle invalid form submission."""
        messages.error(
            self.request,
            "There was an error updating your profile. Please check the form and try again.",
        )
        return super().form_invalid(form)


class TenderListView(LoginRequiredMixin, ListView):
    """
    View for displaying a list of tenders with filtering and pagination.
    """

    model = Tender
    template_name = "tender/list.html"
    context_object_name = "tenders"
    paginate_by = 10

    def get_queryset(self):
        """Get the list of tenders based on filters."""
        queryset = Tender.objects.select_related("user", "department").order_by(
            "-created_at"
        )

        # Apply filters based on user role
        user = self.request.user
        if user.profile.role != "admin":
            # Non-admin users can only see their own tenders or their department's tenders
            queryset = queryset.filter(
                Q(user=user) | Q(department=user.profile.department)
            )

        # Get filter form
        form = TenderFilterForm(self.request.GET)
        if form.is_valid():
            filters = {}

            # Search filter
            search = form.cleaned_data.get("search")
            if search:
                queryset = queryset.filter(
                    Q(tender_number__icontains=search)
                    | Q(title__icontains=search)
                    | Q(description__icontains=search)
                )

            # Department filter
            department = form.cleaned_data.get("department")
            if department:
                filters["department"] = department

            # Status filter
            status = form.cleaned_data.get("status")
            if status:
                filters["status"] = status

            # Date range filter
            date_from = form.cleaned_data.get("date_from")
            date_to = form.cleaned_data.get("date_to")
            if date_from:
                filters["created_at__gte"] = date_from
            if date_to:
                filters["created_at__lte"] = date_to

            # Apply filters
            if filters:
                queryset = queryset.filter(**filters)

            # Apply sorting
            sort_by = form.cleaned_data.get("sort_by")
            if sort_by:
                queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        """Get the context data for the template."""
        context = super().get_context_data(**kwargs)
        context["filter_form"] = TenderFilterForm(self.request.GET)
        return context


class TenderDetailView(LoginRequiredMixin, DetailView):
    """
    View for displaying tender details.
    Shows tender information and activity log.
    """

    model = Tender
    template_name = "tender/detail.html"
    context_object_name = "tender"

    def get_object(self, queryset=None):
        """Get the tender object and check permissions."""
        tender = super().get_object(queryset)
        user = self.request.user

        # Check if user has permission to view this tender
        if (
            user.profile.role != "admin"
            and user != tender.user
            and user.profile.department != tender.department
        ):
            raise PermissionDenied("You don't have permission to view this tender.")

        return tender

    def get_context_data(self, **kwargs):
        """Get context data for the template."""
        context = super().get_context_data(**kwargs)

        # Get tender activities
        context["activities"] = (
            SystemActivityLog.objects.filter(
                target_model="tender", target_id=self.object.id
            )
            .select_related("user", "user__profile")
            .order_by("-timestamp")
        )

        # Log view activity
        SystemActivityLog.objects.create(
            user=self.request.user,
            action="view",
            target_model="tender",
            target_id=self.object.id,
            description=f"Viewed tender {self.object.tender_number}",
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
        )

        return context


class DepartmentListView(LoginRequiredMixin, ListView):
    """View for listing departments."""

    model = Department
    template_name = "tender/department_list.html"
    context_object_name = "departments"

    def get(self, request, *args, **kwargs):
        """Return departments as JSON for API requests."""
        departments = list(Department.objects.values("id", "code", "name"))
        return JsonResponse({"departments": departments})


class CategoryListView(LoginRequiredMixin, ListView):
    """View for listing categories."""

    model = Category
    template_name = "tender/category_list.html"
    context_object_name = "categories"

    def get(self, request, *args, **kwargs):
        """Return categories as JSON for API requests."""
        categories = list(Category.objects.values("id", "code", "name"))
        return JsonResponse({"categories": categories})
