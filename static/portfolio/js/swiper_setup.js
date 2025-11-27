document.addEventListener('DOMContentLoaded', function () {
        var swiper = new Swiper(".certificate-swiper", {
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
    });