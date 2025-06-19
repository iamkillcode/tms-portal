"""
Report-related views for the tender application.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.db.models.functions import ExtractMonth

from .tender_views import has_admin_role


@login_required
@user_passes_test(has_admin_role)
def reports_view(request):
    """View to display various reports and statistics."""
    from ..models import Tender, ISONumber, Department, Vendor
    from datetime import datetime, timedelta
    
    # Get date range filters
    today = datetime.now().date()
    start_date = request.GET.get('start_date', (today - timedelta(days=365)).isoformat())
    end_date = request.GET.get('end_date', today.isoformat())
    
    # Filter tenders by date range
    tenders = Tender.objects.filter(created_at__date__range=[start_date, end_date])
    
    # Generate tender statistics
    tender_count = tenders.count()
    tender_by_department = tenders.values('department__name').annotate(count=Count('id'))
    tender_by_month = tenders.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id'))
    
    # Generate contract value statistics
    total_contract_value = sum(t.contract_amount or 0 for t in tenders if t.contract_amount)
    avg_contract_value = total_contract_value / tender_count if tender_count > 0 else 0
    
    # Get top vendors
    top_vendors = Vendor.objects.annotate(
        agreement_count=Count('framework_agreements')
    ).order_by('-agreement_count')[:10]
    
    context = {
        'tender_count': tender_count,
        'tender_by_department': tender_by_department,
        'tender_by_month': tender_by_month,
        'total_contract_value': total_contract_value,
        'avg_contract_value': avg_contract_value,
        'top_vendors': top_vendors,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'tender_app/reports.html', context)
