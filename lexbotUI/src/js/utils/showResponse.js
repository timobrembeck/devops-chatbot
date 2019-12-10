export default function showResponse(lexResponse) {
    const conversationDiv = document.getElementById('conversation');

    const messageData = document.createElement("div");
    messageData.className = "message-data-lex";
    const messageDataName = document.createElement("span");
    messageDataName.className = "message-data-name";
    messageDataName.appendChild(document.createTextNode("Lex Bot"));
    const messageDataTime = document.createElement("span");
    messageDataTime.className = "message-data-time";
    messageDataTime.appendChild(document.createTextNode(new Date().toLocaleTimeString()));
    messageData.appendChild(messageDataName);
    messageData.appendChild(messageDataTime);

    const responseParaText = document.createElement("P");
    responseParaText.className = 'lexResponseText';

    if (lexResponse.message) {
        responseParaText.appendChild(document.createTextNode(lexResponse.message));
        responseParaText.appendChild(document.createElement('br'));
    }
    if (lexResponse.dialogState === 'ReadyForFulfillment') {
        responseParaText.appendChild(document.createTextNode(
            'Ready for fulfillment'));
        // TODO:  show slot values
    } else {
        responseParaText.appendChild(document.createTextNode(
            '(' + lexResponse.dialogState + ')'));
    }

    const responsePara = document.createElement("div");
    responsePara.className = 'lexResponse';
    responsePara.appendChild(messageData);
    responsePara.appendChild(responseParaText);
    conversationDiv.appendChild(responsePara);

    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}