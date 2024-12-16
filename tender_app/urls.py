from django.urls import path
from . import views  # Import the views from app

urlpatterns = [
    path('tender-generator/', views.tender_generator_view, name='tender_generator'),
]
