let correctCount = localStorage.getItem('correctCount') ? parseInt(localStorage.getItem('correctCount')) : 0;

function correctC() {
    if (correctCount < 5) {
        correctCount++;
        localStorage.setItem('correctCount', correctCount); // 증가한 값을 localStorage에 저장
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
        selectedImageInput.value = slides[currentIndex].dataset.image; // 현재 슬라이드의 이미지 URL을 숨겨진 입력 필드에 저장
    }

    prevButton.addEventListener('click', function() {
        showSlide(currentIndex - 1);
    });

    nextButton.addEventListener('click', function() {
        showSlide(currentIndex + 1);
    });

    showSlide(currentIndex); // 초기 슬라이드 표시
});

// 랜덤 매칭
$(document).ready(function() {
    // 페이지 로드 시 매칭 상태를 가져옵니다.
    $.ajax({
        url: '/fetch_matching_status',
        method: 'GET',
        success: function(response) {
            // 서버에서 받은 메시지에 따라 적절한 문구를 표시
            $('#match-status').text(response.message);
        },
        error: function(error) {
            $('#match-status').text('매칭 상태를 가져오는 데 실패했습니다.');
        }
    });

    $('#match-button').on('click', function() {
        $.ajax({
            url: '/match_teams',
            method: 'POST',
            success: function(response) {
                // 서버 응답에 따라 결과를 페이지에 표시
                let message = '';
                if (response.current_team_result) {
                    message += response.current_team_result;
                }
                $('#match-status').html(message);
            },
            error: function(error) {
                // 에러 메시지를 페이지에 표시
                $('#match-status').text((error.responseJSON.message || '알 수 없는 오류가 발생했습니다.'));
            }
        });
    });
});

