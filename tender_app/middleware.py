from typing import Any, Callable
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from .models import UserProfile, SystemActivityLog
import threading
from django.utils.deprecation import MiddlewareMixin

_local = threading.local()


def get_current_request() -> HttpRequest:
    """Get the current request from thread local storage."""
    return getattr(_local, "request", None)


def get_client_ip(request: HttpRequest) -> str:
    """
    Get the client's IP address from the request.
    Handles cases where the request is behind a proxy.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


class UserActivityMiddleware:
    """
    Middleware to track user activity and store request information.
    Also updates the user's last login IP.
    """

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Store request in thread local
        _local.request = request

        # Get client IP
        client_ip = get_client_ip(request)

        # Update user's last login IP if authenticated
        if request.user.is_authenticated:
            UserProfile.objects.filter(user=request.user).update(
                last_login_ip=client_ip
            )

        response = self.get_response(request)

        # Clean up thread local
        if hasattr(_local, "request"):
            del _local.request

        return response

    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable,
        view_args: tuple[Any, ...],
        view_kwargs: dict[str, Any],
    ) -> None:
        """
        Process view is called just before Django calls the view.
        We can use this to log additional information about the view being accessed.
        """
        # Add view name to request for logging purposes
        if hasattr(view_func, "__name__"):
            request.view_name = view_func.__name__

        # Add any other view-specific processing here
        return None


class ActivityLogMiddleware(MiddlewareMixin):
    """Middleware to log user activities."""

    def process_request(self, request):
        """Process the request and log user activity."""
        if request.user.is_authenticated:
            # Skip logging for static files and admin media
            if not any(
                path in request.path
                for path in ["/static/", "/media/", "/admin/jsi18n/"]
            ):
                SystemActivityLog.objects.create(
                    user=request.user,
                    action="view",
                    target_model=request.path.strip("/").split("/")[0] or "home",
                    description=f"Viewed {request.path}",
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get("HTTP_USER_AGENT", ""),
                )

    def get_client_ip(self, request):
        """Get the client's IP address from the request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
