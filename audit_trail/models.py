from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class AuditLog(models.Model):
    """
    Model to track user activities across the system.
    """
    ACTION_TYPES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('VIEW', 'View'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('EXPORT', 'Export'),
        ('IMPORT', 'Import'),
        ('GENERATE', 'Generate'),
        ('OTHER', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    timestamp = models.DateTimeField(default=timezone.now)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    
    # For tracking the specific object affected
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional details
    object_repr = models.CharField(max_length=255, blank=True, help_text="String representation of the affected object")
    action_detail = models.TextField(blank=True, help_text="Details about the action")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Additional metadata
    app_name = models.CharField(max_length=100, blank=True)
    model_name = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        permissions = [
            ("can_view_all_logs", "Can view all audit logs"),
            ("can_export_logs", "Can export audit logs"),
        ]

    def __str__(self):
        if self.user:
            user_repr = self.user.username
        else:
            user_repr = "Anonymous"
        
        return f"{self.get_action_type_display()} by {user_repr} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
