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
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="auth/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "create-iso-detail/", views.create_iso_detail, name="create_iso_detail"
    ),  # New URL pattern
    path(
        "tender/update/<int:pk>/",
        views.TenderUpdateView.as_view(),
        name="tender_update",
    ),
    path("", views.HomeView.as_view(), name="home"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("tenders/", views.TenderListView.as_view(), name="tender_list"),
    path("tenders/create/", views.TenderCreateView.as_view(), name="tender_create"),
    path("tenders/<int:pk>/", views.TenderDetailView.as_view(), name="tender_detail"),
    path(
        "tenders/<int:pk>/edit/", views.TenderUpdateView.as_view(), name="tender_edit"
    ),
    path(
        "tenders/<int:pk>/delete/",
        views.TenderDeleteView.as_view(),
        name="tender_delete",
    ),
    path(
        "api/departments/", views.DepartmentListView.as_view(), name="department_list"
    ),
    path("api/categories/", views.CategoryListView.as_view(), name="category_list"),
]
