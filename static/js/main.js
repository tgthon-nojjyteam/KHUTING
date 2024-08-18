let correctCount = localStorage.getItem('correctCount') ? parseInt(localStorage.getItem('correctCount')) : 0;

function correctC() {
    if (correctCount < 5) {
        correctCount++;
        localStorage.setItem('correctCount', correctCount); // 증가한 값을 localStorage에 저장
    }
    return correctCount;
}

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

