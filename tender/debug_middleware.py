"""
Debug middleware to help troubleshoot HTMX requests.
"""
import json
import logging

logger = logging.getLogger('django.request')

class HtmxDebugMiddleware:
    """
    Middleware to log HTMX request and response information for debugging purposes.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process the request
        is_htmx = request.headers.get('HX-Request') == 'true'
        if is_htmx:
            logger.debug(f"HTMX Request: {request.method} {request.path}")
            logger.debug(f"HTMX Headers: {dict((k, v) for k, v in request.headers.items() if k.startswith('Hx-'))}")
            
            # Log request body for POST requests
            if request.method == 'POST':
                try:
                    body = request.POST.dict()
                    logger.debug(f"HTMX Request Body: {json.dumps(body)}")
                except:
                    logger.debug("Could not parse HTMX request body")
        
        # Get the response
        response = self.get_response(request)
        
        # Process the response for HTMX requests
        if is_htmx:
            htmx_headers = {}
            for header_name, value in response.items():
                if header_name.lower().startswith('hx-'):
                    htmx_headers[header_name] = value
            
            if htmx_headers:
                logger.debug(f"HTMX Response Headers: {htmx_headers}")
            
            # Log response status
            logger.debug(f"HTMX Response Status: {response.status_code}")
        
        return response
