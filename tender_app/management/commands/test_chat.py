from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tender_app.models import ChatRoom, ChatMessage, ChatParticipant
import random

class Command(BaseCommand):
    help = 'Test the chat functionality by creating test messages'

    def handle(self, *args, **kwargs):
        # Check if there are any users and rooms
        if User.objects.count() == 0:
            self.stdout.write(self.style.ERROR('No users found in the database'))
            return
        
        if ChatRoom.objects.count() == 0:
            self.stdout.write(self.style.ERROR('No chat rooms found in the database'))
            return
            
        # Get a user and room
        users = User.objects.all()
        room = ChatRoom.objects.first()
        
        # Make sure the user is a participant in the room
        for user in users[:2]:
            if not ChatParticipant.objects.filter(room=room, user=user).exists():
                ChatParticipant.objects.create(room=room, user=user)
                self.stdout.write(self.style.SUCCESS(f'Added {user.username} to room {room.name}'))
        
        # Create test messages
        test_messages = [
            "Hello, this is a test message!",
            "How are you doing today?",
            "This is a test of the chat functionality.",
            "Let me know if this message appears in your chat.",
            "Testing 1, 2, 3...",
        ]
        
        # Create messages from both users
        for i, content in enumerate(test_messages):
            user = users[i % 2]  # Alternate between users
            message = ChatMessage.objects.create(
                room=room,
                sender=user,
                content=content
            )
            message.read_by.add(user)
            self.stdout.write(self.style.SUCCESS(f'Created message from {user.username}: "{content[:30]}..."'))
        
        self.stdout.write(self.style.SUCCESS('Test messages created successfully!'))
        self.stdout.write(f'Total messages in room {room.name}: {ChatMessage.objects.filter(room=room).count()}')
