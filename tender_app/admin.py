from django.contrib import admin
from .models import TenderTracker, Department, Tender


@admin.register(TenderTracker)
class TenderTrackerAdmin(admin.ModelAdmin):
    list_display = ('year', 'last_sequence')
    list_filter = ('year',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ('tender_number', 'user', 'description', 'department', 'created_at')
    search_fields = ('tender_number', 'user__username', 'description', 'department__name')
    list_filter = ('created_at', 'department')
    readonly_fields = ('tender_number', 'user', 'created_at')  # Make non-editable fields readonly

    def get_full_name(self, obj):
        return obj.user.profile.full_name  # Access the UserProfile full_name
    get_full_name.short_description = "Officer's Full Name"
    
    def save_model(self, request, obj, form, change):
        # Automatically link the user (officer) creating the tender
        if not obj.pk:  # Only on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)
