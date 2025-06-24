// Chat auto-refresh and real-time features
document.addEventListener('DOMContentLoaded', function() {
    // Chat message handling
    initChatFunctionality();
    
    // Check for new messages periodically
    setInterval(checkForNewMessages, 10000); // Every 10 seconds
});

/**
 * Initialize chat functionality
 */
function initChatFunctionality() {
    const messagesContainer = document.getElementById('messages-container');
    if (!messagesContainer) return;
    
    // Scroll to bottom on load
    scrollChatToBottom();
    
    // Setup for HTMX events
    setupHtmxEventHandling();
    
    // Message input behavior
    const messageInput = document.getElementById('message-input');
    if (messageInput) {
        // Auto-resize the input field as user types
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            const newHeight = Math.min(this.scrollHeight, 150);
            this.style.height = newHeight + 'px';
        });
        
        // Focus input when page loads
        messageInput.focus();
        
        // Handle enter key to send (shift+enter for new line)
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                document.getElementById('message-form').dispatchEvent(new Event('submit'));
            }
        });
    }
    
    // Listen for new messages indicator
    document.body.addEventListener('messageAdded', function(evt) {
        // Play sound notification
        playNotificationSound();
        // Update page title with notification
        updateTitleWithNotification();
        // Scroll to bottom
        scrollChatToBottom();
    });
}

/**
 * Scroll chat container to bottom
 */
function scrollChatToBottom() {
    const messagesContainer = document.getElementById('messages-container');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

/**
 * Check for new messages
 */
function checkForNewMessages() {
    // The messages will be checked via htmx polling
    // This function can be extended for additional functionality
}

/**
 * Play notification sound for new messages
 */
function playNotificationSound() {
    // Add sound notification if needed
    // const audio = new Audio('/static/sounds/notification.mp3');
    // audio.play().catch(err => console.warn('Could not play notification sound', err));
}

/**
 * Update page title with notification
 */
function updateTitleWithNotification() {
    const originalTitle = document.title;
    document.title = '(New message) ' + originalTitle;
    
    // Reset title when window gets focus
    window.addEventListener('focus', function onFocus() {
        document.title = originalTitle;
        window.removeEventListener('focus', onFocus);
    });
}

/**
 * Set up HTMX event handling for chat
 */
function setupHtmxEventHandling() {
    // Handle successful message sending
    document.body.addEventListener('htmx:afterRequest', function(evt) {
        if (evt.detail.elt && evt.detail.elt.id === 'message-form' && evt.detail.successful) {
            // If the response has an HX-Trigger header for messageAdded
            const messageAddedData = evt.detail.headers ? 
                evt.detail.headers['HX-Trigger'] : null;
            
            if (messageAddedData) {
                try {
                    // Try to parse the JSON data if available
                    const triggerData = JSON.parse(messageAddedData);
                    if (triggerData.messageAdded) {
                        console.log('Message added with data:', triggerData.messageAdded);
                        // Create and dispatch custom event with message data
                        document.body.dispatchEvent(
                            new CustomEvent('messageAdded', { detail: triggerData.messageAdded })
                        );
                    }
                } catch (e) {
                    // If it's not JSON, it might be a simple string trigger
                    if (messageAddedData === 'messageAdded') {
                        console.log('Message added (simple trigger)');
                        document.body.dispatchEvent(new CustomEvent('messageAdded'));
                    }
                }
            }
            
            // Always clear the form after a successful request
            document.getElementById('message-form').reset();
        }
    });

    // Error handling
    document.body.addEventListener('htmx:responseError', function(evt) {
        console.error('HTMX Response Error:', evt.detail);
        // Show error in UI
        const messagesContainer = document.getElementById('messages-container');
        if (messagesContainer && evt.detail.elt && evt.detail.elt.id === 'message-form') {
            // Remove any temporary messages
            const tempMessages = document.querySelectorAll('[id^="temp-message-"]');
            tempMessages.forEach(el => el.remove());
            
            // Show error notification
            const errorMessage = document.createElement('div');
            errorMessage.className = 'alert alert-danger mt-2 mb-2 message-error';
            errorMessage.textContent = 'Failed to send message. Please try again.';
            messagesContainer.appendChild(errorMessage);
            
            // Remove error after 3 seconds
            setTimeout(() => {
                if (errorMessage.parentNode) {
                    errorMessage.parentNode.removeChild(errorMessage);
                }
            }, 3000);
        }
    });
}
