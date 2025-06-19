from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

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
