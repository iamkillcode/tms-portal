from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),  # Default Django admin
    path('', include('tender_app.urls')),  # Frontend URLs
    path('todo/', include('todo_app.urls')),  # ToDo system URLs
    path('audit-trail/', include('audit_trail.urls')),  # Audit Trail URLs
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

