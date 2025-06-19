"""
Task management views for the tender application.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone

from ..models import Task, TaskCategory, TaskComment
from ..forms import TaskForm, TaskCategoryForm, TaskCommentForm
from .tender_views import has_user_role


@login_required
@user_passes_test(has_user_role)
def task_list(request):
    """View to list all tasks for the current user."""
    tasks = Task.objects.filter(user=request.user)
    categories = TaskCategory.objects.filter(user=request.user)
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    # Filter by priority if provided
    priority_filter = request.GET.get('priority')
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
        
    context = {
        'tasks': tasks,
        'categories': categories,
        'task_form': TaskForm(initial={'user': request.user}),
        'task_status_choices': Task.STATUS_CHOICES,
        'task_priority_choices': Task.PRIORITY_CHOICES
    }
    return render(request, 'tender_app/task_list.html', context)


@login_required
@user_passes_test(has_user_role)
def task_detail(request, pk):
    """View details of a specific task."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    comments = task.comments.all()
    
    if request.method == 'POST':
        comment_form = TaskCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        comment_form = TaskCommentForm()
    
    context = {
        'task': task,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'tender_app/task_detail.html', context)


@login_required
@user_passes_test(has_user_role)
def task_create(request):
    """Create a new task."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(initial={
            'tender': request.GET.get('tender'),
            'vendor': request.GET.get('vendor')
        })
    
    return render(request, 'tender_app/task_form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
@user_passes_test(has_user_role)
def task_update(request, pk):
    """Update an existing task."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tender_app/task_form.html', {
        'form': form,
        'task': task,
        'action': 'Update'
    })


@login_required
@user_passes_test(has_user_role)
def task_delete(request, pk):
    """Delete a task."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    
    return render(request, 'tender_app/task_confirm_delete.html', {'task': task})


@login_required
@user_passes_test(has_user_role)
def task_status_update(request, pk):
    """Update the status of a task via AJAX."""
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        status = request.POST.get('status')
        
        if status in dict(Task.STATUS_CHOICES).keys():
            task.status = status
            task.save()
            return JsonResponse({'success': True, 'status': task.get_status_display()})
    
    return JsonResponse({'success': False}, status=400)


@login_required
@user_passes_test(has_user_role)
def task_category_create(request):
    """Create a new task category."""
    if request.method == 'POST':
        form = TaskCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('task_list')
    else:
        form = TaskCategoryForm()
    
    return render(request, 'tender_app/task_category_form.html', {'form': form})


@login_required
@user_passes_test(has_user_role)
def task_dashboard(request):
    """View for the task dashboard with task statistics."""
    # Get tasks counts by status
    pending_count = Task.objects.filter(user=request.user, status='pending').count()
    in_progress_count = Task.objects.filter(user=request.user, status='in_progress').count()
    completed_count = Task.objects.filter(user=request.user, status='completed').count()
    
    # Get tasks due soon (within 3 days)
    today = datetime.now(timezone.utc)
    due_soon = Task.objects.filter(
        user=request.user,
        due_date__gte=today,
        due_date__lte=today + timedelta(days=3),
        status__in=['pending', 'in_progress']
    )
    
    # Get overdue tasks
    overdue = Task.objects.filter(
        user=request.user,
        due_date__lt=today,
        status__in=['pending', 'in_progress']
    )
    
    context = {
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'due_soon': due_soon,
        'overdue': overdue,
    }
    
    return render(request, 'tender_app/task_dashboard.html', context)
