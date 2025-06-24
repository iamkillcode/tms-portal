# filepath: c:\Users\USER\Desktop\Dev\tender\tender_app\views.py
"""
This file is maintained for backward compatibility only.
All views have been moved to the views/ directory for better organization.
This file acts as a re-export layer for the modular views structure.
"""

# Import from the modular views structure
from .views.auth_views import *
from .views.dashboard_views import *
from .views.tender_views import *
from .views.vendor_views import *
from .views.framework_views import *
from .views.iso_views import *
from .views.task_views import *
from .views.chemical_views import *
from .views.order_views import *
from .views.report_views import *
from .views.chat_views import *

# Re-export common helper functions
from .views.tender_views import has_admin_role, has_user_role

# Common imports for backward compatibility
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timezone, timedelta
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db.models.functions import ExtractMonth
from django.urls import reverse
from django.utils import timezone as django_timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Import models and forms for backward compatibility
from .models import (
    TenderTracker, Department, Category, Tender, TenderItem,
    VendorBid, FrameworkAgreement, Vendor, ISONumber, ISOTracker,
    Division, UserProfile, BreakfastItem, Order, OrderItem,
    Chemical, ChemicalSpecification, Task, TaskCategory, TaskComment,
    ChatRoom, ChatMessage, ChatParticipant
)

from .forms import (
    CustomUserCreationForm, TenderItemForm, VendorBidForm,
    FrameworkAgreementForm, ChemicalForm, ChemicalSpecificationForm,
    ChemicalImportForm, TaskForm, TaskCategoryForm, TaskCommentForm,
    UserProfileForm, VendorForm
)

# Import other necessary modules for backward compatibility
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
import pandas as pd

# Note: All function definitions have been moved to their respective modules
# in the views/ directory. This file only re-exports them to maintain backward compatibility.
