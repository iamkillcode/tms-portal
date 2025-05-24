from django.urls import path
from . import views

app_name = 'audit_trail'

urlpatterns = [
    path('', views.audit_trail_dashboard, name='dashboard'),
    path('export/csv/', views.export_audit_logs, {'format': 'csv'}, name='export_csv'),
    path('export/excel/', views.export_audit_logs, {'format': 'excel'}, name='export_excel'),
    path('tender_activity/', views.audit_trail_dashboard, name='tender_activity'),  # Admins see all audit logs here
]
