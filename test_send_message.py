"""
Test script to verify message sending functionality
"""
import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tender.settings')
django.setup()

# Now we can import Django models
from django.contrib.auth.models import User
from tender_app.models import ChatRoom, ChatMessage

def test_send_message():
    """Test creating and retrieving a message"""
    print("Testing chat message functionality...")
    
    # Get first user
    try:
        user = User.objects.first()
        if not user:
            print("Error: No users in database")
            return
        print(f"Using user: {user.username}")
        
        # Get first chat room
        room = ChatRoom.objects.first()
        if not room:
            print("Error: No chat rooms in database")
            return
        print(f"Using room: {room.name} (ID: {room.id})")
        
        # Count messages before
        count_before = ChatMessage.objects.filter(room=room).count()
        print(f"Message count before: {count_before}")
        
        # Create a test message
        test_content = "This is a test message from script"
        message = ChatMessage.objects.create(
            room=room,
            sender=user,
            content=test_content
        )
        message.read_by.add(user)
        print(f"Created message: ID={message.id}")
        
        # Verify message was saved
        count_after = ChatMessage.objects.filter(room=room).count()
        print(f"Message count after: {count_after}")
        
        # Verify message can be retrieved
        saved_message = ChatMessage.objects.get(id=message.id)
        print(f"Retrieved message content: {saved_message.content}")
        
        # Check that the message is in the expected room
        room_messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')[:5]
        print("\nLatest messages in room:")
        for msg in room_messages:
            print(f"- {msg.sender.username}: {msg.content}")
        
        if count_after > count_before:
            print("\n✅ Test passed! Message was saved successfully.")
        else:
            print("\n❌ Test failed! Message count did not increase.")
            
    except Exception as e:
        print(f"\n❌ Error during test: {e}")

if __name__ == "__main__":
    test_send_message()
