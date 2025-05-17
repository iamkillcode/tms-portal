from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # Grappelli URLS - must be before admin
    path('admin/', admin.site.urls),  # Default Django admin
    path('', include('tender_app.urls')),  # Frontend URLs
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

