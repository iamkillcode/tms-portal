from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from typing import Optional
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver

# Add at top of file with other constants
PROCUREMENT_TYPE_PREFIXES = {
    "Goods": "RFQ",
    "Works": "NCT",
    "Services": "RFP",
    "Consultancy": "RT",
}

DEPARTMENT = "CSD"  # Can be made configurable if needed

ROLE_CHOICES = [
    ("admin", "Administrator"),
    ("officer", "Procurement Officer"),
    ("viewer", "Viewer"),
]


# Tracks the sequence of tender numbers for each year
class TenderTracker(models.Model):
    year = models.IntegerField(unique=True)  # Ensures one entry per year
    last_sequence = models.IntegerField(default=0)  # Sequence counter

    def __str__(self):
        return f"{self.year} - {self.last_sequence}"

    @classmethod
    def get_next_sequence(cls, year):
        tracker, created = cls.objects.get_or_create(year=year)
        tracker.last_sequence += 1
        tracker.save()
        return tracker.last_sequence


# Represents a department in the system
class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Represents a category, e.g., A.4.1
class Category(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Represents an individual tender
class Tender(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    PROCUREMENT_TYPE_CHOICES = [
        ("Goods", "Goods"),
        ("Works", "Works"),
        ("Services", "Services"),
        ("Consultancy", "Consultancy"),
    ]

    # Basic Information
    tender_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    procurement_type = models.CharField(
        max_length=20, choices=PROCUREMENT_TYPE_CHOICES, default="Goods"
    )
    estimated_value = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    currency = models.CharField(max_length=3, default="USD")

    # Relationships
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tenders"
    )
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, related_name="tenders"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tenders",
    )

    # Status and Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # Document References
    amendment = models.CharField(max_length=10, blank=True, null=True)
    call_off = models.CharField(max_length=10, blank=True, null=True)
    category_type = models.CharField(max_length=100, blank=True, null=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    file_no = models.CharField(max_length=100, blank=True, null=True)
    po_number = models.CharField(max_length=100, blank=True, null=True)

    # Vendor Information
    name_of_vendor_consultant = models.CharField(max_length=200, blank=True, null=True)
    vendor_email = models.EmailField(blank=True, null=True)
    vendor_phone = models.CharField(max_length=20, blank=True, null=True)

    # Important Dates
    invitation_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    evaluation_date = models.DateField(null=True, blank=True)
    date_of_contract = models.DateField(null=True, blank=True)
    date_of_po = models.DateField(null=True, blank=True)
    date_of_payment_memo = models.DateField(null=True, blank=True)

    # Certification
    sra_certification_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_sra_certification = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Tender"
        verbose_name_plural = "Tenders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["tender_number"]),
            models.Index(fields=["department"]),
        ]
        permissions = [
            ("can_approve_tender", "Can approve tender"),
            ("can_reject_tender", "Can reject tender"),
            ("can_view_all_tenders", "Can view all tenders"),
        ]

    def __str__(self) -> str:
        return f"{self.tender_number} - {self.title}"

    def clean(self) -> None:
        """Validate tender data."""
        if self.closing_date and self.invitation_date:
            if self.closing_date < self.invitation_date:
                raise ValidationError(
                    {
                        "closing_date": "Closing date cannot be earlier than invitation date"
                    }
                )

        if self.evaluation_date and self.closing_date:
            if self.evaluation_date < self.closing_date:
                raise ValidationError(
                    {
                        "evaluation_date": "Evaluation date cannot be earlier than closing date"
                    }
                )

    def save(self, *args, **kwargs) -> None:
        """Override save to perform additional operations."""
        if not self.pk and not self.tender_number:
            # Generate tender number for new tenders
            year = date.today().year
            sequence = TenderTracker.get_next_sequence(year)
            prefix = PROCUREMENT_TYPE_PREFIXES.get(self.procurement_type, "NCT")
            self.tender_number = f"{prefix}/{year}/{sequence:04d}"

        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Get the absolute URL for the tender detail view."""
        from django.urls import reverse

        return reverse("tender_detail", kwargs={"pk": self.pk})


# Tracks user profiles for extended user details
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")
    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff_members",
    )
    phone_number = models.CharField(max_length=20, blank=True)
    is_account_active = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.full_name} ({self.role})"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ["full_name"]

    def clean(self) -> None:
        if not self.full_name:
            raise ValidationError({"full_name": "Full name is required"})

        if self.role == "admin" and not self.user.is_staff:
            self.user.is_staff = True
            self.user.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs) -> None:
    """Create or update user profile when user is created/updated."""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()


# Tracks activity logs related to tenders
class SystemActivityLog(models.Model):
    """Model to track user activities in the system."""

    ACTION_CHOICES = [
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("view", "View"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, default="other")
    target_model = models.CharField(max_length=100, blank=True, default="")
    target_id = models.IntegerField(null=True, blank=True)
    description = models.TextField(default="No description provided")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

    class Meta:
        ordering = ["-timestamp"]


class ISOTracker(models.Model):
    year = models.IntegerField(unique=True)
    last_sequence = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.year} - Sequence: {self.last_sequence}"


class ISODetail(models.Model):
    iso_number = models.CharField(max_length=255, unique=True)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    division_name = models.CharField(max_length=255)
    department_name = models.CharField(max_length=255)
    procurement_type = models.CharField(max_length=255)
    year = models.IntegerField()
    sequential_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    number = models.IntegerField(default=1)

    def __str__(self):
        return self.iso_number

    def save(self, *args, **kwargs):
        if not self.pk:  # Only for new records
            # Get latest number for current year
            latest = (
                ISODetail.objects.filter(created_at__year=date.today().year)
                .order_by("-number")
                .first()
            )

            next_number = latest.number + 1 if latest else 1
            self.number = next_number
            self.sequential_number = (
                next_number  # Set sequential_number to same as number
            )

            if not self.iso_number:
                self.iso_number = self.generate_iso_number()

        super().save(*args, **kwargs)

    def generate_iso_number(self) -> str:
        """
        Generate ISO number in format: FDA/CSD/PSD/YY/NCT-XXXX
        FDA - Organization name (fixed)
        CSD - Division name
        PSD - Department name
        YY - Current year
        NCT - Procurement Type
        XXXX - Sequential number
        """
        year = str(date.today().year)[-2:]
        proc_prefix = PROCUREMENT_TYPE_PREFIXES.get(self.procurement_type, "NCT")

        # Extract first part of division/department names if they contain multiple parts
        department_code = "PSD"
        division_code = "CSD"

        return f"FDA/{division_code}/{department_code}/{proc_prefix}/{year}/{str(self.number).zfill(4)}"

    def get_tender_number(self):
        return self.tender.tender_number if self.tender else "N/A"
