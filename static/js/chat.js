// ---------- Chatbot ----------
function sendToChatbot() {
    const userInput = document.getElementById("userInput").value;
    if (!userInput) return;

    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
    })
    .then(res => res.json())
    .then(data => {
        const chatBox = document.getElementById("chatResponse");
        const userDiv = `<p><strong>You:</strong> ${userInput}</p>`;
        const botDiv = `<p><strong>Bot:</strong> ${data.response}</p>`;
        chatBox.innerHTML += userDiv + botDiv;
        document.getElementById("userInput").value = "";
    });
}

// ---------- Group Chat ----------
function sendGroupMessage() {
    const username = document.getElementById("username").value || "Anonymous";
    const message = document.getElementById("groupMessage").value;
    if (!message) return;

    fetch('/api/group_chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, message })
    })
    .then(() => {
        document.getElementById("groupMessage").value = "";
        loadGroupChat();
    });
}

function loadGroupChat() {
    fetch('/api/group_chat')
    .then(res => res.json())
    .then(messages => {
        const chatBox = document.getElementById("groupChatBox");
        chatBox.innerHTML = "";
        messages.forEach(msg => {
            const entry = `<p><strong>${msg.username}:</strong> ${msg.message}</p>`;
            chatBox.innerHTML += entry;
        });
    });
}

// Load messages every 2 seconds
if (window.location.pathname === '/group') {
    setInterval(loadGroupChat, 2000);
    window.onload = loadGroupChat;
}
