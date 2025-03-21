// static/js/chat.js
document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    console.log("Chat interface initialized");

    // Function to add a message to the chat
    function addMessage(message, isUser) {
        console.log(`Adding ${isUser ? 'user' : 'bot'} message: ${message.substring(0, 50)}...`);
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.textContent = message;

        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to send user message to the backend
    async function sendMessage(message) {
        console.log(`Sending message to backend: ${message}`);
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            console.log(`Received response with status: ${response.status}`);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error(`Server error: ${response.status} - ${errorText}`);
                return `Error ${response.status}: ${errorText}`;
            }

            const data = await response.json();
            console.log(`Parsed response data`);
            return data.response;
        } catch (error) {
            console.error('Fetch error:', error);
            return `Network error: ${error.message}`;
        }
    }

    // Handle send button click
    sendButton.addEventListener('click', async function() {
        console.log("Send button clicked");
        const message = userInput.value.trim();
        if (message) {
            console.log(`Processing user message: ${message}`);
            // Add user message to chat
            addMessage(message, true);
            userInput.value = '';
            
            // Show loading indicator
            const loadingMessage = 'Thinking...';
            const loadingDiv = document.createElement('div');
            loadingDiv.classList.add('message', 'bot-message');
            loadingDiv.innerHTML = `<div class="message-content">${loadingMessage}</div>`;
            chatMessages.appendChild(loadingDiv);
            
            // Get response from backend
            console.log("Awaiting response from backend");
            const botResponse = await sendMessage(message);
            
            // Remove loading indicator
            console.log("Removing loading indicator");
            chatMessages.removeChild(loadingDiv);
            
            // Add bot response to chat
            console.log("Adding bot response to chat");
            addMessage(botResponse, false);
        } else {
            console.log("Empty message, not sending");
        }
    });

    // Handle Enter key press
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            console.log("Enter key pressed, triggering send");
            sendButton.click();
        }
    });
    
    // Test network connectivity
    fetch('/').then(() => {
        console.log("Basic connectivity test successful");
    }).catch(error => {
        console.error("Basic connectivity test failed:", error);
    });
});