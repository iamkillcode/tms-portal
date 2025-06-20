"""
Vendor-related views for the tender application.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from ..models import Vendor, FrameworkAgreement, VendorBid, ISONumber
from ..forms import VendorForm
from .tender_views import has_user_role


@login_required
@user_passes_test(has_user_role)
def vendor_list_view(request):
    """Display a list of all vendors."""
    from ..htmx_utils import htmx_template
    
    @htmx_template('vendor_list.html', 'htmx/vendor_list_rows.html')
    def _vendor_list(request):
        vendors = Vendor.objects.all().order_by('name')
        
        # Search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            vendors = vendors.filter(
                Q(name__icontains=search_query) |
                Q(contact_person__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        # Pagination
        paginator = Paginator(vendors, 10)  # Show 10 vendors per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return {
            'page_obj': page_obj,
            'search_query': search_query,
            'total_vendors': vendors.count(),
        }
    
    return _vendor_list(request)


@login_required
@user_passes_test(has_user_role)
def vendor_detail_view(request, vendor_id):
    """Display details of a specific vendor."""
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    # Get related tenders through framework agreements
    framework_agreements = vendor.framework_agreements.all().select_related('tender')
    
    # Get related tenders through winning bids
    winning_bids = VendorBid.objects.filter(vendor=vendor, is_winner=True).select_related('tender', 'tender_item').distinct()
    
    # Get associated ISO numbers through tenders
    iso_numbers = []
    for agreement in framework_agreements:
        iso_numbers.extend(list(ISONumber.objects.filter(tender=agreement.tender)))
    
    for bid in winning_bids:
        if bid.tender:
            iso_numbers.extend(list(ISONumber.objects.filter(tender=bid.tender)))
    
    # Remove duplicates
    iso_numbers = list(set(iso_numbers))
    
    return render(request, 'vendor_detail.html', {
        'vendor': vendor,
        'framework_agreements': framework_agreements,
        'winning_bids': winning_bids,
        'iso_numbers': iso_numbers,
    })


@login_required
@user_passes_test(has_user_role)
def vendor_create_view(request):
    """Create a new vendor."""
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save()
            messages.success(request, f'Vendor "{vendor.name}" created successfully!')
            return redirect('vendor-detail', vendor_id=vendor.id)
    else:
        form = VendorForm()
    
    return render(request, 'vendor_form.html', {
        'form': form,
        'title': 'Add New Vendor',
        'button_text': 'Create Vendor',
    })


@login_required
@user_passes_test(has_user_role)
def vendor_update_view(request, vendor_id):
    """Update an existing vendor."""
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            vendor = form.save()
            messages.success(request, f'Vendor "{vendor.name}" updated successfully!')
            return redirect('vendor-detail', vendor_id=vendor.id)
    else:
        form = VendorForm(instance=vendor)
    
    return render(request, 'vendor_form.html', {
        'form': form,
        'vendor': vendor,
        'title': f'Edit Vendor: {vendor.name}',
        'button_text': 'Update Vendor',
    })


@login_required
@user_passes_test(has_user_role)
def vendor_delete_view(request, vendor_id):
    """Delete an existing vendor."""
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    if request.method == 'POST':
        vendor_name = vendor.name
        vendor.delete()
        messages.success(request, f'Vendor "{vendor_name}" deleted successfully!')
        return redirect('vendor-list')
    
    return render(request, 'vendor_confirm_delete.html', {
        'vendor': vendor,
    })


@login_required
@user_passes_test(has_user_role)
def vendor_bids_view(request, tender_id, item_id):
    """View to manage bids from vendors for a specific tender item."""
    from ..models import Tender, TenderItem
    from ..forms import VendorBidForm
    
    tender = get_object_or_404(Tender, id=tender_id)
    item = get_object_or_404(TenderItem, id=item_id, tender=tender)
    bids = VendorBid.objects.filter(tender_item=item).select_related('vendor')
    vendors = Vendor.objects.all()
    
    if request.method == 'POST':
        form = VendorBidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.tender_item = item
            bid.tender = tender
            bid.save()
            messages.success(request, 'Bid added successfully!')
            return redirect('vendor-bids', tender_id=tender_id, item_id=item_id)
    else:
        form = VendorBidForm()
    
    return render(request, 'vendor_bids.html', {
        'tender': tender,
        'item': item,
        'bids': bids,
        'vendors': vendors,
        'form': form
    })


@login_required
@user_passes_test(has_user_role)
def edit_vendor_bid_view(request, tender_id, item_id, bid_id):
    """View to edit a vendor bid."""
    from ..models import Tender, TenderItem, VendorBid
    from ..forms import VendorBidForm
    
    tender = get_object_or_404(Tender, id=tender_id)
    item = get_object_or_404(TenderItem, id=item_id, tender=tender)
    bid = get_object_or_404(VendorBid, id=bid_id, tender_item=item)
    
    if request.method == 'POST':
        form = VendorBidForm(request.POST, instance=bid)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bid updated successfully!')
    
    return redirect('vendor-bids', tender_id=tender_id, item_id=item_id)
