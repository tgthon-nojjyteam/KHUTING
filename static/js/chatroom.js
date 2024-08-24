// 페이지 로드 시 사용자 정보와 채팅방 정보를 서버로부터 가져오는 함수
function initializeChat() {
    fetch('/get_user_info')
        .then(response => response.json())
        .then(data => {
            var userName = data.user_name;
            var chatRoom = data.chat_room;

            // 메시지 폴링 및 메시지 전송 함수 호출
            pollMessages(userName, chatRoom);
            setupSendMessage(userName, chatRoom);
        })
        .catch(error => {
            console.error('Error fetching user info:', error);
        });
}

// 메시지 폴링 함수
function pollMessages(userName, chatRoom) {
    fetch(`/receive_message/${chatRoom}`)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                data.forEach(msg => {
                    displayMessage(msg.user, msg.message, userName === msg.user);
                });
            }
            setTimeout(() => pollMessages(userName, chatRoom), 1000); // 1초 후 다시 폴링
        })
        .catch(error => {
            console.error('Error receiving message:', error);
            setTimeout(() => pollMessages(userName, chatRoom), 5000); // 오류 발생 시 5초 후 재시도
        });
}

// 메시지를 화면에 출력하는 함수
function displayMessage(userName, message, isUserMessage) {
    var messagesDiv = document.getElementById('messages');
    if (messagesDiv) {
        var newMessage = document.createElement('div');
        newMessage.textContent = `${userName}: ${message}`;
        newMessage.className = 'message ' + (isUserMessage ? 'user' : 'other');
        messagesDiv.appendChild(newMessage);
        messagesDiv.scrollTop = messagesDiv.scrollHeight; // 최신 메시지가 보이도록 스크롤
    } else {
        console.error('Messages div not found');
    }
}

// 메시지 전송 함수
function setupSendMessage(userName, chatRoom) {
    var sendButton = document.getElementById('send-button');
    sendButton.addEventListener('click', function() {
        var messageInput = document.getElementById('message-input');
        var message = messageInput.value;
        if (message) {
            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ from: userName, room: chatRoom, message: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'Message received') {
                    messageInput.value = ''; // 메시지 전송 후 입력 필드 비우기
                }
            })
            .catch(error => {
                console.error('Error sending message:', error);
            });
        } else {
            alert('메시지를 입력해주세요.');
        }
    });
}

window.onload = function() {
    // 사용자 정보 및 채팅 설정 초기화
    initializeChat();

    // 매칭 상태 가져오기
    fetch('/fetch_matching_status')
        .then(response => response.json())
        .then(data => {
            var matchedDepartmentElement = document.getElementById('matched-department');
            if (matchedDepartmentElement) {
                matchedDepartmentElement.innerHTML = data.chat_message; // HTML 태그 유지
            }
        })
        .catch(error => {
            console.error('Error fetching matching status:', error);
        });
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

