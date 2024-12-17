
from django.contrib import admin
from .models import TenderTracker, Department, Tender



admin.site.register(Department)
admin.site.register(Tender)

@admin.register(TenderTracker)
class TenderTrackerAdmin(admin.ModelAdmin):
    list_display = ('year', 'last_sequence')
