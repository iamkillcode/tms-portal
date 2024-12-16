
from django.contrib import admin
from .models import TenderTracker

@admin.register(TenderTracker)
class TenderTrackerAdmin(admin.ModelAdmin):
    list_display = ('year', 'procurement_type', 'last_sequence')
