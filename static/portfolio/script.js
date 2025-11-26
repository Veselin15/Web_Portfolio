/* portfolio/static/portfolio/script.js */

async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    const message = inputField.value;

    if (!message) return;

    // Show User Message
    chatWindow.innerHTML += `<div class="msg user">${message}</div>`;
    inputField.value = '';
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Call API
    try {
        const response = await fetch(`http://localhost:8001/api/chat?message=${encodeURIComponent(message)}`, {
            method: 'POST'
        });
        const data = await response.json();
        const taskId = data.task_id;

        chatWindow.innerHTML += `<div class="msg bot" id="temp-${taskId}"><i>Thinking...</i></div>`;
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Start Polling
        pollResult(taskId);

    } catch (error) {
        console.error(error);
        chatWindow.innerHTML += `<div class="msg bot" style="color:red;">Error connecting to API.</div>`;
    }
}

async function pollResult(taskId) {
    const tempMsg = document.getElementById(`temp-${taskId}`);

    const interval = setInterval(async () => {
        try {
            const res = await fetch(`http://localhost:8001/api/status/${taskId}`);
            const data = await res.json();

            if (data.status === 'Done') {
                tempMsg.innerHTML = data.result;
                tempMsg.style.fontStyle = 'normal';
                clearInterval(interval);
            }
        } catch (e) {
            console.error("Polling error", e);
            clearInterval(interval);
        }
    }, 1000);
}