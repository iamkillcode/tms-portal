from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from . import views

def registration_disabled(request):
    return render(request, 'registration_disabled.html')

urlpatterns = [
    # Authentication URLs
    path('', views.dashboard_view, name='dashboard'),  # Make dashboard the root URL
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', registration_disabled, name='register'),  # Disabled registration
      # Tender URLs
    path('tender-generator/', views.tender_generator_view, name='tender-generator'),
    path('tender/create/', views.tender_generator_view, name='tender-create'),  # Alias for tender-generator
    
    # Tender Management URLs
    path('tenders/', include([
        path('list/', views.tender_list_view, name='tender-list'),
        path('activity/', views.tender_activity_view, name='tender-activity'),
        path('<int:tender_id>/update/', views.tender_update_view, name='tender-update'),
        path('export/', views.export_tenders_view, name='export-tenders'),
        # Tender Items URLs
        path('<int:tender_id>/items/', views.tender_items_view, name='tender-items'),
        path('<int:tender_id>/items/<int:item_id>/edit/', views.edit_tender_item_view, name='edit-tender-item'),
        # Vendor Bids URLs
        path('<int:tender_id>/items/<int:item_id>/bids/', views.vendor_bids_view, name='vendor-bids'),
        path('<int:tender_id>/items/<int:item_id>/bids/<int:bid_id>/edit/', 
             views.edit_vendor_bid_view, name='edit-vendor-bid'),
        # Framework Agreement URLs
        path('<int:tender_id>/agreements/', views.framework_agreements_view, name='framework-agreements'),
        path('<int:tender_id>/agreements/<int:agreement_id>/edit/', 
             views.edit_framework_agreement_view, name='edit-framework-agreement'),
    ])),
    
    # Search and Reports URLs
    path('search/', views.search_view, name='search'),
    path('reports/', views.reports_view, name='reports'),
    path('tender/<int:pk>/', views.TenderDetailView.as_view(), name='tender-detail'),
      # Shop URLs
    path('shop/', views.shop_view, name='shop'),
    path('orders/', views.order_list_view, name='order-list'),
    path('shop/add-to-order/<int:item_id>/', views.add_to_order_view, name='add-to-order'),
    
    # ISO URLs
    path('iso-generator/', views.iso_generator_view, name='iso-generator'),
    path('iso/create/', views.iso_generator_view, name='iso-create'),  # Alias for iso-generator
    path('iso-generator/<int:tender_id>/', views.iso_generator_view, name='iso-generator-for-tender'),
    path('iso/<int:iso_id>/', views.iso_detail_view, name='iso-detail'),
    path('iso/list/', views.iso_list_view, name='iso-list'),

    # Dashboard URL
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Chemical Management URLs
    path('chemicals/', include([
        path('', views.chemical_list, name='chemical_list'),
        path('create/', views.chemical_create, name='chemical_create'),
        path('import/', views.chemical_import, name='chemical_import'),
        path('<int:pk>/', views.chemical_detail, name='chemical_detail'),
        path('<int:pk>/update/', views.chemical_update, name='chemical_update'),
        path('spec/<int:pk>/delete/', views.chemical_spec_delete, name='chemical_spec_delete'),
    ])),    # Task Management URLs
    path('tasks/', include([
        path('', views.task_list, name='task_list'),
        path('dashboard/', views.task_dashboard, name='task_dashboard'),
        path('create/', views.task_create, name='task_create'),
        path('<int:pk>/', views.task_detail, name='task_detail'),
        path('<int:pk>/update/', views.task_update, name='task_update'),
        path('<int:pk>/delete/', views.task_delete, name='task_delete'),
        path('<int:pk>/status/', views.task_status_update, name='task_status_update'),
        path('categories/create/', views.task_category_create, name='task_category_create'),
    ])),
    
    # User Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile-update'),
]
