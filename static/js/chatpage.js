const urlParams = new URLSearchParams(window.location.search);

/* Get github code that will be used as client id   */
let client_id = urlParams.get('code');
document.querySelector("#ws-id").textContent = client_id;
let ws = new WebSocket(`ws://${window.location.host}/ws/${client_id}`);
let messages = document.getElementById("messages");

/* Handle when creating, editing or deleting a message */
ws.onmessage = function (event) {

    let eventDataSplit = event.data.split(":");
    let eventType = eventDataSplit[0];
    let index = parseInt(eventDataSplit[1]);
    let content = eventDataSplit[1]
    let user_name = eventDataSplit[2]
  
    /* Deleting */
    if (eventType.startsWith("Message deleted")) {
        // Message deleted
       
        let deletedMessage = messages.children[index];
        if (deletedMessage) {
            deletedMessage.remove();
        }

     /* Updating */
    } else if (eventType.startsWith("Updated message")) {
        // Message updated
        let updatedMessage = messages.children[index];
        let isCurrentUserMessage = updatedMessage.classList.contains("current-user-message");

        content = eventDataSplit[2]
        user_name = eventDataSplit[3]
        if (isCurrentUserMessage) {
            updatedMessage.textContent = `${user_name}(you): ${content}`;
            addDelAndEditButtons(messages, updatedMessage, content, user_name)
        } else {
            updatedMessage.textContent = `${user_name} ${content}`
        }
    } else {
       /*  New message */
        let message = document.createElement("li");
        let isCurrentUserMessage = event.data.startsWith(client_id);
        let messageContent = document.createElement("span");
        if (isCurrentUserMessage) {
            message.classList.add("current-user-message");
            messageContent.textContent =`${user_name}(you): ${content}`;
        } else {
            messageContent.textContent =`${user_name}: ${content}`;
        }

        
      

        message.appendChild(messageContent);

        if (isCurrentUserMessage) {
           addDelAndEditButtons(messages, message, content, user_name)
        }

        messages.appendChild(message);
    }
};
function sendMessage(event, user_name) {
    event.preventDefault();
    let input = document.getElementById("messageText");
    let message = input.value;

    let prefixedMessage = `${client_id}: ${message}:${user_name}`;
    ws.send("create:" + prefixedMessage);
    input.value = "";
    
}

// Function to update a message
function updateMessage(index, message, user_name) {
    let prefixedMessage = `${client_id}:${message}:${user_name}`;
    ws.send(`update:${index}:${prefixedMessage}`);
}

// Function to delete a message
function deleteMessage(index) {
    ws.send(`delete:${index}`);
}


// Handle form submission
function addDelAndEditButtons(messages, message, content, user_name){
       let editButton = document.createElement("button");
       editButton.textContent = "Edit";
       editButton.addEventListener("click", function () {
           let index = Array.from(messages.children).indexOf(message);
           let newMessage = prompt("Update message:", content);
           if (newMessage !== null) {
               updateMessage(index, newMessage, user_name);
           }
       });

       let deleteButton = document.createElement("button");
       deleteButton.textContent = "Delete";
       deleteButton.addEventListener("click", function () {
           let index = Array.from(messages.children).indexOf(message);
           deleteMessage(index);
       });

       message.appendChild(editButton);
       message.appendChild(deleteButton);

}
