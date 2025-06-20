"""
Middleware to handle PUT requests properly in Django.
"""

class HttpMethodOverrideMiddleware:
    """
    Middleware to handle PUT, DELETE and other non-POST requests.
    
    Django doesn't natively parse the request body for PUT, DELETE, etc.,
    like it does for POST. This middleware allows us to process PUT requests
    like POST requests.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if request.method == 'PUT':
            # Process PUT request body like POST
            if hasattr(request, '_post'):
                del request._post
                del request._files
            
            # Copy content type and content params from original request
            request.method = 'POST'
            request._load_post_and_files()
            request.method = 'PUT'
            
            # Save the processed data as request.PUT
            request.PUT = request.POST
            
        return self.get_response(request)
