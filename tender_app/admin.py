from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponse
from datetime import datetime, timedelta
import csv
from .models import (
    TenderTracker, Department, Tender, Category, UserProfile, 
    BreakfastItem, Order, OrderItem, Division, ISOTracker, ISONumber,
    TenderItem, VendorBid, FrameworkAgreement, Vendor, Chemical, ChemicalSpecification
)

# Customize admin site header and title
admin.site.site_header = "Tender Management System"
admin.site.site_title = "TMS Admin"
admin.site.index_title = "Welcome to TMS Admin"

class CustomUserAdmin(UserAdmin):
    actions = ['delete_selected']
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete users
        return request.user.is_superuser

# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register TenderTracker model
@admin.register(TenderTracker)
class TenderTrackerAdmin(admin.ModelAdmin):
    list_display = ('year', 'last_sequence')
    search_fields = ('year',)
    list_filter = ('year',)
    ordering = ('-year',)
    fieldsets = (
        ('Year Information', {
            'fields': ('year',)
        }),
        ('Sequence Details', {
            'fields': ('last_sequence',)
        }),
    )

# Register Department model
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'get_tenders_count')
    list_display_links = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)
    
    def get_tenders_count(self, obj):
        return obj.tender_set.count()
    get_tenders_count.short_description = 'Tenders'

# Register Tender model
@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ('tender_number', 'get_full_name', 'department', 'category', 'status', 
                   'contract_amount_display', 'invitation_date', 'created_at', 'get_days_since_creation')
    list_filter = ('status', 'category', 'department', 'currency', 
                  ('created_at', admin.DateFieldListFilter),
                  ('invitation_date', admin.DateFieldListFilter))
    search_fields = ('tender_number', 'description', 'user__profile__full_name', 
                    'department__name', 'vendor_name', 'po_number', 'sra_number')
    readonly_fields = ('tender_number', 'user', 'created_at', 'get_days_since_creation')
    list_per_page = 20
    date_hierarchy = 'created_at'
    save_on_top = True
    show_full_result_count = True
    
    def get_days_since_creation(self, obj):
        from django.utils import timezone
        from django.utils.timesince import timesince
        return timesince(obj.created_at)
    get_days_since_creation.short_description = 'Age'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tender_number', 'description', 'department', 'category', 'status')
        }),
        ('Dates', {
            'fields': ('invitation_date', 'closing_date', 'evaluation_date', 'contract_date',
                      'po_date', 'sra_date', 'payment_memo_date')
        }),
        ('Financial Details', {
            'fields': ('currency', 'contract_amount', 'payment_amount', 'vendor_name')
        }),
        ('Reference Numbers', {
            'fields': ('po_number', 'sra_number', 'file_name', 'file_number',
                      'requests_aggregated')
        }),
        ('System Information', {
            'fields': ('user', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_full_name(self, obj):
        return obj.get_officer_name()
    get_full_name.short_description = "Officer"
    
    def contract_amount_display(self, obj):
        if obj.contract_amount:
            return f"{obj.currency} {obj.contract_amount:,.2f}"
        return "-"
    contract_amount_display.short_description = "Contract Amount"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user__profile', 'department')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)

# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'get_tenders_count')
    list_display_links = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)
    
    def get_tenders_count(self, obj):
        return Tender.objects.filter(category=obj.name).count()
    get_tenders_count.short_description = 'Tenders'

# Register UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'created_at', 'get_tenders_count')
    list_display_links = ('full_name', 'user')
    search_fields = ('full_name', 'user__username', 'user__email')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def get_tenders_count(self, obj):
        return obj.user.tender_set.count()
    get_tenders_count.short_description = 'Tenders'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

# Register BreakfastItem model
@admin.register(BreakfastItem)
class BreakfastItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_display', 'available', 'get_orders_count', 'created_at')
    list_display_links = ('name',)
    list_filter = ('available', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('available',)
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }
    
    fieldsets = (
        ('Item Information', {
            'fields': ('name', 'description', 'price', 'available')
        }),
        ('Image', {
            'fields': ('image',),
            'description': 'Upload an image (JPG, PNG or WebP, max 5MB)'
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at',)
    
    def price_display(self, obj):
        return f"GHS {obj.price:,.2f}"
    price_display.short_description = 'Price'
    
    def get_orders_count(self, obj):
        return obj.orderitem_set.count()
    get_orders_count.short_description = 'Orders'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)
    autocomplete_fields = ('item',)

# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_full_name', 'status', 'total_amount_display', 
                   'items_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__profile__full_name', 
                    'items__name')
    readonly_fields = ('total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'total_amount')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_user_full_name(self, obj):
        return obj.user.profile.full_name
    get_user_full_name.short_description = 'Customer'
    
    def total_amount_display(self, obj):
        return f"GHS {obj.total_amount:,.2f}"
    total_amount_display.short_description = 'Total Amount'
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Items'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user__profile').prefetch_related('items')

# Register OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'item', 'quantity', 'price_display', 'subtotal_display')
    search_fields = ('order__id', 'item__name')
    list_filter = ('order__status', 'item')
    readonly_fields = ('price',)
    autocomplete_fields = ('order', 'item')
    
    def order_id(self, obj):
        return f"Order #{obj.order.id}"
    
    def price_display(self, obj):
        return f"GHS {obj.price:,.2f}"
    price_display.short_description = 'Unit Price'
    
    def subtotal_display(self, obj):
        return f"GHS {(obj.price * obj.quantity):,.2f}"
    subtotal_display.short_description = 'Subtotal'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'item')

# Register Division model
@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'get_iso_numbers_count')
    list_display_links = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)
    
    def get_iso_numbers_count(self, obj):
        return obj.isonumber_set.count()
    get_iso_numbers_count.short_description = 'ISO Numbers'

# Register ISOTracker model 
@admin.register(ISOTracker)
class ISOTrackerAdmin(admin.ModelAdmin):
    list_display = ('year', 'last_sequence', 'get_iso_numbers_this_year')
    search_fields = ('year',)
    ordering = ('-year',)
    
    def get_iso_numbers_this_year(self, obj):
        return ISONumber.objects.filter(date_created__year=obj.year).count()
    get_iso_numbers_this_year.short_description = 'ISO Numbers Generated'

# Register ISONumber model
@admin.register(ISONumber)
class ISONumberAdmin(admin.ModelAdmin):
    list_display = ('iso_number', 'get_officer_name', 'division', 'department', 
                   'letter_type', 'date_created')
    search_fields = ('iso_number', 'officer__username', 'officer__profile__full_name',
                    'division__name', 'department__name')
    list_filter = ('letter_type', 'date_created', 'division', 'department')
    readonly_fields = ('iso_number', 'officer', 'date_created')
    
    fieldsets = (
        ('ISO Information', {
            'fields': ('iso_number', 'letter_type')
        }),
        ('Organization', {
            'fields': ('division', 'department')
        }),
        ('System Information', {
            'fields': ('officer', 'date_created'),
            'classes': ('collapse',)
        })
    )
    
    def get_officer_name(self, obj):
        return obj.officer.profile.full_name
    get_officer_name.short_description = 'Officer'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'officer__profile', 'division', 'department'
        )

# Register TenderItem model
@admin.register(TenderItem)
class TenderItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'tender', 'quantity', 'unit_of_measure', 'chemical_grade')
    search_fields = ('item_name', 'description', 'chemical_formula', 'chemical_grade')
    list_filter = ('chemical_grade', 'physical_form')
    fieldsets = (
        (None, {
            'fields': ('tender', 'item_name', 'description', 'quantity', 'unit_of_measure')
        }),
        ('Chemical Properties', {
            'fields': ('chemical_grade', 'molar_mass', 'chemical_formula', 'density', 
                      'vapor_density', 'assay_percentage', 'physical_form', 'package_size',
                      'appearance', 'impurities', 'specifications')
        }),
        ('Manufacturer Information', {
            'fields': ('brand', 'manufacturer')
        }),
    )

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'active_agreements_count', 'total_bids')
    list_filter = ('created_at',)
    search_fields = ('name', 'contact_person', 'email')
    actions = ['export_vendor_data']
    
    def export_vendor_data(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=vendors-{datetime.now().strftime("%Y-%m-%d")}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        
        return response
    export_vendor_data.short_description = "Export Selected Vendors to CSV"
    
    def active_agreements_count(self, obj):
        # Use direct foreign key filter instead of accessing a non-existent attribute
        return FrameworkAgreement.objects.filter(vendor=obj, status='active').count()
    active_agreements_count.short_description = 'Active Agreements'

    def total_bids(self, obj):
        return obj.vendorbid_set.count()
    total_bids.short_description = 'Total Bids'

@admin.register(VendorBid)
class VendorBidAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'tender_item', 'unit_price', 'total_price', 'total_score', 'is_winner')
    list_filter = ('is_winner', 'created_at')
    search_fields = ('vendor__name', 'tender_item__item_name')
    date_hierarchy = 'created_at'
    actions = ['mark_as_winning_bid']

    def mark_as_winning_bid(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one bid to mark as winner")
            return
        
        bid = queryset.first()
        VendorBid.objects.filter(tender_item=bid.tender_item).update(is_winner=False)
        bid.is_winner = True
        bid.save()
    mark_as_winning_bid.short_description = "Mark as winning bid"

@admin.register(FrameworkAgreement)
class FrameworkAgreementAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'agreement_number', 'start_date', 'end_date', 'status', 'days_until_expiry')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('vendor__name', 'agreement_number', 'terms_conditions')
    readonly_fields = ('days_until_expiry',)
    actions = ['extend_agreement']

    def days_until_expiry(self, obj):
        if obj.end_date:
            today = datetime.now().date()
            days = (obj.end_date - today).days
            if days < 0:
                return format_html('<span style="color: red;">Expired</span>')
            elif days < 30:
                return format_html('<span style="color: orange;">{} days</span>', days)
            return f'{days} days'
        return '-'
    days_until_expiry.short_description = 'Days Until Expiry'

    def extend_agreement(self, request, queryset):
        for agreement in queryset:
            if agreement.end_date:
                agreement.end_date = agreement.end_date + timedelta(days=365)
                agreement.save()
    extend_agreement.short_description = "Extend agreements by 1 year"

class ChemicalSpecificationInline(admin.TabularInline):
    model = ChemicalSpecification
    extra = 1

@admin.register(Chemical)
class ChemicalAdmin(admin.ModelAdmin):
    list_display = ('chemical_name', 'lot_number', 'formula', 'grade', 'package_size', 'quantity')
    list_filter = ('grade', 'tender_item__tender')
    search_fields = ('chemical_name', 'lot_number', 'formula')
    inlines = [ChemicalSpecificationInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('chemical_name', 'lot_number', 'formula')
        }),
        ('Specifications', {
            'fields': ('grade', 'package_size', 'quantity')
        }),
        ('Relationships', {
            'fields': ('tender_item',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ChemicalSpecification)
class ChemicalSpecificationAdmin(admin.ModelAdmin):
    list_display = ('chemical', 'spec_type', 'value', 'unit')
    list_filter = ('spec_type', 'chemical__grade')
    search_fields = ('chemical__chemical_name', 'value')
