from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Max, OuterRef, Subquery, Count, IntegerField
from django.utils import timezone
import json

from ..models import ChatRoom, ChatMessage, ChatParticipant, User
from ..htmx_utils import htmx_template

@login_required
def chat_home(request):
    """Main chat interface showing user conversations"""
    user = request.user
    
    try:
        # Get all rooms the user is part of
        rooms = ChatRoom.objects.filter(participants__user=user)
        
        if rooms.exists():
            # Handle each room individually to avoid complex subqueries
            room_data = []
            for room in rooms:
                # Get latest message
                latest_message = ChatMessage.objects.filter(room=room).order_by('-timestamp').first()
                
                # Count unread messages
                unread_count = ChatMessage.objects.filter(room=room).exclude(read_by=user).count()
                
                # Create a customized name for direct messages
                display_name = room.name
                if not room.is_group:
                    other_participant = room.participants.exclude(user=user).first()
                    if other_participant:
                        other_user = other_participant.user
                        display_name = f"Chat with {other_user.first_name or other_user.username}"
                
                room.display_name = display_name
                room.latest_message = latest_message.content if latest_message else None
                room.latest_timestamp = latest_message.timestamp if latest_message else None
                room.unread_count = unread_count
                
                room_data.append(room)
                
            # Sort by latest message timestamp
            rooms = sorted(room_data, key=lambda r: (r.latest_timestamp is not None, r.latest_timestamp), reverse=True)
        else:
            rooms = []
    except Exception as e:
        # Handle database errors
        print(f"Error fetching chat rooms: {e}")
        rooms = []
    
    # Get other users for the new chat modal
    other_users = User.objects.exclude(id=user.id)
    
    return render(request, 'chat/home.html', {
        'rooms': rooms,
        'users': other_users
    })

@login_required
def chat_room(request, room_id):
    """View for a specific chat room"""
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Ensure user is a participant
    if not room.participants.filter(user=request.user).exists():
        return redirect('chat_home')
    
    # Mark messages as read
    unread_messages = ChatMessage.objects.filter(
        room=room
    ).exclude(
        read_by=request.user
    )
    
    for message in unread_messages:
        message.read_by.add(request.user)
    
    # Customize room name for direct messages
    custom_room_name = room.name
    if not room.is_group:
        # For direct messages, show the other user's name
        other_participant = room.participants.exclude(user=request.user).first()
        if other_participant:
            other_user = other_participant.user
            custom_room_name = f"Chat with {other_user.first_name or other_user.username}"
    
    return render(request, 'chat/room.html', {
        'room': room,
        'custom_room_name': custom_room_name,
        'messages': room.messages.all().order_by('timestamp')
    })

@login_required
@htmx_template('chat/room.html', 'chat/messages_partial.html')
def load_messages(request, room_id):
    """Load messages with HTMX for real-time updates"""
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Ensure user is a participant
    if not room.participants.filter(user=request.user).exists():
        return {'error': 'Unauthorized'}
    
    # Mark messages as read
    unread_messages = ChatMessage.objects.filter(
        room=room
    ).exclude(
        read_by=request.user
    )
    
    for message in unread_messages:
        message.read_by.add(request.user)
    
    # Get the messages with the user object preloaded to avoid N+1 queries
    messages = ChatMessage.objects.filter(room=room).select_related('sender').order_by('timestamp')
    
    print(f"Loading messages for room {room.id} - {room.name}, found {messages.count()} messages")
    
    # If it's a messageRefresh trigger, include debug info in headers
    is_refresh = request.headers.get('HX-Trigger') == 'messageRefresh'
    if is_refresh:
        response = {
            'room': room,
            'messages': messages
        }
        # If this view is wrapped with htmx_template, this will be processed by the decorator
        return response
    
    return {
        'room': room,
        'messages': messages
    }

@login_required
def send_message(request, room_id):
    """Send a new message in a chat room"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
    
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Ensure user is a participant
    if not room.participants.filter(user=request.user).exists():
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'})
    
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'status': 'error', 'message': 'Empty message'})
    
    # Create message
    try:
        message = ChatMessage.objects.create(
            room=room,
            sender=request.user,
            content=content
        )
        print(f"Message created: ID={message.id}, Content={message.content}, Sender={message.sender}")
        
        # Mark as read by sender        message.read_by.add(request.user)
        
        # Check for HTMX request - multiple ways to detect
        is_htmx = False
        if hasattr(request, 'htmx'):
            is_htmx = request.htmx
        elif request.headers.get('HX-Request') == 'true':
            is_htmx = True
        print(f"Is HTMX request: {is_htmx}, Headers: {dict(request.headers)}")
        
        if is_htmx:
            # Trigger a reload of messages instead of trying to append
            response = JsonResponse({'status': 'success', 'message_id': message.id})
            response['HX-Trigger'] = json.dumps({
                'messageAdded': {
                    'message_id': message.id,
                    'timestamp': message.timestamp.isoformat()
                }
            })
            return response
        
        return JsonResponse({'status': 'success', 'message_id': message.id})
    except Exception as e:
        print(f"Error creating message: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def create_chat(request, user_id=None):
    """Create a new chat with another user or a group"""
    if user_id:
        # Direct message with another user
        other_user = get_object_or_404(User, id=user_id)
        
        # Check if chat already exists between these users
        existing_rooms = ChatRoom.objects.filter(
            is_group=False,
            participants__user=request.user
        ).filter(
            participants__user=other_user
        )
        
        if existing_rooms.exists():
            # Use existing room
            return redirect('chat_room', room_id=existing_rooms.first().id)
          # Create new room with a more neutral name
        current_user_name = request.user.first_name or request.user.username
        other_user_name = other_user.first_name or other_user.username
        room = ChatRoom.objects.create(
            name=f"Chat: {current_user_name} and {other_user_name}",
            is_group=False
        )
        
        # Add participants
        ChatParticipant.objects.create(room=room, user=request.user)
        ChatParticipant.objects.create(room=room, user=other_user)
        
        return redirect('chat_room', room_id=room.id)
    
    # Group chat creation form
    if request.method == 'POST':
        name = request.POST.get('name')
        participants = request.POST.getlist('participants')
        
        if name and participants:
            room = ChatRoom.objects.create(
                name=name,
                is_group=True
            )
            
            # Add creator
            ChatParticipant.objects.create(room=room, user=request.user)
            
            # Add other participants
            for user_id in participants:
                try:
                    user = User.objects.get(id=user_id)
                    ChatParticipant.objects.create(room=room, user=user)
                except User.DoesNotExist:
                    pass
            
            return redirect('chat_room', room_id=room.id)
    
    # Show form for creating group chat
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/create_group.html', {'users': users})