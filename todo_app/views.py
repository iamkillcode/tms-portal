from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator

from .models import ToDoList, ToDoItem, ToDoComment, ToDoAttachment, ToDoTag, ToDoItemTag
from .forms import ToDoListForm, ToDoItemForm, ToDoCommentForm, ToDoAttachmentForm, ToDoTagForm

import json
import csv
from datetime import datetime, timedelta


@login_required
def todo_dashboard(request):
    """Main dashboard view for todo items"""
    # Get all lists for the user
    todo_lists = ToDoList.objects.filter(user=request.user)
    
    # If user has no lists, create a default one
    if not todo_lists.exists():
        default_list = ToDoList.objects.create(
            name="My Tasks",
            description="Default task list",
            user=request.user,
            is_default=True
        )
        todo_lists = [default_list]
    
    # Get active lists with their corresponding items
    lists_with_items = []
    for todo_list in todo_lists:
        items = ToDoItem.objects.filter(todo_list=todo_list).order_by('-is_pinned', 'status', '-priority', 'due_date')
        lists_with_items.append({
            'list': todo_list,
            'items': items
        })
    
    # Stats for dashboard summary
    today = timezone.now().date()
    upcoming_due = ToDoItem.objects.filter(
        user=request.user, 
        due_date__date__gt=today,
        due_date__date__lte=today + timedelta(days=7),
        status__in=['not_started', 'in_progress']
    ).count()
    
    overdue = ToDoItem.objects.filter(
        user=request.user,
        due_date__date__lt=today,
        status__in=['not_started', 'in_progress']
    ).count()
    
    completed_today = ToDoItem.objects.filter(
        user=request.user,
        completed_at__date=today
    ).count()
    
    # Recent activities
    recent_items = ToDoItem.objects.filter(
        user=request.user
    ).order_by('-updated_at')[:5]
    
    # Categories with item counts
    from django.db.models import Count
    from tender_app.models import TaskCategory
    categories = TaskCategory.objects.filter(
        todo_items__user=request.user
    ).annotate(
        item_count=Count('todo_items')
    ).order_by('-item_count')[:5]
    
    context = {
        'lists_with_items': lists_with_items,
        'stats': {
            'upcoming_due': upcoming_due,
            'overdue': overdue,
            'completed_today': completed_today,
        },
        'recent_items': recent_items,
        'categories': categories,
    }
    
    return render(request, 'todo_app/dashboard.html', context)


@login_required
def todo_list_view(request):
    """View all todo lists"""
    todo_lists = ToDoList.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = ToDoListForm(request.POST)
        if form.is_valid():
            todo_list = form.save(commit=False)
            todo_list.user = request.user
            todo_list.save()
            messages.success(request, f'List "{todo_list.name}" created successfully!')
            return redirect('todo_list_detail', list_id=todo_list.id)
    else:
        form = ToDoListForm()
    
    context = {
        'todo_lists': todo_lists,
        'form': form,
    }
    
    return render(request, 'todo_app/list.html', context)


@login_required
def todo_list_detail(request, list_id):
    """View details of a specific todo list with its items"""
    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    
    # Filter and sort items
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    sort_by = request.GET.get('sort', '-priority')
    
    items = ToDoItem.objects.filter(todo_list=todo_list)
    
    if status_filter:
        items = items.filter(status=status_filter)
    
    if priority_filter:
        items = items.filter(priority=priority_filter)
    
    if sort_by == 'due_date':
        items = items.order_by('due_date', '-priority')
    elif sort_by == '-due_date':
        items = items.order_by('-due_date', '-priority')
    elif sort_by == 'title':
        items = items.order_by('title')
    elif sort_by == '-title':
        items = items.order_by('-title')
    elif sort_by == 'created_at':
        items = items.order_by('created_at')
    elif sort_by == '-created_at':
        items = items.order_by('-created_at')
    else:  # Default to priority
        items = items.order_by('-is_pinned', '-priority', 'due_date')
    
    # Create form for new item
    if request.method == 'POST':
        form = ToDoItemForm(request.user, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.todo_list = todo_list
            item.save()
            messages.success(request, f'Task "{item.title}" created successfully!')
            return redirect('todo_list_detail', list_id=list_id)
    else:
        form = ToDoItemForm(request.user, initial={'todo_list': todo_list})
    
    context = {
        'todo_list': todo_list,
        'items': items,
        'form': form,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'sort_by': sort_by,
    }
    
    return render(request, 'todo_app/list_detail.html', context)


@login_required
def todo_item_detail(request, item_id):
    """View details of a specific todo item"""
    item = get_object_or_404(ToDoItem, id=item_id, user=request.user)
    
    # Comments
    comments = ToDoComment.objects.filter(todo_item=item).order_by('created_at')
    
    # Attachments
    attachments = ToDoAttachment.objects.filter(todo_item=item)
    
    # Comment form
    if request.method == 'POST' and 'comment_submit' in request.POST:
        comment_form = ToDoCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.todo_item = item
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('todo_item_detail', item_id=item_id)
    else:
        comment_form = ToDoCommentForm()
    
    # Attachment form
    if request.method == 'POST' and 'attachment_submit' in request.POST:
        attachment_form = ToDoAttachmentForm(request.POST, request.FILES)
        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.uploaded_by = request.user
            attachment.todo_item = item
            attachment.save()
            messages.success(request, 'Attachment uploaded!')
            return redirect('todo_item_detail', item_id=item_id)
    else:
        attachment_form = ToDoAttachmentForm()
    
    context = {
        'item': item,
        'comments': comments,
        'attachments': attachments,
        'comment_form': comment_form,
        'attachment_form': attachment_form,
    }
    
    return render(request, 'todo_app/item_detail.html', context)


@login_required
def todo_item_create(request):
    """Create a new todo item"""
    if request.method == 'POST':
        form = ToDoItemForm(request.user, request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            
            # Check if we need to add tags
            tags = request.POST.get('tags', '').split(',')
            for tag_name in tags:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = ToDoTag.objects.get_or_create(name=tag_name)
                    ToDoItemTag.objects.create(todo_item=item, tag=tag)
            
            messages.success(request, f'Task "{item.title}" created successfully!')
            
            # Redirect to the referrer if available, otherwise to the dashboard
            next_url = request.POST.get('next', 'todo_dashboard')
            return redirect(next_url)
    else:
        # Pre-select list if provided in query param
        list_id = request.GET.get('list', None)
        initial_data = {}
        if list_id:
            try:
                todo_list = ToDoList.objects.get(id=list_id, user=request.user)
                initial_data = {'todo_list': todo_list}
            except ToDoList.DoesNotExist:
                pass
        
        form = ToDoItemForm(request.user, initial=initial_data)
    
    context = {
        'form': form,
        'next': request.GET.get('next', 'todo_dashboard'),
    }
    
    return render(request, 'todo_app/item_create.html', context)


@login_required
def todo_item_update(request, item_id):
    """Update an existing todo item"""
    item = get_object_or_404(ToDoItem, id=item_id, user=request.user)
    
    if request.method == 'POST':
        form = ToDoItemForm(request.user, request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{item.title}" updated successfully!')
            
            # Redirect to the referrer if available, otherwise to the item detail
            next_url = request.POST.get('next', 'todo_item_detail')
            if next_url == 'todo_item_detail':
                return redirect('todo_item_detail', item_id=item_id)
            else:
                return redirect(next_url)
    else:
        form = ToDoItemForm(request.user, instance=item)
    
    context = {
        'form': form,
        'item': item,
        'next': request.GET.get('next', 'todo_item_detail'),
    }
    
    return render(request, 'todo_app/item_update.html', context)


@login_required
def todo_item_delete(request, item_id):
    """Delete a todo item"""
    item = get_object_or_404(ToDoItem, id=item_id, user=request.user)
    
    if request.method == 'POST':
        list_id = item.todo_list.id
        item.delete()
        messages.success(request, f'Task "{item.title}" deleted successfully!')
        
        # Redirect to the referrer if available, otherwise to the list detail
        next_url = request.POST.get('next', 'todo_list_detail')
        if next_url == 'todo_list_detail':
            return redirect('todo_list_detail', list_id=list_id)
        else:
            return redirect(next_url)
    
    context = {
        'item': item,
        'next': request.GET.get('next', 'todo_list_detail'),
    }
    
    return render(request, 'todo_app/item_delete.html', context)


@login_required
@require_POST
def todo_item_status_update(request, item_id):
    """AJAX endpoint to update a todo item's status"""
    item = get_object_or_404(ToDoItem, id=item_id, user=request.user)
    
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status in [status[0] for status in ToDoItem.STATUS_CHOICES]:
            item.status = new_status
            
            # Update completed_at if needed
            if new_status == 'completed' and not item.completed_at:
                item.completed_at = timezone.now()
            elif new_status != 'completed':
                item.completed_at = None
                
            # Update progress if needed
            if new_status == 'completed':
                item.progress = 100
            elif new_status == 'not_started':
                item.progress = 0
                
            item.save()
            
            return JsonResponse({
                'success': True, 
                'status': item.status,
                'progress': item.progress,
                'completed_at': item.completed_at.isoformat() if item.completed_at else None
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def todo_list_create(request):
    """Create a new todo list"""
    if request.method == 'POST':
        form = ToDoListForm(request.POST)
        if form.is_valid():
            todo_list = form.save(commit=False)
            todo_list.user = request.user
            todo_list.save()
            messages.success(request, f'List "{todo_list.name}" created successfully!')
            return redirect('todo_list_detail', list_id=todo_list.id)
    else:
        form = ToDoListForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'todo_app/list_create.html', context)


@login_required
def todo_list_update(request, list_id):
    """Update an existing todo list"""
    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    
    if request.method == 'POST':
        form = ToDoListForm(request.POST, instance=todo_list)
        if form.is_valid():
            form.save()
            messages.success(request, f'List "{todo_list.name}" updated successfully!')
            return redirect('todo_list_detail', list_id=list_id)
    else:
        form = ToDoListForm(instance=todo_list)
    
    context = {
        'form': form,
        'todo_list': todo_list,
    }
    
    return render(request, 'todo_app/list_update.html', context)


@login_required
def todo_list_delete(request, list_id):
    """Delete a todo list"""
    todo_list = get_object_or_404(ToDoList, id=list_id, user=request.user)
    
    # Don't allow deleting the default list
    if todo_list.is_default:
        messages.error(request, "Cannot delete the default list.")
        return redirect('todo_list_view')
    
    if request.method == 'POST':
        todo_list.delete()
        messages.success(request, f'List "{todo_list.name}" deleted successfully!')
        return redirect('todo_list_view')
    
    context = {
        'todo_list': todo_list,
    }
    
    return render(request, 'todo_app/list_delete.html', context)


@login_required
def todo_calendar(request):
    """Calendar view for todo items"""
    # Get all items with due dates for the user
    items = ToDoItem.objects.filter(
        user=request.user,
        due_date__isnull=False
    ).order_by('due_date')
    
    context = {
        'items': items,
    }
    
    return render(request, 'todo_app/calendar.html', context)


@login_required
def todo_export(request):
    """Export todo items as CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="todo-items-{timezone.now().strftime("%Y-%m-%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Title', 'Description', 'List', 'Category', 'Status', 'Priority',
        'Progress', 'Due Date', 'Completed At', 'Created At'
    ])
    
    # Get filtered items if any filters are applied
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    list_filter = request.GET.get('list', '')
    
    items = ToDoItem.objects.filter(user=request.user)
    
    if status_filter:
        items = items.filter(status=status_filter)
    
    if priority_filter:
        items = items.filter(priority=priority_filter)
    
    if list_filter:
        items = items.filter(todo_list_id=list_filter)
    
    for item in items:
        writer.writerow([
            item.title,
            item.description,
            item.todo_list.name,
            item.category.name if item.category else '',
            dict(ToDoItem.STATUS_CHOICES).get(item.status, ''),
            dict(ToDoItem.PRIORITY_CHOICES).get(item.priority, ''),
            f"{item.progress}%",
            item.due_date.strftime('%Y-%m-%d %H:%M') if item.due_date else '',
            item.completed_at.strftime('%Y-%m-%d %H:%M') if item.completed_at else '',
            item.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response
