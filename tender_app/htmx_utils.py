"""
Utility functions for HTMX integration in Django templates.
"""

from django.http import HttpResponse
from django.template.response import TemplateResponse


def is_htmx_request(request):
    """Check if the request is an HTMX request."""
    return request.headers.get('HX-Request') == 'true'


def with_htmx(view_func):
    """
    Decorator to handle both HTMX and regular requests in view functions.
    
    For HTMX requests, it renders only the partial template.
    For regular requests, it renders the full template with layout.
    
    Usage:
    @with_htmx(template='path/to/template.html', partial='path/to/partial.html')
    def my_view(request):
        # Your view logic here
        return {'context': 'data'}
    """
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        
        # If the response is already a HttpResponse, return it directly
        if isinstance(response, HttpResponse) and not isinstance(response, TemplateResponse):
            return response
        
        # Extract context or use empty dict if the response is a dict
        context = response if isinstance(response, dict) else {}
        
        if is_htmx_request(request):
            # If it's an HTMX request, set the template to the partial template
            template_name = wrapper.partial_template
            
            # Check if we're targeting a specific element
            target = request.headers.get('HX-Target')
            if target:
                context['hx_target'] = target
                
        else:
            # Regular request, use the full template
            template_name = wrapper.full_template
            
        return TemplateResponse(request, template_name, context)
    
    # This will be set by the decorator when called
    wrapper.full_template = None
    wrapper.partial_template = None
    
    return wrapper


def htmx_template(full_template, partial_template):
    """
    Decorator that specifies which template to use for full and partial rendering.
    
    Args:
        full_template: Path to the full template with layout
        partial_template: Path to the partial template for HTMX requests
    
    Usage:
    @htmx_template('path/to/full.html', 'path/to/partial.html')
    def my_view(request):
        # Your view logic here
        return {'context': 'data'}
    """
    def decorator(view_func):
        wrapped_view = with_htmx(view_func)
        wrapped_view.full_template = full_template
        wrapped_view.partial_template = partial_template
        return wrapped_view
    
    return decorator
