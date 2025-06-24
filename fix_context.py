"""
This script resolves the conflict between context_processors.py and the context_processors directory.
It ensures that the unread_messages context processor is available at the correct import path.
"""

import os
import shutil
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / 'tender_app'
CONTEXT_FILE = APP_DIR / 'context_processors.py'
CONTEXT_DIR = APP_DIR / 'context_processors'
INIT_FILE = CONTEXT_DIR / '__init__.py'
CHAT_FILE = CONTEXT_DIR / 'chat.py'

def main():
    print("Starting context processor fix...")
    
    # Step 1: Ensure the __init__.py imports the unread_messages function
    if INIT_FILE.exists():
        with open(INIT_FILE, 'r') as f:
            content = f.read()
        
        if 'from .chat import unread_messages' not in content:
            with open(INIT_FILE, 'w') as f:
                f.write(content + '\n\n# Import the unread_messages function\nfrom .chat import unread_messages\n')
            print("Updated __init__.py to import unread_messages")
        else:
            print("__init__.py already imports unread_messages")
    
    # Step 2: If a context_processors.py file exists, rename it to avoid confusion
    if CONTEXT_FILE.exists():
        backup_path = str(CONTEXT_FILE) + '.bak'
        shutil.copy2(CONTEXT_FILE, backup_path)
        print(f"Backed up {CONTEXT_FILE} to {backup_path}")
    
    # Step 3: Ensure the chat.py file has the complete unread_messages function
    ensure_chat_file_complete()
    
    print("Context processor fix completed!")

def ensure_chat_file_complete():
    """Ensure the chat.py file has the complete unread_messages function"""
    if not CHAT_FILE.exists():
        chat_content = """# filepath: tender_app/context_processors/chat.py
\"\"\"
Context processor for chat-related data
\"\"\"
from django.db.models import Count, Q
from tender_app.models import ChatMessage, ChatRoom

def unread_messages(request):
    \"\"\"Add unread message count to all templates\"\"\"
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
    except Exception as e:
        # Handle the case where tables might not exist yet
        print(f"Error in chat context processor: {e}")
        return {'unread_chat_count': 0}
"""
        with open(CHAT_FILE, 'w') as f:
            f.write(chat_content)
        print(f"Created {CHAT_FILE} with unread_messages function")
    else:
        print(f"{CHAT_FILE} already exists")

if __name__ == "__main__":
    main()
