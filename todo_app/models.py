from django.db import models
from django.contrib.auth.models import User
from tender_app.models import TaskCategory
from django.utils import timezone

class ToDoList(models.Model):
    """A list/collection of todo items"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_lists')
    created_at = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)
    color = models.CharField(max_length=7, default="#3498db", help_text="Hex color code")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "To-Do List"
        verbose_name_plural = "To-Do Lists"
        ordering = ['name']


class ToDoItem(models.Model):
    """Individual todo item extending the base Task model"""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('deferred', 'Deferred'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    RECURRENCE_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_items')
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name='items')
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='todo_items')
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    progress = models.IntegerField(default=0, help_text="Progress percentage (0-100)")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Recurrence
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default='none')
    recurrence_end_date = models.DateField(null=True, blank=True)
    
    # Reminders
    reminder_date = models.DateTimeField(null=True, blank=True)
    
    # Flagging
    is_flagged = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-set completed_at when status changes to completed
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        # Clear completed_at if status is not completed
        elif self.status != 'completed':
            self.completed_at = None
        
        # Ensure progress is 100% when completed
        if self.status == 'completed':
            self.progress = 100
            
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "To-Do Item"
        verbose_name_plural = "To-Do Items"
        ordering = ['-is_pinned', '-priority', 'due_date', '-created_at']


class ToDoComment(models.Model):
    """Comments on todo items"""
    todo_item = models.ForeignKey(ToDoItem, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment on {self.todo_item.title} by {self.user.username}"
    
    class Meta:
        ordering = ['created_at']


class ToDoAttachment(models.Model):
    """Attachments for todo items"""
    todo_item = models.ForeignKey(ToDoItem, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='todo_attachments/')
    name = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class ToDoTag(models.Model):
    """Tags for categorizing todo items"""
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#6c757d", help_text="Hex color code")
    
    def __str__(self):
        return self.name


class ToDoItemTag(models.Model):
    """Many-to-many relationship between todo items and tags"""
    todo_item = models.ForeignKey(ToDoItem, on_delete=models.CASCADE)
    tag = models.ForeignKey(ToDoTag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('todo_item', 'tag')
