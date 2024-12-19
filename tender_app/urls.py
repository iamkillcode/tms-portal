from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # views from app

urlpatterns = [
    path('tender-generator/', views.tender_generator_view, name='tender_generator'),
    path('', views.register_view, name='register'),
    # path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tender-activities/', views.tender_activity_view, name='tender_activities'),

]
