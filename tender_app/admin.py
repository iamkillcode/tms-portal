from django.contrib import admin
from .models import TenderTracker, Department, Tender, ActivityLog
import csv
from django.http import HttpResponse
from openpyxl import Workbook


@admin.register(TenderTracker)
class TenderTrackerAdmin(admin.ModelAdmin):
    list_display = ('year', 'last_sequence')
    list_filter = ('year',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

    def get_full_name(self, obj):
        return obj.user.profile.full_name  # Access the UserProfile full_name
    get_full_name.short_description = "Officer's Full Name"
    
    def save_model(self, request, obj, form, change):
        # Automatically link the user (officer) creating the tender
        if not obj.pk:  # Only on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)
        
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'officer', 'activity_description', 'tender')
    search_fields = ('officer__username', 'activity_description', 'tender__tender_number')
    list_filter = ('date', 'officer', 'tender')
    
@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ('tender_number', 'user', 'description', 'department', 'created_at', 'status')
    search_fields = ('tender_number', 'user__username', 'description', 'department__name')
    list_filter = ('created_at', 'department', 'status')
    readonly_fields = ('tender_number', 'user', 'created_at')  # Make non-editable fields readonly
    actions = ['mark_as_approved', 'export_to_csv', 'export_to_excel']

    # Custom action to mark selected tenders as approved
    def mark_as_approved(self, request, queryset):
        updated = queryset.update(status='Approved')
        self.message_user(request, f"{updated} tender(s) marked as approved.")
    mark_as_approved.short_description = "Mark selected tenders as Approved"

    # Custom action to export selected tenders to CSV
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tenders.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Tender Number', 'User', 'Description', 'Department', 'Created At', 'Status'])
        for tender in queryset:
            writer.writerow([
                tender.tender_number,
                tender.user.username,
                tender.description,
                tender.department.name if tender.department else '',
                tender.created_at,
                tender.status,
            ])
        return response
    export_to_csv.short_description = "Export selected tenders to CSV"

    # Custom action to export selected tenders to Excel
    def export_to_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="tenders.xlsx"'

        wb = Workbook()
        ws = wb.active
        ws.title = "Tenders"

        # Write header
        headers = ['Tender Number', 'User', 'Description', 'Department', 'Created At', 'Status']
        ws.append(headers)

        # Write data
        for tender in queryset:
            ws.append([
                tender.tender_number,
                tender.user.username,
                tender.description,
                tender.department.name if tender.department else '',
                tender.created_at,
                tender.status,
            ])

        wb.save(response)
        return response
    export_to_excel.short_description = "Export selected tenders to Excel"
