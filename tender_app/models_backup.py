# filepath: c:\Users\USER\Desktop\Dev\tender\tender_app\models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class TenderTracker(models.Model):
    MONTH_CHOICES = [
        ('JAN', 'January'),
        ('FEB', 'February'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'June'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December'),
    ]
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=3, choices=MONTH_CHOICES)
    sequence = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['department', 'year', 'month']

class Tender(models.Model):
    CATEGORY_CHOICES = [
        ('Goods', 'Goods'),
        ('Technical Service', 'Technical Service'),
        ('Consultancy', 'Consultancy'),
        ('Works', 'Works'),
    ]
    
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    CURRENCY_CHOICES = [
        ('GHS', 'GHS'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]

    # Existing fields
    tender_number = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # New fields
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    requests_aggregated = models.IntegerField(default=0)
    invitation_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    evaluation_date = models.DateField(null=True, blank=True)
    contract_date = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='GHS')
    contract_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    vendor_name = models.CharField(max_length=200, blank=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.SET_NULL, null=True, blank=True, related_name='tenders')
    po_date = models.DateField(null=True, blank=True)
    po_number = models.CharField(max_length=100, blank=True)
    sra_date = models.DateField(null=True, blank=True)
    sra_number = models.CharField(max_length=100, blank=True)
    payment_memo_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.tender_number} - {self.description[:50]}"
