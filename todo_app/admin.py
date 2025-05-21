from django.contrib import admin
from .models import ToDoList, ToDoItem, ToDoComment, ToDoAttachment, ToDoTag, ToDoItemTag


class ToDoCommentInline(admin.TabularInline):
    model = ToDoComment
    extra = 0


class ToDoAttachmentInline(admin.TabularInline):
    model = ToDoAttachment
    extra = 0


@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'is_default', 'item_count')
    list_filter = ('is_default', 'user')
    search_fields = ('name', 'description', 'user__username')
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(ToDoItem)
class ToDoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'todo_list', 'status', 'priority', 'due_date', 'progress')
    list_filter = ('status', 'priority', 'is_flagged', 'is_pinned', 'todo_list', 'user')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'created_at'
    inlines = [ToDoCommentInline, ToDoAttachmentInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'user', 'todo_list', 'category')
        }),
        ('Status', {
            'fields': ('status', 'priority', 'progress')
        }),
        ('Dates', {
            'fields': ('due_date', 'completed_at')
        }),
        ('Recurrence', {
            'fields': ('recurrence', 'recurrence_end_date'),
            'classes': ('collapse',)
        }),
        ('Reminders', {
            'fields': ('reminder_date',),
            'classes': ('collapse',)
        }),
        ('Flags', {
            'fields': ('is_flagged', 'is_pinned'),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'todo_list', 'category')


@admin.register(ToDoComment)
class ToDoCommentAdmin(admin.ModelAdmin):
    list_display = ('todo_item', 'user', 'content_preview', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'user__username', 'todo_item__title')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(ToDoAttachment)
class ToDoAttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'todo_item', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'uploaded_by')
    search_fields = ('name', 'uploaded_by__username', 'todo_item__title')


@admin.register(ToDoTag)
class ToDoTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'item_count')
    search_fields = ('name',)
    
    def item_count(self, obj):
        return ToDoItemTag.objects.filter(tag=obj).count()
    item_count.short_description = 'Items'


@admin.register(ToDoItemTag)
class ToDoItemTagAdmin(admin.ModelAdmin):
    list_display = ('todo_item', 'tag')
    list_filter = ('tag',)
    search_fields = ('todo_item__title', 'tag__name')
