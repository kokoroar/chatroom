var connection = new WebSocket("ws://" + location.host + "/backend");
var chatWindow = document.getElementById("chat_window");
var chatForm = document.getElementById("chat_form");
var messageInput = document.getElementById("message");
var messages = new Array();

function formSubmit() {
    connection.send(messageInput.value);
    messageInput.value = "";
    console.log(messageInput.value);
    return false;
}

function connectionOnMessage(e) {
    console.log(e.data);
    messages[messages.length] = JSON.parse(e.data);
    writeMessagesOnWindow()
}

function writeMessagesOnWindow() {
    chatWindow.innerHTML = "";
    for (var i = 0; i < messages.length; i++) {
        addMessagesOnWindow(messages[i]);
    }
}

function addMessagesOnWindow(message) {
    var newMessage = document.createElement("p");
    newMessage.textContent = message["from"] + ": " + message["message"];
    chatWindow.appendChild(newMessage);
}

chatForm.onsubmit = formSubmit;
connection.onmessage = connectionOnMessage;