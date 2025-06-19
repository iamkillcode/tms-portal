"""
Generic view utilities for the tender application.
"""

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q


def generic_list_view(request, model_class, template_name, context_name, 
                      search_fields=None, order_by='-created_at', paginate_by=10):
    """
    Generic view to list objects of any model with search and pagination.
    
    Parameters:
    - request: The HTTP request
    - model_class: The model class to list objects for
    - template_name: The template to render
    - context_name: The name to use for the objects list in the template context
    - search_fields: List of fields to search against
    - order_by: Field to order results by
    - paginate_by: Number of items per page
    """
    objects = model_class.objects.all()
    
    # Apply search if provided
    search_query = request.GET.get('search', '')
    if search_query and search_fields:
        query = Q()
        for field in search_fields:
            query |= Q(**{f"{field}__icontains": search_query})
        objects = objects.filter(query)
    
    # Apply ordering
    objects = objects.order_by(order_by)
    
    # Pagination
    paginator = Paginator(objects, paginate_by)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    
    context = {
        context_name: page_obj,
        'search_query': search_query,
        f'total_{context_name}': objects.count(),
    }
    
    return render(request, template_name, context)
