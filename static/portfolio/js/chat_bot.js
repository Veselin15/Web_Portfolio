// Toggle Chat Widget (Minimize/Maximize)
function toggleChat() {
    const widget = document.getElementById('chat-widget');
    const icon = document.getElementById('chat-icon');

    // Toggle the 'minimized' class on the main wrapper
    widget.classList.toggle('minimized');

    // Change icon based on state
    if (widget.classList.contains('minimized')) {
        icon.classList.remove('fa-chevron-down');
        icon.classList.add('fa-chevron-up');
    } else {
        icon.classList.remove('fa-chevron-up');
        icon.classList.add('fa-chevron-down');
    }
}

// Allow sending message with "Enter" key
function handleEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    const message = inputField.value.trim();

    if (!message) return;

    // Show User Message
    chatWindow.innerHTML += `<div class="msg user">${message}</div>`;
    inputField.value = '';
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Call API
    try {
        // Show temporary thinking bubble
        const tempId = `temp-${Date.now()}`;
        chatWindow.innerHTML += `<div class="msg bot" id="${tempId}"><i>Thinking...</i></div>`;
        chatWindow.scrollTop = chatWindow.scrollHeight;

        const response = await fetch(`http://localhost:8001/api/chat?message=${encodeURIComponent(message)}`, {
            method: 'POST'
        });
        const data = await response.json();
        const taskId = data.task_id;

        // Start Polling for result
        pollResult(taskId, tempId);

    } catch (error) {
        console.error(error);
        chatWindow.innerHTML += `<div class="msg bot" style="color:red;">Error connecting to API.</div>`;
    }
}

async function pollResult(taskId, tempMsgId) {
    const tempMsg = document.getElementById(tempMsgId);
    if (!tempMsg) return;

    const interval = setInterval(async () => {
        try {
            const res = await fetch(`http://localhost:8001/api/status/${taskId}`);
            const data = await res.json();

            if (data.status === 'Done') {
                tempMsg.innerHTML = data.result;
                tempMsg.style.fontStyle = 'normal';
                clearInterval(interval);

                // Scroll to bottom again after receiving message
                const chatWindow = document.getElementById('chat-window');
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }
        } catch (e) {
            console.error("Polling error", e);
            clearInterval(interval);
        }
    }, 1000);
}