document.addEventListener("DOMContentLoaded", function() {
    const subheading = document.querySelector(".livability-subheading");
    const button = document.querySelector(".shadow-btn");
    const startPage = document.querySelector(".start-page");
    const personalizationPage = document.querySelector(".personalization-page");

    // Animation Timing Settings
    const subheadingDelay = 1000;
    const buttonAppearDelay = 3000;
    const fadeOutDuration = 2500;

    // Animate the subheading to fade in
    setTimeout(() => {
        subheading.style.opacity = '1';
        subheading.style.transform = 'translateY(0)';
    }, subheadingDelay);

    // Animate the button to fade in
    setTimeout(() => {
        button.style.opacity = '1';
        button.style.transform = 'translateY(0)';
    }, buttonAppearDelay);

    // Button handlers
    button.addEventListener("mousedown", function() {
        button.classList.add("shadow-btn-clicked");
    });

    button.addEventListener("mouseup", function() {
        button.classList.remove("shadow-btn-clicked");
    });

    button.addEventListener("mouseleave", function() {
        button.classList.remove("shadow-btn-clicked");
    });

    // Fade out the start page when button is clicked
    button.addEventListener("click", function() {
        startPage.style.opacity = '0';
        setTimeout(() => {
            startPage.style.display = 'none';
            
            personalizationPage.classList.add("visible");
        }, fadeOutDuration);
    });
});
