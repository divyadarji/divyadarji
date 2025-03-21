// Chat widget functionality
document.addEventListener('DOMContentLoaded', function () {
    const chatToggle = document.getElementById('chat-widget-toggle');
    const chatContainer = document.getElementById('chat-container');
    const closeChat = document.getElementById('close-chat');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Set your deployed API URL
    const API_URL = 'http://127.0.0.1:5000/api/chat';

    // Toggle chat visibility
    chatToggle.addEventListener('click', function () {
        chatContainer.classList.add('active');
        userInput.focus();
    });

    // Close chat
    closeChat.addEventListener('click', function () {
        chatContainer.classList.remove('active');
    });

    // Function to add a message to the chat
    // Function to add a message to the chat
    // Function to add a message to the chat
    // Function to add a message to the chat
    // Function to add a message to the chat
    function addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');

        // Render HTML so links are clickable
        messageContent.innerHTML = message;

        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);

        // Scroll to the bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }





    // Function to send user message to API
    async function sendMessage(message) {
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('Error:', error);
            return 'Sorry, there was an error processing your request.';
        }
    }

    // Handle send button click
    sendButton.addEventListener('click', async function () {
        const message = userInput.value.trim();
        if (message) {
            // Add user message to chat
            addMessage(message, true);
            userInput.value = '';

            // Show loading indicator
            const loadingMessage = 'Thinking...';
            const loadingDiv = document.createElement('div');
            loadingDiv.classList.add('message', 'bot-message');
            loadingDiv.innerHTML = `<div class="message-content">${loadingMessage}</div>`;
            chatMessages.appendChild(loadingDiv);

            // Get response from API
            const botResponse = await sendMessage(message);

            // Remove loading indicator
            chatMessages.removeChild(loadingDiv);

            // Add bot response to chat
            addMessage(botResponse, false);
        }
    });

    // Handle Enter key press
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });
});