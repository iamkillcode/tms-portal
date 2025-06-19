"""
Views package for the tender application.

This package contains views for different aspects of the tender application.
All views from submodules are imported here to maintain backward compatibility.
"""

# Import all views from the separate modules to maintain the same API
from .auth_views import *
from .tender_views import *
from .vendor_views import *
from .framework_views import *
from .iso_views import *
from .task_views import *
from .chemical_views import *
from .order_views import *
from .report_views import *
from .dashboard_views import *
