from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timezone, timedelta
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db.models.functions import ExtractMonth
from django.urls import reverse
from django.utils import timezone as django_timezone
from django.views.generic import DetailView

from .models import (
    TenderTracker, Department, Category, Tender, TenderItem,
    VendorBid, FrameworkAgreement, Vendor, ISONumber, ISOTracker,
    Division, UserProfile, BreakfastItem, Order, OrderItem,
    Chemical, ChemicalSpecification, Task, TaskCategory, TaskComment
)

from .forms import (
    CustomUserCreationForm, TenderItemForm, VendorBidForm,
    FrameworkAgreementForm, ChemicalForm, ChemicalSpecificationForm,
    ChemicalImportForm, TaskForm, TaskCategoryForm, TaskCommentForm,
    UserProfileForm, VendorForm
)

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
import pandas as pd

def all_framework_agreements_view(request):
    """View to list all framework agreements across all tenders."""
    from datetime import datetime, timedelta
    
    agreements = FrameworkAgreement.objects.all().select_related('vendor', 'tender')
    tenders = Tender.objects.all()
    
    # Process agreements to find status
    active_agreements = []
    expiring_soon = []
    expired = []
    
    today = datetime.now().date()
    soon = today + timedelta(days=30)
    
    # Categorize agreements in a single pass
    for agreement in agreements:
        if agreement.end_date < today:
            expired.append(agreement)
        elif agreement.end_date <= soon:
            expiring_soon.append(agreement)
        else:
            active_agreements.append(agreement)
            
    grouped_agreements = {
        'all': agreements,
        'active': active_agreements,
        'expiring_soon': expiring_soon,
        'expired': expired,
    }
    
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
                except Exception as e:
                    messages.error(request, f'Error creating agreement: {str(e)}')
            else:
                messages.error(request, 'Please select a tender')
    else:
        form = FrameworkAgreementForm()
    
    return render(request, 'all_framework_agreements.html', {
        'agreements': grouped_agreements,
        'tenders': tenders,
        'form': form,
    })
