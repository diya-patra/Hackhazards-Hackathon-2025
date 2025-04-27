document.addEventListener("DOMContentLoaded", function () {
    const messagesDiv = document.getElementById("messages");
    const group = "{{ group }}";  // This placeholder will not be evaluated here.
    const groupInput = document.querySelector('input[name="groupname"]');
    const groupName = groupInput ? groupInput.value : "";

    function fetchMessages() {
        fetch(`/get_messages?groupname=${groupName}`)
            .then(response => response.json())
            .then(data => {
                if (Array.isArray(data.messages)) {
                    messagesDiv.innerHTML = "";
                    data.messages.forEach(msg => {
                        const p = document.createElement("p");
                        p.innerHTML = `<strong>${msg.sender}:</strong> ${msg.message}`;
                        messagesDiv.appendChild(p);
                    });
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
            })
            .catch(error => console.error("Error fetching messages:", error));
    }

    // Fetch messages every 3 seconds
    setInterval(fetchMessages, 3000);
    fetchMessages(); // initial load
});