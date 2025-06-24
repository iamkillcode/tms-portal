"""
A simple script to check the latest messages in the chat system.
Run this script after sending messages to verify they are being saved.
"""

import os
import sys
import django

# Set up Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tender.settings')
django.setup()

# Now import Django models
from tender_app.models import ChatRoom, ChatMessage
from django.contrib.auth.models import User

def get_latest_messages():
    """Get the most recent messages in the chat system"""
    
    # Count rooms and messages
    room_count = ChatRoom.objects.count()
    message_count = ChatMessage.objects.count()
    
    print(f"Total chat rooms: {room_count}")
    print(f"Total messages: {message_count}")
    
    # Get the latest messages
    latest_messages = ChatMessage.objects.all().order_by('-timestamp')[:10]
    
    print("\nLatest messages:")
    print("===============")
    
    if latest_messages:
        for i, msg in enumerate(latest_messages, 1):
            room_name = msg.room.name
            sender = msg.sender.username
            timestamp = msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            content = msg.content
            
            print(f"{i}. [{timestamp}] {sender} in '{room_name}': {content}")
    else:
        print("No messages found.")
    
    # Check if any new messages were added in the last hour
    from django.utils import timezone
    now = timezone.now()
    one_hour_ago = now - timezone.timedelta(hours=1)
    
    recent_count = ChatMessage.objects.filter(timestamp__gte=one_hour_ago).count()
    print(f"\nMessages sent in the last hour: {recent_count}")

if __name__ == "__main__":
    get_latest_messages()
