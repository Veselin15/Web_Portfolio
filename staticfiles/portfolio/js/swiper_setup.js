document.addEventListener('DOMContentLoaded', function () {

    // 1. Certificates Slider
    var certSwiper = new Swiper(".certificate-swiper", {
        effect: "coverflow",
        centeredSlides: true,
        slidesPerView: "auto",
        initialSlide: 1,
        // DISABLE DRAGGING
        allowTouchMove: false,
        grabCursor: false,

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
        // ENABLE ARROWS
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        autoplay: {
            delay: 2500,
            disableOnInteraction: false,
        },
    });

    // 2. Projects Sliders (Initialize each separately to map arrows correctly)
    document.querySelectorAll('.project-swiper').forEach(function(swiperElement) {
        new Swiper(swiperElement, {
            slidesPerView: 1,
            spaceBetween: 30,
            // DISABLE DRAGGING
            allowTouchMove: false,
            grabCursor: false,

            pagination: {
                el: swiperElement.querySelector(".swiper-pagination"),
                clickable: true,
            },
            // ENABLE ARROWS (Scoped to this specific slider)
            navigation: {
                nextEl: swiperElement.querySelector(".swiper-button-next"),
                prevEl: swiperElement.querySelector(".swiper-button-prev"),
            },
            breakpoints: {
                768: {
                    slidesPerView: 2,
                },
                1024: {
                    slidesPerView: 3,
                },
            },
        });
    });
});