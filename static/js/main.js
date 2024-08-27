let correctCount = localStorage.getItem('correctCount') ? parseInt(localStorage.getItem('correctCount')) : 0;

function correctC() {
    if (correctCount < 5) {
        correctCount++;
        localStorage.setItem('correctCount', correctCount); // localStorage에 저장
    }
    return correctCount;
}

// 프로필 사진 선택
document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    const selectedImageInput = document.getElementById('selected-image');
    
    let currentIndex = 0;

    function showSlide(index) {
        const totalSlides = slides.length;
        if (index >= totalSlides) {
            currentIndex = 0;
        } else if (index < 0) {
            currentIndex = totalSlides - 1;
        } else {
            currentIndex = index;
        }
        const offset = -100 * currentIndex;
        document.querySelector('.slides').style.transform = `translateX(${offset}%)`;
        selectedImageInput.value = slides[currentIndex].dataset.image;
    }

    prevButton.addEventListener('click', function() {
        showSlide(currentIndex - 1);
    });

    nextButton.addEventListener('click', function() {
        showSlide(currentIndex + 1);
    });

    showSlide(currentIndex);
});

// 랜덤 매칭
$(document).ready(function() {
    function updateMatchStatus() {
        $.ajax({
            url: '/fetch_matching_status',
            method: 'GET',
            success: function(response) {
                $('#match-status').html(response.message);

                let buttonContainer = $('#match-buttons');
                buttonContainer.empty();

                if (response.matching) {
                    buttonContainer.html('<button id="completed-button">매칭 완료</button>');
                    $('#match-status').append('<button id="chat-button">채팅방으로 이동하기</button>');
                    
                    $('#chat-button').on('click', function() {
                        window.location.href = '/chatroom';
                    });
                } else if (response.requested && !response.matching) {
                    buttonContainer.html('<button id="cancel-button">매칭 취소하기</button>');
                    $('#cancel-button').on('click', function() {
                        $.ajax({
                            url: '/cancel_match',
                            method: 'POST',
                            success: function(response) {
                                $('#match-status').html(response.message);
                                updateMatchStatus();
                            },
                            error: function(error) {
                                $('#match-status').html(error.responseJSON.message || '알 수 없는 오류가 발생했습니다.');
                            }
                        });
                    });
                } else if (!response.requested) {
                    buttonContainer.html('<button id="match-button">매칭하기</button>');
                    $('#match-button').on('click', function() {
                        $('#match-buttons').html('<button id="cancel-button">매칭 취소하기</button>');
                        
                        $('#cancel-button').on('click', function() {
                            $.ajax({
                                url: '/cancel_match',
                                method: 'POST',
                                success: function(response) {
                                    $('#match-status').html(response.message);
                                    updateMatchStatus(); 
                                },
                                error: function(error) {
                                    $('#match-status').html(error.responseJSON.message || '알 수 없는 오류가 발생했습니다.');
                                }
                            });
                        });

                        $.ajax({
                            url: '/match_teams',
                            method: 'POST',
                            success: function(response) {
                                let message = '';
                                if (response.current_team_result) {
                                    message += response.current_team_result;
                                }
                                $('#match-status').html(message);
                                updateMatchStatus();
                            },
                            error: function(error) {
                                $('#match-status').html(error.responseJSON.message || '알 수 없는 오류가 발생했습니다.');
                                updateMatchStatus();
                            }
                        });
                    });
                }
            },
            error: function(error) {
                $('#match-status').html('팀 등록하기 버튼을 눌러 팀을 등록하세요.');
            }
        });
    }

    updateMatchStatus();
});