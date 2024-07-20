document.addEventListener("DOMContentLoaded", function () {
    initializeApp();

    let formData = {};

    const subheading = document.querySelector(".livability-subheading");
    const button = document.querySelector(".shadow-btn");
    const startPage = document.querySelector(".start-page");
    const personalizationPage = document.querySelector(".personalization-page");
    const screen = document.querySelector(".screen");
    const resultsPage = document.querySelector(".results-page");
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

    const slider = document.getElementById("myRange");
    const currentValue = document.getElementById("currentValue");
    const categoryDescription = document.getElementById("categoryDescription");

    const stars = document.querySelectorAll('input[name="rate"]');
    const infoBox = document.getElementById('aqiInfo');
    infoBox.style.display = 'none';
    const submitButton = document.querySelector(".submit-btn");

    let map;
    let currentActiveScreen = null;

    hideAllContentDivs();
    setupInitialPageState();
    setupButtonInteractions();
    setupLogoInteraction();
    setupOptionInteractions();

    window.initMap = function () {
        map = new google.maps.Map(document.getElementById("map"), {
            center: { lat: -34.397, lng: 150.644 },
            zoom: 8,
        });

        const searchBox = new google.maps.places.SearchBox(searchInput);
        searchBox.addListener("places_changed", () => handlePlacesChanged(searchBox));
        map.addListener("bounds_changed", () => {
            searchBox.setBounds(map.getBounds());
        });
    }

    function handlePlacesChanged(searchBox) {
        const places = searchBox.getPlaces();
        if (places.length === 0) return;
        const bounds = new google.maps.LatLngBounds();
        places.forEach(place => {
            if (!place.geometry) return;
            if (place.geometry.viewport) {
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
        formData['Location'] = places.map(place => place.name).join(', ');
    }

    function initializeApp() {
        clearCookies();
        clearLocalStorageAndSessionStorage(); // Clear all local storage and session storage
        if (!sessionStorage.getItem('initialized')) {
            sessionStorage.setItem('initialized', 'true');
        }
    }

    function clearCookies() {
        document.cookie.split(";").forEach(cookie => {
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            document.cookie = name + `=;expires=${new Date(0).toUTCString()};path=/`;
        });
    }

    function clearLocalStorageAndSessionStorage() {
        localStorage.clear();
        sessionStorage.clear();
    }

    function setupInitialPageState() {
        const currentPage = localStorage.getItem('currentPage');
        if (currentPage === 'personalizationPage') {
            showPersonalizationPage(false);
            hideAllContentDivs();
            currentActiveScreen = locationInformationDiv;
            currentActiveScreen.style.display = 'flex';
        } else if (currentPage === 'resultsPage') {
            showResultsPage(false);
        } else {
            displayStartPage();
        }
    }

    function setupButtonInteractions() {
        submitButton.addEventListener("click", function () {
            const missingFields = validateInputs();
            if (missingFields.length > 0) {
                Toastify({
                    text: "Please fill in the following fields before submitting:\n " + missingFields.join(", "),
                    duration: 3000,
                    close: true,
                    gravity: "top",
                    position: "right",
                    style: {
                        background: "linear-gradient(to right, #472be7, #288128)",
                    }
                }).showToast();
            } else {
                sendPreferencesToFlask();
            }
        });

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
                    if (currentActiveScreen) {
                        currentActiveScreen.style.display = 'none';
                    }
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
                updateFormData();
            });
        });
        locationInfoButton.click();
    }

    function updateFormData() {
        formData['Search Input'] = searchInput.value.trim();
        document.querySelectorAll('.environmental-stance input[type="radio"]').forEach(radio => {
            if (radio.checked) {
                formData['Environmental Stance'] = radio.nextElementSibling.textContent.trim();
            }
        });
    
        document.querySelectorAll('.temperature .temp-radio-input').forEach(radio => {
            if (radio.checked) {
                let label = document.querySelector(`#label-${radio.value}`);
                formData['Heat Index Temperature'] = extractMedianTemperature(label.textContent);
            }
        });
    
        document.querySelectorAll('.wind .wind-radio-input').forEach(radio => {
            if (radio.checked) {
                let label = document.querySelector(`#label-${radio.value}`);
                formData['Wind Speed Tolerance'] = extractMedian(label.textContent);
            }
        });
    
        formData['Carbon Intensity'] = slider.value;
        stars.forEach(star => {
            if (star.checked) {
                formData['Air Quality'] = star.value;
                updateAqiInfo(star.value);
            }
        });
        console.log('Form Data:', formData);
    }
    
    function extractMedianTemperature(text) {
        let numbers = text.match(/\d+/g).map(Number);
        let medianIndex = Math.floor(numbers.length / 2);
        return numbers[medianIndex - 1];
    }
    
    function extractMedian(text) {
        let numbers = text.match(/\d+/g).map(Number);
        if (numbers.length === 1) {
            return numbers[0];
        }
        let medianIndex = Math.floor(numbers.length / 2);
        return numbers[medianIndex];
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

    function fadeOutScreen() {
        screen.style.opacity = '0';
        setTimeout(() => {
            screen.style.display = 'none';
            showResultsPage(true);
        }, 2500);
    }

    function sendPreferencesToFlask() {
        fetch('/preferences', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fadeOutScreen();
            } else {
                Toastify({
                    text: "Failed to submit preferences. Please try again.",
                    duration: 3000,
                    close: true,
                    gravity: "top",
                    position: "right",
                    style: {
                        background: "linear-gradient(to right, #e74c3c, #e74c3c)",
                    }
                }).showToast();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Toastify({
                text: "An error occurred. Please try again.",
                duration: 3000,
                close: true,
                gravity: "top",
                position: "right",
                style: {
                    background: "linear-gradient(to right, #e74c3c, #e74c3c)",
                }
            }).showToast();
        });
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

    function showResultsPage(saveState) {
        resultsPage.style.display = 'flex';
        resultsPage.style.opacity = '0';
        setTimeout(() => {
            resultsPage.style.opacity = '1';
            if (saveState) {
                localStorage.setItem('currentPage', 'resultsPage');
            }
        }, 10);

        const messages = [
            "Analyzing Environmental Stance...",
            "Evaluating city's environmental policies...",
            "Comparing sustainability measures...",
            "Assessing average temperature...",
            "Checking climate conditions...",
            "Matching temperature with your preferences...",
            "Measuring wind speed...",
            "Evaluating breeziness...",
            "Checking wind conditions...",
            "Calculating air quality index...",
            "Assessing air purity...",
            "Evaluating pollution levels...",
            "Analyzing carbon footprint...",
            "Evaluating carbon intensity...",
            "Checking emission levels..."
        ];

        rotateMessages(messages, "loadingMessage", 2000); // Change message every 2 seconds
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

    slider.oninput = function () {
        currentValue.textContent = `Current Value: ${this.value}`;
        updateCategoryDescription(this.value);
        updateFormData();
    }

    function updateCategoryDescription(value) {
        let description = "";
        const numValue = parseInt(value);
        if (numValue <= 100) {
            description = "Low - Ideal for renewables like wind and solar";
        } else if (numValue <= 300) {
            description = "Moderate - Common for efficient natural gas";
        } else if (numValue <= 500) {
            description = "High - Typical for older fossil fuel plants";
        } else {
            description = "Very High - Associated with coal power plants";
        }
        categoryDescription.textContent = description;
    }

    stars.forEach(star => {
        star.addEventListener('change', function () {
            updateAqiInfo(this.value);
            updateFormData();
            infoBox.style.display = 'block';
        });
    });

    function updateAqiInfo(value) {
        let aqiInfo = "";
        let aqiUpperBound = 0;
        switch (value) {
            case '1':
                aqiInfo = "Hazardous (301-500)";
                aqiUpperBound = 500;
                break;
            case '2':
                aqiInfo = "Very Unhealthy (201-300)";
                aqiUpperBound = 300;
                break;
            case '3':
                aqiInfo = "Unhealthy (151-200)";
                aqiUpperBound = 200;
                break;
            case '4':
                aqiInfo = "Unhealthy for Sensitive Groups (101-150)";
                aqiUpperBound = 150;
                break;
            case '5':
                aqiInfo = "Moderate (51-100)";
                aqiUpperBound = 100;
                break;
        }
        formData['AQI'] = aqiUpperBound;
        infoBox.textContent = aqiInfo;
    }

    function updateLabelColorsTemp() {
        document.querySelectorAll('.temp-radio-input').forEach(input => {
            const label = document.getElementById('label-' + input.value);
            if (input.checked) {
                switch (input.value) {
                    case 'comfortable':
                        label.style.color = 'hsl(120, 100%, 40%)';
                        break;
                    case 'caution':
                        label.style.color = 'hsl(60, 100%, 50%)';
                        break;
                    case 'extreme-caution':
                        label.style.color = 'hsl(30, 100%, 50%)';
                        break;
                    case 'danger':
                        label.style.color = 'hsl(0, 100%, 50%)';
                        break;
                    case 'extreme-danger':
                        label.style.color = 'hsl(330, 100%, 40%)';
                        break;
                }
            } else {
                label.style.color = 'hsl(0, 0%, 60%)';
            }
        });
    }

    function updateLabelColorsWind() {
        document.querySelectorAll('.wind-radio-input').forEach(input => {
            const label = document.getElementById('label-' + input.value);
            if (input.checked) {
                switch (input.value) {
                    case 'calm-light-breeze':
                        label.style.color = 'hsl(197, 71%, 88%)';
                        break;
                    case 'gentle-moderate-breeze':
                        label.style.color = 'hsl(197, 71%, 78%)';
                        break;
                    case 'fresh-strong-breeze':
                        label.style.color = 'hsl(197, 71%, 68%)';
                        break;
                    case 'near-gale-gale':
                        label.style.color = 'hsl(207, 90%, 54%)';
                        break;
                    case 'strong-gale-storm':
                        label.style.color = 'hsl(217, 89%, 33%)';
                        break;
                    case 'hurricane':
                        label.style.color = 'hsl(240, 100%, 27%)';
                        break;
                }
            } else {
                label.style.color = 'hsl(0, 0%, 60%)';
            }
        });
    }

    document.querySelectorAll('.temp-radio-input').forEach(input => {
        input.addEventListener('change', function () {
            if (this.checked) {
                updateLabelColorsTemp();
            }
        });
    });

    document.querySelectorAll('.wind-radio-input').forEach(input => {
        input.addEventListener('change', function () {
            if (this.checked) {
                updateLabelColorsWind();
            }
        });
    });
    document.querySelectorAll('.temperature .temp-radio-input').forEach(input => {
        input.addEventListener('change', function () {
            updateFormData();
        });
    });

    document.querySelectorAll('.wind .wind-radio-input').forEach(input => {
        input.addEventListener('change', function () {
            updateFormData();
        });
    });

    function validateInputs() {
        let missingFields = [];
        if (!searchInput.value.trim()) {
            missingFields.push("Search Input");
        }
        if (!document.querySelector('.environmental-stance input[type="radio"]:checked')) {
            missingFields.push("Environmental Stance");
        }
        if (!document.querySelector('input[name="temp-radio"]:checked')) {
            missingFields.push("Temperature Preferences");
        }
        if (!document.querySelector('input[name="wind-radio"]:checked')) {
            missingFields.push("Wind Speed Preferences");
        }
        if (!document.querySelector('input[name="rate"]:checked')) {
            missingFields.push("Air Quality Rating");
        }
        if (!slider.value.trim()) {
            missingFields.push("Carbon Intensity");
        }
        return missingFields;
    }

    function rotateMessages(messages, elementId, interval) {
        let index = 0;
        const element = document.getElementById(elementId);
    
        setInterval(() => {
            element.textContent = messages[index];
            index = (index + 1) % messages.length;
        }, interval);
    }
});
