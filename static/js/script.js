document.addEventListener("DOMContentLoaded", function() {
    // Elements selection
    const subheading = document.querySelector(".livability-subheading");
    const button = document.querySelector(".shadow-btn");
    const startPage = document.querySelector(".start-page");
    const personalizationPage = document.querySelector(".personalization-page");
    const logoContainer = document.querySelector(".logo-container");

    // Initialize page based on stored state
    setupInitialPageState();

    // Set up interactions
    setupButtonInteractions();
    setupLogoInteraction();

    // Function to check and set the initial page state from localStorage
    function setupInitialPageState() {
        if (localStorage.getItem('currentPage') === 'personalizationPage') {
            personalizationPage.classList.add("visible");
            personalizationPage.style.display = 'block';
            startPage.style.display = 'none';
        } else {
            displayStartPage();
        }
    }

    // Button interactions for page transitions
    function setupButtonInteractions() {
        button.addEventListener("click", function() {
            fadeOutStartPage();
        });

        // Additional mouse interaction styles for the button
        button.addEventListener("mousedown", function() {
            button.classList.add("shadow-btn-clicked");
        });

        button.addEventListener("mouseup", function() {
            button.classList.remove("shadow-btn-clicked");
        });

        button.addEventListener("mouseleave", function() {
            button.classList.remove("shadow-btn-clicked");
        });
    }

    // Logo click handler to return to the start page
    function setupLogoInteraction() {
        logoContainer.addEventListener('click', function() {
            localStorage.removeItem('currentPage'); // Clear state
            displayStartPage(); // Reset and display the start page
        });
    }

    // Display the start page with reset animations
    function displayStartPage() {
        personalizationPage.style.display = 'none';
        personalizationPage.classList.remove("visible");
        startPage.style.display = 'flex';
        startPage.style.opacity = '0';

        resetAnimations();

        setTimeout(() => {
            startPage.style.opacity = '1';
        }, 10); // Ensure transition effect is visible
    }

    // Fade out the start page and prepare to display the personalization page
    function fadeOutStartPage() {
        startPage.style.opacity = '0';
        setTimeout(() => {
            startPage.style.display = 'none';
            fadeInPersonalizationPage();
        }, 2500); // Match duration to CSS transition time
    }

    // Fade in the personalization page after it's displayed
    function fadeInPersonalizationPage() {
        personalizationPage.style.display = 'block';
        personalizationPage.style.opacity = '0';
        setTimeout(() => {
            personalizationPage.style.opacity = '1';
            personalizationPage.classList.add("visible");
            localStorage.setItem('currentPage', 'personalizationPage');
        }, 10);
    }

    // Reset animations for subheading and button
    function resetAnimations() {
        subheading.style.opacity = '0';
        subheading.style.transform = 'translateY(20px)';
        button.style.opacity = '0';
        button.style.transform = 'translateY(20px)';
        void subheading.offsetWidth; // Force reflow to restart CSS animations
        void button.offsetWidth;
        setTimeout(() => {
            subheading.style.opacity = '1';
            subheading.style.transform = 'translateY(0)';
            button.style.opacity = '1';
            button.style.transform = 'translateY(0)';
        }, 1000); // Delay to reapply styles and re-trigger animations
    }
});
