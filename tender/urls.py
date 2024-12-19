from django.contrib import admin
from django.urls import path, include 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tender_app.urls")),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('grappelli/', include('grappelli.urls')),
]

