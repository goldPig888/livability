document.addEventListener("DOMContentLoaded", function () {
    const subheading = document.querySelector(".livability-subheading");
    const button = document.querySelector(".shadow-btn");
    const startPage = document.querySelector(".start-page");
    const personalizationPage = document.querySelector(".personalization-page");
    const logoContainer = document.querySelector(".logo-container");
    const searchInput = document.querySelector('.search__input');

    const locationInfoButton = document.querySelector(".option-btn:nth-child(1)");
    const environmentalStanceButton = document.querySelector(".option-btn:nth-child(2)");
    const airQualityButton = document.querySelector(".option-btn:nth-child(3)");
    const carbonIntensityButton = document.querySelector(".option-btn:nth-child(4)");
    const temperatureButton = document.querySelector(".option-btn:nth-child(5)");
    const windButton = document.querySelector(".option-btn:nth-child(6)");

    const locationInformationDiv = document.querySelector(".location-information");
    const environmentalStanceDiv = document.querySelector(".environmental-stance");
    const airQualityDiv = document.querySelector(".air-quality-index");
    const carbonIntensityDiv = document.querySelector(".carbon-intensity");
    const temperatureDiv = document.querySelector(".temperature");
    const windDiv = document.querySelector(".wind");

    let map;
    let currentActiveScreen = locationInformationDiv; 

    // Initialize page based on stored state
    setupInitialPageState();

    // Set up interactions
    setupButtonInteractions();
    setupLogoInteraction();
    setupOptionInteractions();

    window.initMap = function () {
        map = new google.maps.Map(document.getElementById("map"), {
            center: { lat: -34.397, lng: 150.644 },
            zoom: 8,
        });

        const searchBox = new google.maps.places.SearchBox(searchInput);

        map.addListener("bounds_changed", () => {
            searchBox.setBounds(map.getBounds());
        });

        searchBox.addListener("places_changed", () => {
            const places = searchBox.getPlaces();
            if (places.length == 0) return;

            const bounds = new google.maps.LatLngBounds();
            places.forEach((place) => {
                if (!place.geometry) return;
                if (place.geometry.viewport) {
                    bounds.union(place.geometry.viewport);
                } else {
                    bounds.extend(place.geometry.location);
                }
            });
            map.fitBounds(bounds);
        });
    }

    function setupInitialPageState() {
        const currentPage = localStorage.getItem('currentPage');
        if (currentPage === 'personalizationPage') {
            showPersonalizationPage(false);
            hideAllContentDivs();
            currentActiveScreen.style.display = 'flex';
        } else {
            displayStartPage();
        }
    }

    function setupButtonInteractions() {
        button.addEventListener("click", function () {
            fadeOutStartPage();
        });

        button.addEventListener("mousedown", function () {
            button.classList.add("shadow-btn-clicked");
        });

        button.addEventListener("mouseup", function () {
            button.classList.remove("shadow-btn-clicked");
        });

        button.addEventListener("mouseleave", function () {
            button.classList.remove("shadow-btn-clicked");
        });
    }

    function setupLogoInteraction() {
        logoContainer.addEventListener('click', function () {
            localStorage.removeItem('currentPage');
            displayStartPage();
        });
    }

    function setupOptionInteractions() {
        const optionButtons = document.querySelectorAll('.option-btn');

        optionButtons.forEach(button => {
            button.addEventListener('click', function () {
                optionButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');

                const contentId = this.textContent.toLowerCase().replace(/\s+/g, '-');
                const newActiveScreen = document.querySelector(`.${contentId}`);

                if (newActiveScreen && currentActiveScreen !== newActiveScreen) {
                    currentActiveScreen.style.display = 'none';
                    newActiveScreen.style.display = 'flex';
                    currentActiveScreen = newActiveScreen;
                }

                if (this === locationInfoButton) {
                    if (!map) {
                        initMap();
                    } else {
                        google.maps.event.trigger(map, 'resize');
                    }
                }
            });
        });

        // Select location info by default
        locationInfoButton.click();
    }

    function hideAllContentDivs() {
        locationInformationDiv.style.display = 'none';
        environmentalStanceDiv.style.display = 'none';
        airQualityDiv.style.display = 'none';
        carbonIntensityDiv.style.display = 'none';
        temperatureDiv.style.display = 'none';
        windDiv.style.display = 'none';
    }

    function displayStartPage() {
        personalizationPage.style.display = 'none';
        personalizationPage.classList.remove("visible");
        startPage.style.display = 'flex';
        startPage.style.opacity = '0';

        resetAnimations();

        setTimeout(() => {
            startPage.style.opacity = '1';
        }, 10);
    }

    function fadeOutStartPage() {
        startPage.style.opacity = '0';
        setTimeout(() => {
            startPage.style.display = 'none';
            showPersonalizationPage(true);
        }, 2500);
    }

    function showPersonalizationPage(saveState) {
        personalizationPage.style.display = 'flex';
        personalizationPage.style.opacity = '0';
        setTimeout(() => {
            personalizationPage.style.opacity = '1';
            personalizationPage.classList.add("visible");
            if (saveState) {
                localStorage.setItem('currentPage', 'personalizationPage');
            }
        }, 10);
        locationInfoButton.click();
    }

    function resetAnimations() {
        subheading.style.opacity = '0';
        subheading.style.transform = 'translateY(20px)';
        button.style.opacity = '0';
        button.style.transform = 'translateY(20px)';
        void subheading.offsetWidth;
        void button.offsetWidth;
        setTimeout(() => {
            subheading.style.opacity = '1';
            subheading.style.transform = 'translateY(0)';
            button.style.opacity = '1';
            button.style.transform = 'translateY(0)';
        }, 1000);
    }
    document.querySelectorAll('.temp-radio-input').forEach(input => {
        input.addEventListener('change', function () {
            if (this.checked) {
                updateLabelColors();
            }
        });
    });

    function updateLabelColors() {
        document.querySelectorAll('.temp-radio-input').forEach(input => {
            const label = document.getElementById('label-' + input.value);
            if (input.checked) {
                switch (input.value) {
                    case 'freezing':
                        label.style.color = 'hsl(217, 71%, 63%)'; // Lighter blue
                        break;
                    case 'very-cold':
                        label.style.color = 'hsl(203, 89%, 67%)'; // Cyan-blue
                        break;
                    case 'cold':
                        label.style.color = 'hsl(197, 71%, 73%)'; // Sky blue
                        break;
                    case 'cool':
                        label.style.color = 'hsl(174, 59%, 59%)'; // Soft teal
                        break;
                    case 'mild':
                        label.style.color = 'hsl(54, 100%, 62%)'; // Lemon yellow
                        break;
                    case 'pleasant':
                        label.style.color = 'hsl(34, 100%, 57%)'; // Orange
                        break;
                    case 'warm':
                        label.style.color = 'hsl(14, 100%, 67%)'; // Light red
                        break;
                    case 'hot':
                        label.style.color = 'hsl(6, 90%, 57%)'; // Darker orange
                        break;
                    case 'very-hot':
                        label.style.color = 'hsl(348, 83%, 57%)'; // Rich red
                        break;
                    case 'extreme-heat':
                        label.style.color = 'hsl(284, 57%, 80%)'; // Lighter purple
                        break;
                }
            } else {
                label.style.color = 'hsl(0, 0%, 60%)'; // Default grey
            }
        });
    }

});
