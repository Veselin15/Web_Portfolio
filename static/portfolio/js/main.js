/* static/portfolio/js/main.js */
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    const icon = document.getElementById('menu-icon');
    const body = document.body;

    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
        menu.classList.add('flex');

        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
        icon.classList.add('rotate-90');

        body.style.overflow = 'hidden';
    } else {
        menu.classList.add('hidden');
        menu.classList.remove('flex');

        icon.classList.remove('fa-times');
        icon.classList.remove('rotate-90');
        icon.classList.add('fa-bars');

        body.style.overflow = 'auto';
    }
}
// document.addEventListener('DOMContentLoaded', function () {
//
//     // 1. Initialize AOS (Animate On Scroll)
//     if (typeof AOS !== 'undefined') {
//         AOS.init({
//             duration: 800,
//             once: true,
//         });
//     }
//
//     // 2. Initialize Typed.js (Само ако елементът съществува на страницата)
//     const typedElement = document.getElementById('typed-text');
//     if (typedElement && typeof Typed !== 'undefined') {
//         new Typed('#typed-text', {
//             strings: ['Python Developer', 'Django Specialist', 'Hardware Enthusiast'],
//             typeSpeed: 50,
//             backSpeed: 30,
//             loop: true
//         });
//     }
//
//     // 3. Mobile Menu Logic
//     const menuBtn = document.querySelector('button[onclick="toggleMobileMenu()"]');
//     const mobileMenu = document.getElementById('mobile-menu');
//     const iconClosed = document.getElementById('menu-icon-closed');
//     const iconOpen = document.getElementById('menu-icon-open');
//     const mobileLinks = mobileMenu ? mobileMenu.querySelectorAll('a') : [];
//
//     // Функция за превключване
//     window.toggleMobileMenu = function() {
//         if (mobileMenu.classList.contains('hidden')) {
//             mobileMenu.classList.remove('hidden');
//             iconClosed.classList.add('hidden');
//             iconOpen.classList.remove('hidden');
//         } else {
//             mobileMenu.classList.add('hidden');
//             iconClosed.classList.remove('hidden');
//             iconOpen.classList.add('hidden');
//         }
//     };
//
//     // Затваряне на менюто при клик на линк (UX подобрение)
//     mobileLinks.forEach(link => {
//         link.addEventListener('click', () => {
//             if (!mobileMenu.classList.contains('hidden')) {
//                 toggleMobileMenu();
//             }
//         });
//     });
//
//     // Затваряне при resize (ако минем на десктоп)
//     window.addEventListener('resize', () => {
//         if (window.innerWidth >= 768 && mobileMenu) {
//             mobileMenu.classList.add('hidden');
//             iconClosed.classList.remove('hidden');
//             iconOpen.classList.add('hidden');
//         }
//     });
// });