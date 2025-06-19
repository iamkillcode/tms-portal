"""
Chemical-related views for the tender application.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from ..models import Chemical, ChemicalSpecification, TenderItem
from ..forms import ChemicalForm, ChemicalSpecificationForm, ChemicalImportForm
from .tender_views import has_user_role


@login_required
@user_passes_test(has_user_role)
def chemical_list(request):
    """View to list all chemicals."""
    chemicals = Chemical.objects.all().select_related('tender_item__tender')
    
    # Filter by tender item if provided
    tender_item_id = request.GET.get('tender_item')
    if tender_item_id:
        chemicals = chemicals.filter(tender_item_id=tender_item_id)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        chemicals = chemicals.filter(
            Q(chemical_name__icontains=search_query) |
            Q(lot_number__icontains=search_query) |
            Q(formula__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(chemicals, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tender_items': TenderItem.objects.all(),
        'search_query': search_query,
        'tender_item_id': tender_item_id,
    }
    return render(request, 'tender_app/chemical_list.html', context)


@login_required
@user_passes_test(has_user_role)
def chemical_create(request):
    """View to create a new chemical."""
    if request.method == 'POST':
        form = ChemicalForm(request.POST)
        if form.is_valid():
            chemical = form.save()
            messages.success(request, f'Chemical "{chemical.chemical_name}" created successfully!')
            return redirect('chemical_detail', pk=chemical.pk)
    else:
        form = ChemicalForm()
    
    return render(request, 'tender_app/chemical_form.html', {'form': form, 'title': 'Create Chemical'})


@login_required
@user_passes_test(has_user_role)
def chemical_detail(request, pk):
    """View details of a specific chemical."""
    chemical = get_object_or_404(Chemical, pk=pk)
    spec_form = ChemicalSpecificationForm()
    
    if request.method == 'POST':
        spec_form = ChemicalSpecificationForm(request.POST)
        if spec_form.is_valid():
            spec = spec_form.save(commit=False)
            spec.chemical = chemical
            spec.save()
            messages.success(request, 'Specification added successfully!')
            return redirect('chemical_detail', pk=chemical.pk)
    
    context = {
        'chemical': chemical,
        'spec_form': spec_form,
        'specifications': chemical.specifications.all(),
    }
    return render(request, 'tender_app/chemical_detail.html', context)


@login_required
@user_passes_test(has_user_role)
def chemical_update(request, pk):
    """View to update an existing chemical."""
    chemical = get_object_or_404(Chemical, pk=pk)
    if request.method == 'POST':
        form = ChemicalForm(request.POST, instance=chemical)
        if form.is_valid():
            chemical = form.save()
            messages.success(request, f'Chemical "{chemical.chemical_name}" updated successfully!')
            return redirect('chemical_detail', pk=chemical.pk)
    else:
        form = ChemicalForm(instance=chemical)
    
    return render(request, 'tender_app/chemical_form.html', {'form': form, 'title': 'Update Chemical'})


@login_required
@user_passes_test(has_user_role)
def chemical_import(request):
    """View to import chemicals from a file."""
    if request.method == 'POST':
        form = ChemicalImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            tender_item_id = form.cleaned_data['tender_item']
            
            try:
                import pandas as pd
                
                # Read file (Excel or CSV)
                if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                    df = pd.read_excel(file)
                elif file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    raise ValueError("Unsupported file format. Please use Excel or CSV.")
                
                # Get the tender item
                tender_item = TenderItem.objects.get(id=tender_item_id)
                
                # Process each row
                chemicals_created = 0
                for _, row in df.iterrows():
                    chemical = Chemical(
                        tender_item=tender_item,
                        chemical_name=row.get('chemical_name', ''),
                        cas_number=row.get('cas_number', ''),
                        formula=row.get('formula', ''),
                        purity=row.get('purity', ''),
                        lot_number=row.get('lot_number', ''),
                        manufacturer=row.get('manufacturer', ''),
                        appearance=row.get('appearance', ''),
                        notes=row.get('notes', '')
                    )
                    chemical.save()
                    chemicals_created += 1
                
                messages.success(request, f'{chemicals_created} chemicals imported successfully!')
                return redirect('chemical_list')
                
            except Exception as e:
                messages.error(request, f"Error importing chemicals: {str(e)}")
                
    else:
        form = ChemicalImportForm()
    
    return render(request, 'tender_app/chemical_import.html', {'form': form})


@login_required
@user_passes_test(has_user_role)
def chemical_spec_delete(request, pk):
    """Delete a chemical specification."""
    spec = get_object_or_404(ChemicalSpecification, pk=pk)
    chemical_pk = spec.chemical.pk
    spec.delete()
    messages.success(request, 'Specification deleted successfully.')
    return redirect('chemical_detail', pk=chemical_pk)
