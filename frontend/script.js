window.onload = loadChatHistory;

async function sendMessage() {

    const input =
        document.getElementById("message-input");

    const message = input.value;

    if (!message) return;

    const chatBox =
        document.getElementById("chat-box");

    chatBox.innerHTML +=
        `<div class="user">
            <b>You:</b> ${message}
        </div>`;

    input.value = "";

    chatBox.scrollTop =
        chatBox.scrollHeight;

    const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        }
    );

    const data = await response.json();

    chatBox.innerHTML +=
        `<div class="bot">
            <b>Bot:</b> ${data.response}
        </div>`;

    chatBox.scrollTop =
        chatBox.scrollHeight;
}

async function loadChatHistory() {

    const response = await fetch(
        "http://127.0.0.1:8000/chat-history"
    );

    const messages = await response.json();

    const chatBox =
        document.getElementById("chat-box");

    chatBox.innerHTML = "";

    messages.forEach(message => {

        if (message.sender === "user") {

            chatBox.innerHTML +=
                `<div class="user">
                    <b>You:</b> ${message.content}
                </div>`;
        }

        else {

            chatBox.innerHTML +=
                `<div class="bot">
                    <b>Bot:</b> ${message.content}
                </div>`;
        }

    });

    chatBox.scrollTop =
        chatBox.scrollHeight;
}

document
    .getElementById("message-input")
    .addEventListener("keypress", function(event) {

        if (event.key === "Enter") {
            sendMessage();
        }

    });

    