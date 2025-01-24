from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from typing import Optional
from datetime import date

# Add at top of file with other constants
PROCUREMENT_TYPE_PREFIXES = {
    "Goods": "RFQ",
    "Works": "NCT",
    "Services": "RFP",
    "Consultancy": "RT",
}

DEPARTMENT = "CSD"  # Can be made configurable if needed


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
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    tender_number = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    amendment = models.CharField(max_length=10, blank=True, null=True)
    call_off = models.CharField(max_length=10, blank=True, null=True)
    category_type = models.CharField(max_length=100, blank=True, null=True)
    name_of_vendor_consultant = models.CharField(max_length=200, blank=True, null=True)
    date_of_contract = models.DateField(null=True, blank=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    invitation_date = models.DateField(null=True, blank=True)
    po_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_payment_memo = models.DateField(null=True, blank=True)
    file_no = models.CharField(max_length=100, blank=True, null=True)
    sra_certification_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_sra_certification = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    evaluation_date = models.DateField(null=True, blank=True)
    date_of_po = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.tender_number} by {self.user.username}"


# Tracks user profiles for extended user details
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150)

    def __str__(self):
        return self.full_name


# Tracks activity logs related to tenders
class ActivityLog(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    officer = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_description = models.TextField()
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.officer.username} - {self.tender.tender_number}"


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
