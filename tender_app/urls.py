from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render

# Import from the modular views structure
from .views import (
    auth_views as app_auth_views,
    dashboard_views,
    tender_views, 
    vendor_views,
    framework_views,
    iso_views,
    task_views,
    chemical_views,
    order_views,
    report_views
)

def registration_disabled(request):
    return render(request, 'registration_disabled.html')

urlpatterns = [
    # Authentication URLs
    path('', dashboard_views.dashboard_view, name='dashboard'),  # Make dashboard the root URL
    path('login/', app_auth_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),    path('register/', registration_disabled, name='register'),  # Disabled registration
    # Tender URLs
    path('tender-generator/', tender_views.tender_generator_view, name='tender-generator'),
    path('tender/create/', tender_views.tender_generator_view, name='tender-create'),  # Alias for tender-generator
      # Vendor Management URLs
    path('vendors/', vendor_views.vendor_list_view, name='vendor-list'),
    path('vendors/create/', vendor_views.vendor_create_view, name='vendor-create'),
    path('vendors/<int:vendor_id>/', vendor_views.vendor_detail_view, name='vendor-detail'),
    path('vendors/<int:vendor_id>/update/', vendor_views.vendor_update_view, name='vendor-update'),    path('vendors/<int:vendor_id>/delete/', vendor_views.vendor_delete_view, name='vendor-delete'),
    # Framework Agreements URL - all agreements
    path('agreements/', framework_views.all_framework_agreements_view, name='all-framework-agreements'),
    # Tender Management URLs
    path('tenders/', include([
        path('list/', tender_views.tender_list_view, name='tender-list'),
        path('activity/', tender_views.tender_activity_view, name='tender-activity'),
        path('<int:tender_id>/update/', tender_views.tender_update_view, name='tender-update'),        path('export/', tender_views.export_tenders_view, name='export-tenders'),
        # Tender Items URLs
        path('<int:tender_id>/items/', tender_views.tender_items_view, name='tender-items'),
        path('<int:tender_id>/items/<int:item_id>/edit/', tender_views.edit_tender_item_view, name='edit-tender-item'),
        # Vendor Bids URLs
        path('<int:tender_id>/items/<int:item_id>/bids/', vendor_views.vendor_bids_view, name='vendor-bids'),        path('<int:tender_id>/items/<int:item_id>/bids/<int:bid_id>/edit/', 
             vendor_views.edit_vendor_bid_view, name='edit-vendor-bid'),
        # Framework Agreement URLs
        path('<int:tender_id>/agreements/', framework_views.framework_agreements_view, name='framework-agreements'),
        path('<int:tender_id>/agreements/<int:agreement_id>/edit/', 
             framework_views.edit_framework_agreement_view, name='edit-framework-agreement'),    ])),
    # Search and Reports URLs
    path('search/', tender_views.search_view, name='search'),
    path('reports/', report_views.reports_view, name='reports'),
    path('tender/<int:pk>/', tender_views.TenderDetailView.as_view(), name='tender-detail'),
    # Shop URLs
    path('shop/', order_views.shop_view, name='shop'),
    path('orders/', order_views.order_list_view, name='order-list'),    path('shop/add-to-order/<int:item_id>/', order_views.add_to_order_view, name='add-to-order'),
    # ISO URLs
    path('iso-generator/', iso_views.iso_generator_view, name='iso-generator'),
    path('iso/create/', iso_views.iso_generator_view, name='iso-create'),  # Alias for iso-generator
    path('iso-generator/<int:tender_id>/', iso_views.iso_generator_view, name='iso-generator-for-tender'),    path('iso/<int:iso_id>/', iso_views.iso_detail_view, name='iso-detail'),
    path('iso/list/', iso_views.iso_list_view, name='iso-list'),
    # Dashboard URL
    path('dashboard/', dashboard_views.dashboard_view, name='dashboard'),
    # Chemical Management URLs
    path('chemicals/', include([
        path('', chemical_views.chemical_list, name='chemical_list'),
        path('create/', chemical_views.chemical_create, name='chemical_create'),
        path('import/', chemical_views.chemical_import, name='chemical_import'),
        path('<int:pk>/', chemical_views.chemical_detail, name='chemical_detail'),
        path('<int:pk>/update/', chemical_views.chemical_update, name='chemical_update'),        path('spec/<int:pk>/delete/', chemical_views.chemical_spec_delete, name='chemical_spec_delete'),
    ])),
    # Task Management URLs
    path('tasks/', include([
        path('', task_views.task_list, name='task_list'),
        path('dashboard/', task_views.task_dashboard, name='task_dashboard'),
        path('create/', task_views.task_create, name='task_create'),
        path('<int:pk>/', task_views.task_detail, name='task_detail'),
        path('<int:pk>/update/', task_views.task_update, name='task_update'),
        path('<int:pk>/delete/', task_views.task_delete, name='task_delete'),
        path('<int:pk>/status/', task_views.task_status_update, name='task_status_update'),
        path('categories/create/', task_views.task_category_create, name='task_category_create'),
    ])),    
    # User Profile URLs
    path('profile/', app_auth_views.profile_view, name='profile'),
    path('profile/update/', app_auth_views.profile_update_view, name='profile-update'),
]
