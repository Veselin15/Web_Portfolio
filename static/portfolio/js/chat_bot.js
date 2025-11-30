// Toggle Chat Window
function toggleChat() {
    const chatWindow = document.getElementById('chat-window-wrapper');
    const btn = document.getElementById('chat-toggle-btn');

    // Toggle visibility class
    if (chatWindow.classList.contains('hidden')) {
        chatWindow.classList.remove('hidden');
        // Скриваме бутона, когато чатът е отворен (опционално, по-чисто е)
        btn.style.display = 'none';
    } else {
        chatWindow.classList.add('hidden');
        btn.style.display = 'flex';
    }
}

// Затваряне от хикса горе
// (Функцията е същата, просто викаме toggleChat)

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

    // User Message
    chatWindow.innerHTML += `<div class="msg user">${message}</div>`;
    inputField.value = '';
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Bot Typing...
    const tempId = `temp-${Date.now()}`;
    chatWindow.innerHTML += `<div class="msg bot" id="${tempId}">...</div>`;
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
        const response = await fetch(`http://localhost:8001/api/chat?message=${encodeURIComponent(message)}`, {
            method: 'POST'
        });
        const data = await response.json();
        pollResult(data.task_id, tempId);
    } catch (error) {
        document.getElementById(tempId).innerHTML = "Error connecting.";
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
                clearInterval(interval);
                const chatWindow = document.getElementById('chat-window');
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }
        } catch (e) {
            clearInterval(interval);
        }
    }, 1000);
}