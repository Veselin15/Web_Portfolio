document.addEventListener('DOMContentLoaded', function () {

    // 1. Certificates Slider (Coverflow Effect)
    var certSwiper = new Swiper(".certificate-swiper", {
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: "auto",
        initialSlide: 1,
        coverflowEffect: {
            rotate: 50,
            stretch: 0,
            depth: 100,
            modifier: 1,
            slideShadows: true,
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        autoplay: {
            delay: 2500,
            disableOnInteraction: false,
        },
    });

    // 2. Projects Slider (Standard Grid Carousel)
    var projectSwiper = new Swiper(".project-swiper", {
        slidesPerView: 1,
        spaceBetween: 30, // Разстояние между картите
        grabCursor: true,
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        breakpoints: {
            // На таблет (>= 768px) -> 2 карти
            768: {
                slidesPerView: 2,
            },
            // На десктоп (>= 1024px) -> 3 карти
            1024: {
                slidesPerView: 3,
            },
        },
    });
});