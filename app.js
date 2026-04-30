const chatBox = document.getElementById("chat");
const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const imageBtn = document.getElementById("imageBtn");

// Send text message to Groq
sendBtn.onclick = async () => {
    const message = input.value.trim();
    if (!message) return;

    input.value = "";
    addMessage("You", message);

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    addMessage("Lexor", data.reply);
};

// Generate image using Fal.ai
imageBtn.onclick = async () => {
    const prompt = input.value.trim();
    if (!prompt) return;

    input.value = "";
    addMessage("You (Image Prompt)", prompt);

    const response = await fetch("/generate-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
    });

    const data = await response.json();

    const img = document.createElement("img");
    img.src = data.image_url;
    img.className = "generated-image";

    chatBox.appendChild(img);
};

// Add message to chat window
function addMessage(sender, text) {
    const div = document.createElement("div");
    div.className = "message";
    div.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}