document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatLog = document.getElementById('chat-log');
    const inputLangSelector = document.getElementById('input-lang'); // Get the language selector

    function addMessageToChatLog(sender, messageEn, messageNl) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');

        if (sender === 'user') {
            // For user messages, we only display what they typed
            // In a real app, you might want to show their chosen language label
            messageDiv.innerHTML = `<span>${messageEn}</span>`;
        } else {
            // For bot messages, display both English and Dutch
            messageDiv.innerHTML = `
                <span class="lang-en">${messageEn}</span><br>
                <span class="lang-nl">${messageNl}</span>
            `;
        }

        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll to the bottom
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        const selectedLang = inputLangSelector.value; // Get the currently selected language
        if (message === '') return;

        addMessageToChatLog('user', message); // Display user's message

        userInput.value = ''; // Clear input field

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Send both the message AND the selected language to the backend
                body: JSON.stringify({ message: message, lang: selectedLang })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            addMessageToChatLog('bot', data.en_response, data.nl_response);

        } catch (error) {
            console.error('Error sending message:', error);
            addMessageToChatLog('bot',
                "Sorry, I'm having trouble connecting right now. Please try again.",
                "Sorry, ik kan nu geen verbinding maken. Probeer het opnieuw.");
        }
    }

    sendButton.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});