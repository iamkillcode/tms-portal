from django.contrib import admin
from django.utils.html import format_html
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user_link', 'action_type', 'app_name', 'model_name', 'object_repr', 'ip_address')
    list_filter = ('timestamp', 'action_type', 'app_name', 'model_name', 'user')
    search_fields = ('user__username', 'action_detail', 'object_repr', 'ip_address')
    readonly_fields = ('timestamp', 'user', 'action_type', 'content_type', 'object_id', 'object_repr', 
                      'action_detail', 'ip_address', 'user_agent', 'app_name', 'model_name')
    date_hierarchy = 'timestamp'
    
    def user_link(self, obj):
        if obj.user:
            return format_html('<a href="{}">{}</a>', 
                              f'/admin/auth/user/{obj.user.id}/change/',
                              obj.user.username)
        return 'Anonymous'
    
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__username'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Only allow superusers to delete audit logs
        return request.user.is_superuser
