"""
Middleware to handle HTMX-specific response requirements.
"""

from django.utils.deprecation import MiddlewareMixin


class HtmxMiddleware(MiddlewareMixin):
    """
    Middleware for handling HTMX requests and responses.
    
    This middleware adds htmx-specific attributes to the request object
    and adds appropriate headers to HTMX responses.
    """
    
    def process_request(self, request):
        # Add htmx property to requests
        request.htmx = False
        if 'HX-Request' in request.headers:
            request.htmx = True
            
        # Add additional HTMX attributes to the request
        if request.htmx:
            request.htmx_boosted = 'HX-Boosted' in request.headers
            request.htmx_target = request.headers.get('HX-Target', None)
            request.htmx_trigger = request.headers.get('HX-Trigger', None)
            request.htmx_trigger_name = request.headers.get('HX-Trigger-Name', None)
            request.htmx_current_url = request.headers.get('HX-Current-URL', None)
    
    def process_response(self, request, response):
        # Only add headers if this is an HTMX request
        if getattr(request, 'htmx', False):
            # If HX-Redirect is set, use that for redirection
            hx_redirect = getattr(response, 'HX_REDIRECT', None)
            if hx_redirect:
                response['HX-Redirect'] = hx_redirect
            
            # If HX-Refresh is set to true, trigger a full page refresh
            if getattr(response, 'HX_REFRESH', False):
                response['HX-Refresh'] = 'true'
            
            # If HX-Trigger is set, add triggers
            hx_trigger = getattr(response, 'HX_TRIGGER', None)
            if hx_trigger:
                response['HX-Trigger'] = hx_trigger
            
            # If HX-Trigger-After-Swap is set, add those triggers
            hx_trigger_after_swap = getattr(response, 'HX_TRIGGER_AFTER_SWAP', None)
            if hx_trigger_after_swap:
                response['HX-Trigger-After-Swap'] = hx_trigger_after_swap
            
        return response
