export default function showRequest(text) {
    const conversationDiv = document.getElementById('conversation');

    const messageData = document.createElement("div");
    messageData.className = "message-data-user";
    const messageDataName = document.createElement("span");
    messageDataName.className = "message-data-name";
    messageDataName.appendChild(document.createTextNode("User"));
    const messageDataTime = document.createElement("span");
    messageDataTime.className = "message-data-time";
    messageDataTime.appendChild(document.createTextNode(new Date().toLocaleTimeString()));
    messageData.appendChild(messageDataName);
    messageData.appendChild(messageDataTime);

    const requestParaText = document.createElement("P");
    requestParaText.className = 'userRequestText';
    requestParaText.appendChild(document.createTextNode(text));

    const requestPara = document.createElement("div");
    requestPara.className = 'userRequest';
    requestPara.appendChild(messageData);
    requestPara.appendChild(requestParaText);

    conversationDiv.appendChild(requestPara)
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}