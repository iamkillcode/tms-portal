"""
Framework agreement-related views for the tender application.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import logging

from ..models import FrameworkAgreement, Tender, Vendor
from ..forms import FrameworkAgreementForm
from .tender_views import has_user_role

# Set up logger
logger = logging.getLogger(__name__)


@login_required
@user_passes_test(has_user_role)
def all_framework_agreements_view(request):
    """View to list all framework agreements across all tenders."""
    from datetime import datetime, timedelta
    
    # Get filter parameters first
    today = datetime.now().date()
    soon = today + timedelta(days=30)
    
    # Make efficient DB queries
    agreements = FrameworkAgreement.objects.all().select_related('vendor', 'tender')
    expired = agreements.filter(end_date__lt=today)
    expiring_soon = agreements.filter(end_date__gte=today, end_date__lte=soon)
    active_agreements = agreements.filter(end_date__gt=soon)
    
    grouped_agreements = {
        'all': agreements,
        'active': active_agreements,
        'expiring_soon': expiring_soon,
        'expired': expired,
    }
    
    tenders = Tender.objects.all()
    
    if request.method == 'POST':
        form = FrameworkAgreementForm(request.POST)
        if form.is_valid():
            agreement = form.save(commit=False)
            tender_id = request.POST.get('tender')
            if tender_id and tender_id.strip():
                try:
                    tender = get_object_or_404(Tender, id=tender_id)
                    agreement.tender = tender
                    agreement.save()
                    messages.success(request, 'Framework Agreement created successfully!')
                    return redirect('all-framework-agreements')
                except Tender.DoesNotExist:
                    messages.error(request, 'Tender not found.')
                except IntegrityError:
                    messages.error(request, 'Database integrity error. This agreement may already exist.')
                except ValidationError as e:
                    messages.error(request, f'Validation error: {str(e)}')
                except Exception as e:
                    messages.error(request, f'Unexpected error: {str(e)}')
                    # Log the unexpected exception
                    logger.error(f"Unexpected error creating agreement: {str(e)}")
            else:
                messages.error(request, 'Please select a tender')
    else:
        form = FrameworkAgreementForm()
    
    return render(request, 'all_framework_agreements.html', {
        'agreements': grouped_agreements,
        'tenders': tenders,
        'form': form,
    })


@login_required
@user_passes_test(has_user_role)
def framework_agreements_view(request, tender_id):
    """View to manage framework agreements for a specific tender."""
    tender = get_object_or_404(Tender, id=tender_id)
    agreements = tender.framework_agreements.all().select_related('vendor')
    
    # Get winning vendors from tender items
    winning_vendors = Vendor.objects.all()
    
    if request.method == 'POST':
        form = FrameworkAgreementForm(request.POST)
        if form.is_valid():
            agreement = form.save(commit=False)
            agreement.tender = tender
            agreement.save()
            messages.success(request, 'Framework Agreement created successfully!')
            return redirect('framework-agreements', tender_id=tender_id)
    else:
        form = FrameworkAgreementForm()
    
    return render(request, 'framework_agreements.html', {
        'tender': tender,
        'agreements': agreements,
        'winning_vendors': winning_vendors,
        'form': form
    })


@login_required
@user_passes_test(has_user_role)
def edit_framework_agreement_view(request, tender_id, agreement_id):
    """View to edit a framework agreement."""
    tender = get_object_or_404(Tender, id=tender_id)
    agreement = get_object_or_404(FrameworkAgreement, id=agreement_id, tender=tender)
    
    if request.method == 'POST':
        form = FrameworkAgreementForm(request.POST, instance=agreement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Framework Agreement updated successfully!')
    
    return redirect('framework-agreements', tender_id=tender_id)
