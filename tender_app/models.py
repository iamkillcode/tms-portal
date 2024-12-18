from django.db import models
from django.contrib.auth.models import User


class TenderTracker(models.Model):
    year = models.IntegerField(unique=True)  # Ensures one entry per year
    last_sequence = models.IntegerField(default=0)  # sequence counter

    def __str__(self):
        return f"{self.year} - {self.last_sequence}"

    @classmethod
    def get_next_sequence(cls, year):
        tracker, created = cls.objects.get_or_create(year=year)
        tracker.last_sequence += 1
        tracker.save()
        return tracker.last_sequence


class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Tender(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to registered users
    tender_number = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)  # Track department
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tender_number} by {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150)

    def __str__(self):
        return self.full_name
from django.db import models

class Category(models.Model):
    code = models.CharField(max_length=10, unique=True)  # e.g., A.4.1
    name = models.CharField(max_length=255)  # e.g., Category Name

    def __str__(self):
        return f"{self.code} - {self.name}"