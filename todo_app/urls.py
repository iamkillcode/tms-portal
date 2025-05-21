from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.todo_dashboard, name='todo_dashboard'),
    
    # List views
    path('lists/', views.todo_list_view, name='todo_list_view'),
    path('lists/create/', views.todo_list_create, name='todo_list_create'),
    path('lists/<int:list_id>/', views.todo_list_detail, name='todo_list_detail'),
    path('lists/<int:list_id>/update/', views.todo_list_update, name='todo_list_update'),
    path('lists/<int:list_id>/delete/', views.todo_list_delete, name='todo_list_delete'),
    
    # Item views
    path('items/create/', views.todo_item_create, name='todo_item_create'),
    path('items/<int:item_id>/', views.todo_item_detail, name='todo_item_detail'),
    path('items/<int:item_id>/update/', views.todo_item_update, name='todo_item_update'),
    path('items/<int:item_id>/delete/', views.todo_item_delete, name='todo_item_delete'),
    path('items/<int:item_id>/status/', views.todo_item_status_update, name='todo_item_status_update'),
    
    # Calendar view
    path('calendar/', views.todo_calendar, name='todo_calendar'),
    
    # Export
    path('export/', views.todo_export, name='todo_export'),
]
