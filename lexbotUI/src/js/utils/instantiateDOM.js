import pushChat from './pushChat';

export default async function instantiateDOM(lexUserId, lexruntime, height, width) {

    document.getElementById("lexbotapp").style.height = `${height}px`;
    document.getElementById("lexbotapp").style.maxWidth = `${width}px`;

    //Create conversation div and append it to lexbotapp 
    const menu = document.createElement("div");
    menu.id = "menu";
    menu.style.maxWidth = `${width}px`;
    const menuText = document.createElement("h2");
    menuText.appendChild(document.createTextNode("Lex Bot Chat"));
    menu.appendChild(menuText);
    document.getElementById("lexbotapp").appendChild(menu);

    //Create conversation div and append it to lexbotapp 
    const conversation = document.createElement("div");
    conversation.id = "conversation";
    conversation.style.height = `${height-100}px`;
    conversation.style.maxWidth = `${width}px`;
    document.getElementById("lexbotapp").appendChild(conversation);

    //Create chatform form and append it to lexbotapp
    const chatform= document.createElement("form");
    chatform.id = "chatform";
    const chatformInput= document.createElement("input");
    chatformInput.type = "text";
    chatformInput.id = "wisdom";
    chatformInput.placeholder = "Type your message...";
    chatformInput.style.width = `${width}px`;
    chatform.appendChild(chatformInput);
    document.getElementById("lexbotapp").appendChild(chatform);

    // set the focus to the input box
    document.getElementById("wisdom").focus();

    // add event listener to chatform
    document.getElementById("chatform").addEventListener("submit", (e) => {
        e.preventDefault();
        pushChat(lexUserId, lexruntime);
    });

}