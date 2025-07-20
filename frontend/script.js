document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chat-history');
    const chatMessages = document.getElementById('chat-messages');
    const promptInput = document.getElementById('prompt-input');
    const sendButton = document.getElementById('send-button');
    const agentList = document.getElementById('agent-list');
    const addAgentButton = document.getElementById('add-agent-button');
    const newAgentNameInput = document.getElementById('new-agent-name');

    // Dummy data for chat history
    const history = [
        { id: 1, name: 'Chat 1', messages: [{ sender: 'user', text: 'Hello!' }, { sender: 'agent', text: 'Hi there!' }] },
        { id: 2, name: 'Chat 2', messages: [{ sender: 'user', text: 'How are you?' }, { sender: 'agent', text: 'I am fine, thank you.' }] },
        { id: 3, name: 'Chat 3', messages: [{ sender: 'user', text: 'What is your name?' }, { sender: 'agent', text: 'I am a chatbot.' }] },
    ];

    // Populate chat history
    history.forEach(chat => {
        const listItem = document.createElement('li');
        listItem.textContent = chat.name;
        listItem.dataset.chatId = chat.id;
        chatHistory.appendChild(listItem);
    });

    // Handle chat history selection
    chatHistory.addEventListener('click', (e) => {
        if (e.target.tagName === 'LI') {
            const chatId = parseInt(e.target.dataset.chatId);
            const selectedChat = history.find(chat => chat.id === chatId);
            if (selectedChat) {
                chatMessages.innerHTML = '';
                selectedChat.messages.forEach(message => {
                    const messageElement = document.createElement('div');
                    messageElement.classList.add('message', message.sender === 'user' ? 'user-message' : 'agent-message');
                    messageElement.innerHTML = `<p>${message.text}</p>`;
                    chatMessages.appendChild(messageElement);
                });
            }
        }
    });

    // Handle sending messages
    sendButton.addEventListener('click', () => {
        const text = promptInput.value.trim();
        if (text) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', 'user-message');
            messageElement.innerHTML = `<p>${text}</p>`;
            chatMessages.appendChild(messageElement);
            promptInput.value = '';
            // TODO: Add agent response logic
        }
    });

    // Handle adding new agents
    addAgentButton.addEventListener('click', () => {
        const agentName = newAgentNameInput.value.trim();
        if (agentName) {
            const agentId = `agent${agentList.children.length + 1}`;
            const newAgent = document.createElement('div');
            newAgent.classList.add('agent');
            newAgent.innerHTML = `
                <input type="checkbox" id="${agentId}" name="${agentId}">
                <label for="${agentId}">${agentName}</label>
            `;
            agentList.appendChild(newAgent);
            newAgentNameInput.value = '';
        }
    });
});
