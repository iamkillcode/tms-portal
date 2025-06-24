"""
Debug script to verify the chat messaging system functionality
"""
import os
import sys
import django
import json
import time
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tender.settings')
django.setup()

# Import required models
from django.contrib.auth.models import User
from tender_app.models import ChatRoom, ChatMessage, ChatParticipant

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 50)
    print(f" {text} ".center(50, '='))
    print("=" * 50)

def print_section(text):
    """Print a formatted section header"""
    print("\n" + "-" * 40)
    print(f" {text} ".center(40, '-'))
    print("-" * 40)

def debug_messages():
    """Test the complete message flow"""
    print_header("CHAT MESSAGING SYSTEM DIAGNOSTICS")
    
    # Get all users
    print_section("Users")
    users = User.objects.all()
    print(f"Found {users.count()} users")
    for i, user in enumerate(users[:5], 1):
        print(f"{i}. {user.username} ({user.email})")
    
    # Get all chat rooms
    print_section("Chat Rooms")
    rooms = ChatRoom.objects.all()
    print(f"Found {rooms.count()} chat rooms")
    for i, room in enumerate(rooms, 1):
        participants = room.participants.all()
        participants_str = ", ".join([p.user.username for p in participants])
        message_count = room.messages.count()
        print(f"{i}. {room.name} (ID: {room.id}) - Participants: {participants_str} - Messages: {message_count}")
    
    if not rooms.exists():
        print("No chat rooms found. Creating a test room...")
        if users.count() >= 2:
            room = ChatRoom.objects.create(
                name="Test Chat Room",
                is_group=False
            )
            ChatParticipant.objects.create(room=room, user=users[0])
            ChatParticipant.objects.create(room=room, user=users[1])
            print(f"Created room: {room.name} (ID: {room.id})")
        else:
            print("Not enough users to create a chat room. Need at least 2 users.")
            return
    
    # Select the first room for testing
    test_room = rooms.first()
    
    print_section(f"Messages in Room: {test_room.name} (ID: {test_room.id})")
    messages = ChatMessage.objects.filter(room=test_room).order_by('timestamp')
    print(f"Found {messages.count()} messages")
    
    for i, message in enumerate(messages[:10], 1):
        read_by_count = message.read_by.count()
        read_by = ", ".join([u.username for u in message.read_by.all()])
        print(f"{i}. [{message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {message.sender.username}: {message.content[:50]}... (Read by: {read_by or 'nobody'})")
    
    # Test creating a new message
    print_section("Creating Test Message")
    if users.exists():
        test_user = users.first()
        test_content = f"Test message sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        try:
            new_message = ChatMessage.objects.create(
                room=test_room,
                sender=test_user,
                content=test_content
            )
            new_message.read_by.add(test_user)
            print(f"Message created successfully!")
            print(f"ID: {new_message.id}")
            print(f"Content: {new_message.content}")
            print(f"Sender: {new_message.sender.username}")
            print(f"Timestamp: {new_message.timestamp}")
            print(f"Room: {new_message.room.name}")
            print(f"Read by: {test_user.username}")
        except Exception as e:
            print(f"Error creating message: {e}")
    
    print_section("Database Integrity Check")
    # Count messages again to verify the new message was saved
    new_count = ChatMessage.objects.filter(room=test_room).count()
    print(f"Messages in room before: {messages.count()}")
    print(f"Messages in room after: {new_count}")
    print(f"Difference: {new_count - messages.count()}")
    
    # Verify the latest message
    latest = ChatMessage.objects.filter(room=test_room).order_by('-timestamp').first()
    print(f"Latest message: {latest.content[:50]}...")
    
    print_header("DIAGNOSTICS COMPLETE")

if __name__ == "__main__":
    debug_messages()
