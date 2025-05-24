import re
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser
from .models import AuditLog
import json

class AuditTrailMiddleware(MiddlewareMixin):
    """
    Middleware to automatically log user activity.
    """
    # Paths that should not be logged
    EXCLUDED_PATHS = [
        r'^/admin/jsi18n/',
        r'^/static/',
        r'^/media/',
        r'^/__debug__/',
        r'^/favicon\.ico$',
    ]

    # Add the async_mode attribute required in Django 5.1.4
    async_mode = 'sync'

    def __init__(self, get_response):
        self.get_response = get_response
        # Compile excluded paths regex
        self.excluded_paths_regex = [re.compile(path) for path in self.EXCLUDED_PATHS]

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_request(self, request):
        request._audit_trail_info = {
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
        request.client_ip = self.get_client_ip(request)
        return None

    def process_response(self, request, response):
        path = request.path
        for pattern in self.excluded_paths_regex:
            if pattern.match(path):
                return response

        # Special handling for logout path - log even with 405 status
        if path == '/logout/' or path.endswith('/logout/'):
            user = request.user if hasattr(request, 'user') and request.user.is_authenticated else None
            if user:
                try:
                    AuditLog.objects.create(
                        user=user,
                        action_type='LOGOUT',
                        action_detail=f"URL: {request.path}, Method: {request.method}",
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        app_name='auth',
                        model_name='user',
                        object_repr=f"User #{user.id}"
                    )
                except Exception as e:
                    # Log the error but don't break the application
                    print(f"Error logging logout: {e}")
            
            # Always return the response for logout requests
            return response

        # Skip if status code is not successful (except for the special case above)
        if response.status_code < 200 or response.status_code >= 400:
            return response

        # Only log GET, POST, PUT, DELETE methods
        if request.method not in ['GET', 'POST', 'PUT', 'DELETE']:
            return response

        # Skip logging for static files and media
        if path.startswith(('/static/', '/media/')):
            return response

        # Check if the user is authenticated
        user = request.user if request.user.is_authenticated else None
        if not user:
            # Skip logging for anonymous users except for login attempts
            if not path.startswith('/login/'):
                return response

        # Try to determine the action type based on the request
        action_type = self.determine_action_type(request)
        app_name, model_name = self.get_app_and_model_from_request(request)

        # Create the audit log (only once per request)
        try:
            if hasattr(request, '_audit_trail_info'):
                AuditLog.objects.create(
                    user=user,
                    action_type=action_type,
                    action_detail=f"URL: {request.path}, Method: {request.method}",
                    ip_address=request._audit_trail_info.get('ip_address'),
                    user_agent=request._audit_trail_info.get('user_agent'),
                    app_name=app_name,
                    model_name=model_name,
                    object_repr=self.get_object_repr(request)
                )
        except Exception:
            pass
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def determine_action_type(self, request):
        method = request.method
        path = request.path
        if path.endswith('/login/') and method == 'POST':
            return 'LOGIN'
        elif path.endswith('/logout/'):
            return 'LOGOUT'
        if method == 'GET':
            return 'VIEW'
        elif method == 'POST':
            if 'delete' in path or 'remove' in path:
                return 'DELETE'
            if any(x in path for x in ['edit', 'update']):
                return 'UPDATE'
            return 'CREATE'
        elif method == 'PUT':
            return 'UPDATE'
        elif method == 'DELETE':
            return 'DELETE'
        if 'export' in path:
            return 'EXPORT'
        if any(x in path for x in ['generate', 'create']):
            return 'GENERATE'
        return 'OTHER'

    def get_app_and_model_from_request(self, request):
        try:
            resolver_match = resolve(request.path)
            app_name = resolver_match.app_name or resolver_match.namespaces[0] if resolver_match.namespaces else ''
            view_name = resolver_match.func.__name__
            model_indicators = ['view', 'list', 'detail', 'create', 'update', 'delete']
            model_name = view_name
            for indicator in model_indicators:
                if indicator in view_name:
                    model_name = view_name.replace(f"_{indicator}", "").replace(f"{indicator}_", "")
                    break
            return app_name, model_name
        except Exception:
            return '', ''

    def get_object_repr(self, request):
        path_parts = request.path.strip('/').split('/')
        for i, part in enumerate(path_parts):
            if part.isdigit() and i > 0:
                return f"{path_parts[i-1]} #{part}"
        return ""
