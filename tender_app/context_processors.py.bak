from django.db.models import Count
from .models import ChatMessage

def unread_messages(request):
    """Add unread message count to all templates"""
    if request.user.is_authenticated:
        try:
            unread_count = ChatMessage.objects.filter(
                room__participants__user=request.user
            ).exclude(read_by=request.user).distinct().count()
            return {'unread_chat_count': unread_count}
        except Exception as e:
            # Handle case where the table doesn't exist yet or other errors
            print(f"Error in unread_messages context processor: {str(e)}")
            return {'unread_chat_count': 0}
    return {'unread_chat_count': 0}