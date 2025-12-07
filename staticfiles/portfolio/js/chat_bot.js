// Toggle Chat Window
function toggleChat() {
    const chatWindow = document.getElementById('chat-window-wrapper');
    const btn = document.getElementById('chat-toggle-btn');

    if (chatWindow.classList.contains('hidden')) {
        chatWindow.classList.remove('hidden');
        btn.style.display = 'none';
    } else {
        chatWindow.classList.add('hidden');
        btn.style.display = 'flex';
    }
}

function handleEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    
    // 1. Взимаме текста ПРЕДИ да изчистим полето
    const message = inputField.value.trim();

    if (!message) return; // Ако е празно, спираме

    // 2. Показваме съобщението на екрана
    chatWindow.innerHTML += `<div class="msg user">${message}</div>`;
    inputField.value = ''; // Чак сега чистим полето
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // 3. Показваме "..." докато мисли
    const tempId = `temp-${Date.now()}`;
    chatWindow.innerHTML += `<div class="msg bot" id="${tempId}">...</div>`;
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
        console.log("Sending message:", message); // Debug

        // 4. Изпращаме към /api/chat (относителен път)
        const response = await fetch('/api/chat?message=' + encodeURIComponent(message), {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log("Task ID received:", data.task_id); // Debug

        if (data.task_id) {
            pollResult(data.task_id, tempId);
        } else {
            document.getElementById(tempId).innerHTML = "Error: No Task ID.";
        }

    } catch (error) {
        console.error(error);
        const errElement = document.getElementById(tempId);
        if (errElement) errElement.innerHTML = "Error connecting to AI.";
    }
}

async function pollResult(taskId, tempMsgId) {
    const tempMsg = document.getElementById(tempMsgId);
    if (!tempMsg) return;

    let attempts = 0;
    const maxAttempts = 30; // 30 секунди максимум

    const interval = setInterval(async () => {
        attempts++;
        try {
            // 5. Питаме за статус
            const res = await fetch(`/api/status/${taskId}`);
            
            if (!res.ok) {
                // Ако API върне 404, значи задачата още не е готова или липсва
                console.log("Waiting for task..."); 
                if (attempts > maxAttempts) {
                    clearInterval(interval);
                    tempMsg.innerHTML = "AI took too long to respond.";
                }
                return;
            }

            const data = await res.json();

            if (data.status === 'Done') {
                tempMsg.innerHTML = data.result; // Показваме отговора
                clearInterval(interval);
                const chatWindow = document.getElementById('chat-window');
                chatWindow.scrollTop = chatWindow.scrollHeight;
            } else if (data.status === 'FAILURE') {
                tempMsg.innerHTML = "AI Failed.";
                clearInterval(interval);
            }
        } catch (e) {
            console.error("Polling error:", e);
            clearInterval(interval);
            tempMsg.innerHTML = "Connection lost.";
        }
    }, 1000);
}
