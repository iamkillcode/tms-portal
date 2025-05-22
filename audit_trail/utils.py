from django.contrib.contenttypes.models import ContentType
from .models import AuditLog

def log_user_action(user, action_type, content_object=None, action_detail='', ip_address=None, user_agent=''):
    """
    Manually log a user action.
    
    Args:
        user: The user performing the action
        action_type: Type of action (must be one of AuditLog.ACTION_TYPES)
        content_object: The object being acted upon (optional)
        action_detail: Additional details about the action (optional)
        ip_address: IP address of the user (optional)
        user_agent: User agent string (optional)
    
    Returns:
        The created AuditLog instance
    """
    # Validate action_type
    valid_actions = [action[0] for action in AuditLog.ACTION_TYPES]
    if action_type not in valid_actions:
        action_type = 'OTHER'
    
    # Create the audit log entry
    audit_log = AuditLog(
        user=user,
        action_type=action_type,
        action_detail=action_detail,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    # Add content object if provided
    if content_object:
        audit_log.content_type = ContentType.objects.get_for_model(content_object)
        audit_log.object_id = content_object.pk
        audit_log.object_repr = str(content_object)
        audit_log.app_name = content_object._meta.app_label
        audit_log.model_name = content_object._meta.model_name
    
    audit_log.save()
    return audit_log


def get_request_data(request):
    """
    Extract common request data for audit logging.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Dict with IP address and user agent
    """
    # Get IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    
    # Get user agent
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    return {
        'ip_address': ip_address,
        'user_agent': user_agent
    }


def log_tender_action(request, tender, action_type, action_detail=''):
    """
    Log a tender-specific action.
    
    Args:
        request: The HTTP request
        tender: The tender object
        action_type: Type of action
        action_detail: Additional details
        
    Returns:
        The created AuditLog instance
    """
    request_data = get_request_data(request)
    
    return log_user_action(
        user=request.user if request.user.is_authenticated else None,
        action_type=action_type,
        content_object=tender,
        action_detail=action_detail,
        ip_address=request_data['ip_address'],
        user_agent=request_data['user_agent']
    )


def log_iso_action(request, iso, action_type, action_detail=''):
    """
    Log an ISO-specific action.
    
    Args:
        request: The HTTP request
        iso: The ISO object
        action_type: Type of action
        action_detail: Additional details
        
    Returns:
        The created AuditLog instance
    """
    request_data = get_request_data(request)
    
    return log_user_action(
        user=request.user if request.user.is_authenticated else None,
        action_type=action_type,
        content_object=iso,
        action_detail=action_detail,
        ip_address=request_data['ip_address'],
        user_agent=request_data['user_agent']
    )
