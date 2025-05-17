from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.dashboard_view, name='dashboard'),  # Make dashboard the root URL
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_view, name='register'),
      # Tender URLs
    path('tender-generator/', views.tender_generator_view, name='tender-generator'),
    path('tender/create/', views.tender_generator_view, name='tender-create'),  # Alias for tender-generator
    
    # Tender Management URLs
    path('tenders/', include([
        path('list/', views.tender_list_view, name='tender-list'),
        path('activity/', views.tender_activity_view, name='tender-activity'),
        path('<int:tender_id>/update/', views.tender_update_view, name='tender-update'),
        path('export/', views.export_tenders_view, name='export-tenders'),
    ])),
    
    # Search and Reports URLs
    path('search/', views.search_view, name='search'),
    path('reports/', views.reports_view, name='reports'),
    path('tender/<int:pk>/', views.TenderDetailView.as_view(), name='tender-detail'),
    
    # Shop URLs
    path('shop/', views.shop_view, name='shop'),
    path('orders/', views.order_list_view, name='order-list'),
    path('shop/add-to-order/<int:item_id>/', views.add_to_order_view, name='add-to-order'),    # ISO URLs
    path('iso-generator/', views.iso_generator_view, name='iso-generator'),
    path('iso/create/', views.iso_generator_view, name='iso-create'),  # Alias for iso-generator
    path('iso-generator/<int:tender_id>/', views.iso_generator_view, name='iso-generator-for-tender'),
    path('iso/<int:iso_id>/', views.iso_detail_view, name='iso-detail'),
    path('iso/list/', views.iso_list_view, name='iso-list'),

    # Dashboard URL
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
