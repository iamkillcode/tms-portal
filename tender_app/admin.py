from django.contrib import admin
from .models import TenderTracker, Department, Tender, Category, UserProfile, BreakfastItem, Order, OrderItem, Division, ISOTracker, ISONumber

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
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

# Register Tender model
@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ('tender_number', 'get_full_name', 'description', 'department', 'created_at') #user
    search_fields = ('tender_number', 'user__username', 'description', 'department__name')
    list_filter = ('created_at', 'department')
    readonly_fields = ('tender_number', 'user', 'created_at')  # Make non-editable fields readonly

    def get_full_name(self, obj):
        return obj.user.profile.full_name  # Access the UserProfile full_name
    get_full_name.short_description = "Officer"

    def save_model(self, request, obj, form, change):
        # Automatically link the user (officer) creating the tender
        if not obj.pk:  # Only on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)

# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

# Register UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name')
    search_fields = ('user__username', 'full_name')

# Register BreakfastItem model
@admin.register(BreakfastItem)
class BreakfastItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'created_at')
    list_filter = ('available',)
    search_fields = ('name', 'description')

# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'user__email')

# Register OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'price')
    search_fields = ('order__id', 'item__name')

# Register Division model
@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)

# Register ISOTracker model 
@admin.register(ISOTracker)
class ISOTrackerAdmin(admin.ModelAdmin):
    list_display = ('year', 'last_sequence')
    search_fields = ('year',)
    ordering = ('-year',)

# Register ISONumber model
@admin.register(ISONumber)
class ISONumberAdmin(admin.ModelAdmin):
    list_display = ('iso_number', 'officer', 'division', 'department', 'letter_type', 'date_created')
    search_fields = ('iso_number', 'officer__username', 'division__name', 'department__name')
    list_filter = ('letter_type', 'date_created', 'division', 'department')
    readonly_fields = ('iso_number', 'date_created')
