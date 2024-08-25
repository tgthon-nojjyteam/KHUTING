// Set to store the IDs of recent messages to avoid duplicates
let lastMessageIds = new Set();

// Initialize chat by fetching user and chatroom info, then set up polling and sending
function initializeChat() {
    fetch('/get_user_info')
        .then(response => response.json())
        .then(data => {
            const { user_name: userName, chat_room: chatRoom } = data;

            // Start polling for messages and set up message sending
            pollMessages(userName, chatRoom);
            setupSendMessage(userName, chatRoom);
        })
        .catch(error => {
            console.error('Error fetching user info:', error);
        });
}

// Poll messages from the server periodically
function pollMessages(userName, chatRoom) {
    fetch(`/receive_message/${chatRoom}`)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                data.forEach(msg => {
                    if (!lastMessageIds.has(msg.id)) { // Check for duplicate messages
                        lastMessageIds.add(msg.id); // Store message ID to avoid duplication
                        displayMessage(msg.user, msg.message, userName === msg.user);
                    }
                });
            } else {
                console.error('Unexpected data format:', data);
            }
            setTimeout(() => pollMessages(userName, chatRoom), 1000); // Poll every second
        })
        .catch(error => {
            console.error('Error receiving message:', error);
            setTimeout(() => pollMessages(userName, chatRoom), 5000); // Retry after 5 seconds if an error occurs
        });
}


// Set up message sending functionality
function setupSendMessage(userName, chatRoom) {
    const sendButton = document.getElementById('send-button');
    sendButton.addEventListener('click', () => {
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value.trim();

        if (message) {
            sendMessage(userName, chatRoom, message);
            messageInput.value = ''; // Clear input field after sending
        } else {
            alert('Please enter a message.');
        }
    });
}

// Send message to the server
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

// Display message in the chat window
function displayMessage(userName, message, isUserMessage) {
    const messagesDiv = document.getElementById('messages');
    if (messagesDiv) {
        const newMessage = document.createElement('div');
        newMessage.textContent = `${userName}: ${message}`;
        newMessage.className = `message ${isUserMessage ? 'user' : 'other'}`;
        messagesDiv.appendChild(newMessage);
        messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to the latest message
    } else {
        console.error('Messages div not found');
    }
}

// Fetch and display matching status on page load
function fetchMatchingStatus() {
    fetch('/fetch_matching_status')
        .then(response => response.json())
        .then(data => {
            const matchedDepartmentElement = document.getElementById('matched-department');
            if (matchedDepartmentElement) {
                matchedDepartmentElement.innerHTML = data.chat_message; // Keep HTML tags intact
            }
        })
        .catch(error => {
            console.error('Error fetching matching status:', error);
        });
}

// Set up event listeners for the menu and overlay
function setupMenuToggle() {
    const menuButton = document.getElementById('menu-button');
    const sideMenu = document.getElementById('side-menu');
    const closeMenu = document.getElementById('close-menu');
    const overlay = document.getElementById('overlay');

    // Open the menu and overlay when menu button is clicked
    menuButton.addEventListener('click', () => {
        sideMenu.classList.add('open');
        overlay.style.display = 'block';
    });

    // Close the menu and overlay when close button or overlay is clicked
    [closeMenu, overlay].forEach(element => {
        element.addEventListener('click', () => {
            sideMenu.classList.remove('open');
            overlay.style.display = 'none';
        });
    });
}

// Initialize everything on window load
window.onload = function() {
    initializeChat();      // Initialize chat functionality
    fetchMatchingStatus(); // Fetch matching status for the department
    setupMenuToggle();     // Set up menu toggle functionality
};





// 메뉴창
document.addEventListener('DOMContentLoaded', function() {
    var menuButton = document.getElementById('menu-button');
    var sideMenu = document.getElementById('side-menu');
    var closeMenu = document.getElementById('close-menu');
    var overlay = document.getElementById('overlay');

    // 메뉴 버튼 클릭 시 메뉴와 오버레이 열기
    menuButton.addEventListener('click', function() {
        sideMenu.classList.add('open');
        overlay.style.display = 'block';
    });

    // 닫기 버튼 클릭 시 메뉴와 오버레이 닫기
    closeMenu.addEventListener('click', function() {
        sideMenu.classList.remove('open');
        overlay.style.display = 'none';
    });

    // 오버레이 클릭 시 메뉴와 오버레이 닫기
    overlay.addEventListener('click', function() {
        sideMenu.classList.remove('open');
        overlay.style.display = 'none';
    });
});

