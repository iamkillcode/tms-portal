from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Custom logout view to ensure proper logout handling"""
    # Log is handled by middleware
    logout(request)
    # Redirect to login page
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),  # Default Django admin
    path('', include('tender_app.urls')),  # Frontend URLs
    path('todo/', include('todo_app.urls')),  # ToDo system URLs
    path('audit-trail/', include('audit_trail.urls')),  # Audit Trail URLs
    path('logout/', logout_view, name='logout'),  # Custom logout view
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

