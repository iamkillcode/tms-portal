from django.contrib import admin
from .models import (
    TenderTracker,
    Department,
    Tender,
    ActivityLog,
    ISODetail,
    ISOTracker,
)
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from django.utils.timezone import localtime
from typing import Optional, Sequence, Any


@admin.register(TenderTracker)
class TenderTrackerAdmin(admin.ModelAdmin):
    list_display = ("year", "last_sequence")
    list_filter = ("year",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")

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
    list_display = ("date", "officer", "activity_description", "tender")
    search_fields = (
        "officer__username",
        "activity_description",
        "tender__tender_number",
    )
    list_filter = ("date", "officer", "tender")
    actions = ["export_to_csv", "export_to_excel"]

    # Custom action to export selected activity logs to CSV
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="activity_logs.csv"'

        writer = csv.writer(response)
        writer.writerow(["Date", "Officer", "Activity Description", "Tender"])
        for log in queryset:
            writer.writerow(
                [
                    log.date,
                    log.officer.username,
                    log.activity_description,
                    log.tender.tender_number,
                ]
            )
        return response

    export_to_csv.short_description = "Export selected activity logs to CSV"

    # Custom action to export selected activity logs to Excel
    def export_to_excel(self, request, queryset):
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="activity_logs.xlsx"'

        wb = Workbook()
        ws = wb.active
        ws.title = "Activity Logs"

        # Write header
        headers = ["Date", "Officer", "Activity Description", "Tender"]
        ws.append(headers)

        # Write data
        for log in queryset:
            ws.append(
                [
                    log.date,
                    log.officer.username,
                    log.activity_description,
                    log.tender.tender_number,
                ]
            )

        wb.save(response)
        return response

    export_to_excel.short_description = "Export selected activity logs to Excel"


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = (
        "tender_number",
        "user",
        "description",
        "department",
        "created_at",
        "status",
    )
    search_fields = (
        "tender_number",
        "user__username",
        "description",
        "department__name",
    )
    list_filter = ("created_at", "department", "status")
    readonly_fields = (
        "tender_number",
        "user",
        "created_at",
    )  # Make non-editable fields readonly
    actions = ["mark_as_approved", "export_to_csv", "export_to_excel"]

    # Custom action to mark selected tenders as approved
    def mark_as_approved(self, request, queryset):
        updated = queryset.update(status="Approved")
        self.message_user(request, f"{updated} tender(s) marked as approved.")

    mark_as_approved.short_description = "Mark selected tenders as Approved"

    # Custom action to export selected tenders to CSV
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="tenders.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "Tender Number",
                "User",
                "Description",
                "Department",
                "Created At",
                "Status",
            ]
        )
        for tender in queryset:
            writer.writerow(
                [
                    tender.tender_number,
                    tender.user.username,
                    tender.description,
                    tender.department.name if tender.department else "",
                    tender.created_at,
                    tender.status,
                ]
            )
        return response

    export_to_csv.short_description = "Export selected tenders to CSV"

    # Custom action to export selected tenders to Excel
    def export_to_excel(self, request, queryset):
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="tenders.xlsx"'

        wb = Workbook()
        ws = wb.active
        ws.title = "Tenders"

        # Write header
        headers = [
            "Tender Number",
            "User",
            "Description",
            "Department",
            "Created At",
            "Status",
        ]
        ws.append(headers)

        # Write data
        for tender in queryset:
            created_at_naive = localtime(tender.created_at).replace(tzinfo=None)
            ws.append(
                [
                    tender.tender_number,
                    tender.user.username,
                    tender.description,
                    tender.department.name if tender.department else "",
                    created_at_naive,
                    tender.status,
                ]
            )

        wb.save(response)
        return response

    export_to_excel.short_description = "Export selected tenders to Excel"

    # Add date hierarchy
    date_hierarchy = "created_at"

    # Add more list filters
    list_filter = (
        "created_at",
        "department",
        "status",
        "category_type",
        "amendment",
        "call_off",
    )

    # Add search fields
    search_fields = (
        "tender_number",
        "user__username",
        "user__email",
        "description",
        "department__name",
        "name_of_vendor_consultant",
    )

    # Add fieldsets for better organization
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "tender_number",
                    "user",
                    "description",
                    "department",
                    "status",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "invitation_date",
                    "closing_date",
                    "evaluation_date",
                    "date_of_contract",
                )
            },
        ),
        (
            "Financial Details",
            {"fields": ("currency_of_payment", "contract_amount", "amount_to_be_paid")},
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "category_type",
                    "name_of_vendor_consultant",
                    "file_name",
                    "file_no",
                )
            },
        ),
        ("Flags", {"fields": ("amendment", "call_off")}),
    )

    def save_model(self, request: Any, obj: Any, form: Any, change: bool) -> None:
        """Override save_model to set user on creation."""
        if not change:  # Only on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(
        self, request: Any, obj: Optional[Any] = None
    ) -> Sequence[str]:
        """Dynamic readonly fields based on object state."""
        if obj:  # Editing existing object
            return self.readonly_fields + ("tender_number",)
        return self.readonly_fields


@admin.register(ISOTracker)
class ISOTrackerAdmin(admin.ModelAdmin):
    list_display = ("year", "last_sequence")
    list_filter = ("year",)


@admin.register(ISODetail)
class ISODetailAdmin(admin.ModelAdmin):
    list_display = (
        "iso_number",
        "user",
        "division_name",
        "department_name",
        "procurement_type",
        "year",
        "tender",  # Replace sequential_number with tender
        "created_at",
    )
    search_fields = (
        "iso_number",
        "user__username",
        "division_name",
        "department_name",
        "procurement_type",
    )
    list_filter = ("year", "division_name", "department_name", "procurement_type")
