"""
ISO number-related views for the tender application.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

from ..models import ISONumber, Division, Department, Tender, ISOTracker
from .tender_views import has_user_role


@login_required
@user_passes_test(has_user_role)
def iso_generator_view(request, tender_id=None):
    """View to generate a new ISO number."""
    if tender_id:
        tender = get_object_or_404(Tender, id=tender_id)
    else:
        tender = None

    if request.method == "POST":
        try:
            division_code = request.POST.get("division_code")
            department_code = request.POST.get("department_code")
            letter_type = request.POST.get("letter_type")
            tender_id = request.POST.get("tender_id")

            if not all([division_code, department_code, letter_type, tender_id]):
                raise ValueError("All fields must be provided.")

            tender = get_object_or_404(Tender, id=tender_id)
            division = get_object_or_404(Division, code=division_code)
            department = get_object_or_404(Department, code=department_code)

            # Generate ISO number
            prefix = "FDA"
            year = datetime.now().year
            year_short = str(year)[-2:]
            
            # Get next sequence number
            sequence = ISOTracker.get_next_sequence(year)
            sequence_str = str(sequence).zfill(4)

            iso_number = f"{prefix}/{division.code}/{department.code}/{letter_type}/{year_short}/{sequence_str}"

            # Create ISO number record
            iso = ISONumber.objects.create(
                iso_number=iso_number,
                officer=request.user,
                tender=tender,
                division=division,
                department=department,
                letter_type=letter_type,
                description=tender.description
            )

            messages.success(request, f'ISO Number generated successfully: {iso_number}')
            return redirect('iso-detail', iso_id=iso.id)

        except Exception as e:
            messages.error(request, str(e))

    divisions = Division.objects.all()
    if not divisions.exists():
        messages.warning(request, "No divisions found. Please add divisions to the database.")
    
    context = {
        'divisions': divisions,
        'departments': Department.objects.all(),
        'tender': tender,
        'tenders': Tender.objects.all() if not tender else None
    }
    
    return render(request, 'iso_generator.html', context)


@login_required
@user_passes_test(has_user_role)
def iso_detail_view(request, iso_id):
    """View details of a specific ISO number."""
    iso = get_object_or_404(ISONumber, id=iso_id)
    return render(request, 'iso_detail.html', {'iso': iso})


@login_required
@user_passes_test(has_user_role)
def iso_list_view(request):
    """View to list all ISO numbers."""
    isos = ISONumber.objects.all().order_by('-date_created')
    search_query = request.GET.get('search', '')
    
    if search_query:
        isos = isos.filter(
            Q(iso_number__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(division__name__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )
    
    paginator = Paginator(isos, 10)
    page = request.GET.get('page')
    isos = paginator.get_page(page)
    
    return render(request, 'iso_list.html', {
        'isos': isos,
        'search_query': search_query
    })
