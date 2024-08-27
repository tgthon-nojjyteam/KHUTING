let lastMessageIds = new Set();

function initializeChat() {
    fetch('/get_user_info')
        .then(response => response.json())
        .then(data => {
            const { user_name: userName, chat_room: chatRoom } = data;

            pollMessages(userName, chatRoom);
            setupSendMessage(userName, chatRoom);
        })
        .catch(error => {
            console.error('Error fetching user info:', error);
        });
}

function pollMessages(userName, chatRoom) {
    fetch(`/receive_message/${chatRoom}`)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                data.forEach(msg => {
                    if (!lastMessageIds.has(msg.id)) { 
                        lastMessageIds.add(msg.id);
                        displayMessage(msg.user, msg.message, userName === msg.user);
                    }
                });
            } else {
                console.error('Unexpected data format:', data);
            }
            setTimeout(() => pollMessages(userName, chatRoom), 1000);
        })
        .catch(error => {
            console.error('Error receiving message:', error);
            setTimeout(() => pollMessages(userName, chatRoom), 5000); 
        });
}


function setupSendMessage(userName, chatRoom) {
    const sendButton = document.getElementById('send-button');
    sendButton.addEventListener('click', () => {
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value.trim();

        if (message) {
            sendMessage(userName, chatRoom, message);
            messageInput.value = '';
        } else {
            alert('Please enter a message.');
        }
    });
}

function sendMessage(userName, chatRoom, message) {
    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ from: userName, room: chatRoom, message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status !== 'Message received') {
            console.error('Message was not received by the server.');
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
}

function displayMessage(userName, message, isUserMessage) {
    const messagesDiv = document.getElementById('messages');
    if (messagesDiv) {
        const newMessage = document.createElement('div');
        newMessage.textContent = `${userName}: ${message}`;
        newMessage.className = `message ${isUserMessage ? 'user' : 'other'}`;
        messagesDiv.appendChild(newMessage);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    } else {
        console.error('Messages div not found');
    }
}

function fetchMatchingStatus() {
    fetch('/fetch_matching_status')
        .then(response => response.json())
        .then(data => {
            const matchedDepartmentElement = document.getElementById('matched-department');
            if (matchedDepartmentElement) {
                matchedDepartmentElement.innerHTML = data.chat_message;
            }
        })
        .catch(error => {
            console.error('Error fetching matching status:', error);
        });
}

function setupMenuToggle() {
    const menuButton = document.getElementById('menu-button');
    const sideMenu = document.getElementById('side-menu');
    const closeMenu = document.getElementById('close-menu');
    const overlay = document.getElementById('overlay');

    menuButton.addEventListener('click', () => {
        sideMenu.classList.add('open');
        overlay.style.display = 'block';
    });

    [closeMenu, overlay].forEach(element => {
        element.addEventListener('click', () => {
            sideMenu.classList.remove('open');
            overlay.style.display = 'none';
        });
    });
}

window.onload = function() {
    initializeChat();      
    fetchMatchingStatus(); 
    setupMenuToggle();    
};





// 메뉴창
document.addEventListener('DOMContentLoaded', function() {
    var menuButton = document.getElementById('menu-button');
    var sideMenu = document.getElementById('side-menu');
    var closeMenu = document.getElementById('close-menu');
    var overlay = document.getElementById('overlay');

    menuButton.addEventListener('click', function() {
        sideMenu.classList.add('open');
        overlay.style.display = 'block';
    });

    closeMenu.addEventListener('click', function() {
        sideMenu.classList.remove('open');
        overlay.style.display = 'none';
    });

    overlay.addEventListener('click', function() {
        sideMenu.classList.remove('open');
        overlay.style.display = 'none';
    });
});

