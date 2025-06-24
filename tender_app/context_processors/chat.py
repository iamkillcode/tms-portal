"""
Context processor for chat-related data
"""
from django.db.models import Count, Q
from tender_app.models import ChatMessage, ChatRoom

def unread_messages(request):
    """Add unread message count to all templates"""
    if not request.user.is_authenticated:
        return {'unread_chat_count': 0}
    
    try:
        # Get count of distinct messages that are unread
        unread_count = ChatMessage.objects.filter(
            room__participants__user=request.user
        ).exclude(
            read_by=request.user
        ).distinct().count()
        
        return {'unread_chat_count': unread_count}
    except Exception:
        # Handle the case where tables might not exist yet
        return {'unread_chat_count': 0}
