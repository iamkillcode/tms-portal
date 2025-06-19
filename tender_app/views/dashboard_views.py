"""
Dashboard views for the tender application.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

from ..models import Tender, ISONumber, Vendor
from .tender_views import has_user_role


@login_required
@user_passes_test(has_user_role)
def dashboard_view(request):
    """Main dashboard view for the tender application."""
    # Get counts
    total_tenders = Tender.objects.count()
    total_isos = ISONumber.objects.count()
    total_vendors = Vendor.objects.count()
    
    # Get recent items (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_tenders = Tender.objects.filter(
        created_at__gte=thirty_days_ago
    ).order_by('-created_at')[:5]
    
    recent_isos = ISONumber.objects.filter(
        date_created__gte=thirty_days_ago
    ).order_by('-date_created')[:5]
    
    # Get tender statistics by department
    department_stats = Tender.objects.values('department__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Get upcoming contract expirations
    today = timezone.now().date()
    upcoming_30_days = today + timedelta(days=30)
    expiring_contracts = Tender.objects.filter(
        contract_date__lt=upcoming_30_days,
        contract_date__gte=today
    ).order_by('contract_date')[:5]
    
    context = {
        'total_tenders': total_tenders,
        'total_isos': total_isos,
        'total_vendors': total_vendors,
        'recent_tenders': recent_tenders,
        'recent_isos': recent_isos,
        'department_stats': department_stats,
        'expiring_contracts': expiring_contracts,
    }
    
    return render(request, 'dashboard.html', context)
