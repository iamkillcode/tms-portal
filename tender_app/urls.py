from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # views from app


urlpatterns = [
    path("tender-generator/", views.tender_generator_view, name="tender_generator"),
    path(
        "iso-number-generator/",
        views.generate_iso_number,  # Changed from iso_number_generator_view
        name="iso_number_generator",
    ),
    path("iso-number-list/", views.iso_number_list_view, name="iso_number_list"),
    path(
        "tender-number-list/", views.tender_number_list_view, name="tender_number_list"
    ),
    path("register/", views.register_view, name="register"),
    path("home/", views.home_view, name="home"),
    path("login/", views.custom_login_view, name="login"),  # Use custom login view
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "create-iso-detail/", views.create_iso_detail, name="create_iso_detail"
    ),  # New URL pattern
    path(
        "tender/update/<int:pk>/",
        views.TenderUpdateView.as_view(),
        name="tender_update",
    ),
    path("", views.redirect_to_home, name="redirect_to_home"),  # Redirect root URL
]
