# Livability

## Overview
Climate change is causing significant shifts in weather patterns, leading to extreme heat, rising sea levels, and an increased frequency of natural disasters. As a result, individuals, families, and businesses face challenges in assessing the livability of a location due to uncertainties related to climate conditions.

The **Livability Index** addresses these challenges by providing a comprehensive tool that evaluates environmental metrics, assesses climate-related risks, and offers personalized recommendations based on user preferences. This tool helps people make more informed decisions about where to live, work, or invest, considering both present conditions and future climate projections.

## Specific Issues
1. **Increased Extreme Weather Events:** More frequent and severe weather events, such as hurricanes, floods, and wildfires, directly impact the livability of certain areas.
2. **Rising Temperatures:** Global temperature increases are making certain regions less habitable due to extreme heat, which in turn affects the overall livability.
3. **Sea Level Rise:** Coastal areas are experiencing sea-level rise, posing a threat to communities and affecting the desirability of living in those locations.
4. **Shifts in Rainfall Patterns:** Changing precipitation patterns can lead to either water scarcity or excessive rainfall, impacting agriculture, water resources, and general livability.

## Solution
Provide users with a comprehensive livability index that takes into account climate factors such as temperature, precipitation, sea level, and extreme weather events. This tool will help individuals, families, and businesses make informed decisions about where to live or invest based on current and projected climate conditions.

## Key Features

### 1. Climate Livability Score
The Livability Index calculates a comprehensive climate livability score for each city based on environmental factors like:
* Air Quality Index (AQI)
* Carbon Intensity
* Heat Index
* Wind Speed

The score integrates these factors to provide a holistic assessment of how climate affects the quality of life in a particular region.

**Formula for Livability Score:**
Livability Score = Base Score - ( ∑ Deviation(i) )

*Where:*
- *i* represents each climate-related metric.
- The *Base Score* starts at 100, and deviations from ideal values reduce the score.

### 2. Personalized Recommendations
Users input their preferences for environmental conditions, such as:
* Preferred air quality
* Tolerance for extreme temperatures
* Desired wind speeds and carbon intensity levels

The app compares the user’s preferences against real-world data from various cities and provides personalized recommendations on livability.

### 3. Risk Assessment
Each location is assessed for climate-related risks, such as:
* Floods
* Hurricanes
* Wildfires
* Heatwaves

This provides users with a clearer understanding of the potential challenges they may face in a particular region.

### 4. Future Climate Predictions
The app integrates climate change projections, enabling users to see how a location’s livability might evolve over time. This feature is critical for long-term planning, helping users anticipate how climate conditions will impact their desired location in the coming years.

### 5. Community Engagement
The platform fosters a sense of community by allowing users to share their experiences, tips, and insights about living in specific climates. Users can collaborate, support each other, and make more informed decisions based on shared information.

## Livability Score Calculation
The livability score is calculated using several environmental metrics, which are compared against ideal thresholds. Each deviation from these ideal values contributes to a reduction in the livability score:

* **Air Quality Index (AQI):** Measures the level of air pollution. Lower AQI values are better for health.
 
AQI Deviation = | User AQI - City AQI |


* **Heat Index:** The "feels-like" temperature combining air temperature and humidity.
 
Heat Index Deviation = | User Heat Index - City Heat Index |


* **Wind Speed:** Impacts air circulation and temperature comfort. Extreme speeds reduce livability.
 
Wind Speed Deviation = | User Wind Speed - City Wind Speed |


Additionally, a user's environmental stance (Pro, Neutral, or Anti) is factored in, affecting the overall livability score based on how well it aligns with the city's environmental policies.

## Machine Learning Integration (AI Prediction)

### AI Model Training
The app uses a **Random Forest Regressor** model to predict livability scores based on the environmental metrics. The model is trained on historical livability scores that are manually calculated, using metrics such as AQI, carbon intensity, heat index, and wind speed.

* **Features (X):** Environmental metrics (e.g., AQI, carbon intensity, heat index, wind speed).
* **Target (y):** Livability score.

### Prediction Formula
Predicted Livability Score = (1/n) ∑ Ti(X)

Where:
* *n* is the number of decision trees in the Random Forest model.
* *Ti(X)* is the prediction from the *i*-th decision tree.

The predicted livability score is compared with other cities in the dataset to compute a percentile rank, helping users understand how the city performs in relation to others.

## Flow of the Application
1. **User Preferences:** Users enter their preferences for various environmental factors, such as AQI, wind speed, and heat index.
2. **City Data Retrieval:** The app retrieves real-time or pre-existing data for the selected city.
3. **Score Calculation:**
    * For manually calculated scores, the app compares city data with user preferences and computes deviations for each metric.
    * For AI-predicted scores, the trained Random Forest model predicts the livability score based on the input preferences and city metrics.
4. **Risk Assessment & Climate Projections:**
    * The app provides a risk assessment of climate-related challenges, such as extreme weather events.
    * Users can view future climate projections to understand how livability may change in the chosen city.
5. **Results & Percentile Rank:** The app displays the livability score along with a percentile rank, helping users compare the livability of the selected city with others in the dataset.

## Sources

- **Environmental hazard** - [Wikipedia](https://en.wikipedia.org/wiki/Environmental_hazard)
- **Sustainability** - [Wikipedia](https://en.wikipedia.org/wiki/Sustainability)
- **Environmental impact assessment** - [Wikipedia](https://en.wikipedia.org/wiki/Environmental_impact_assessment)
- **How hot is too hot for the human body?** - [MIT Technology Review](https://www.technologyreview.com/2020/08/13/1006785/how-hot-is-too-hot-for-the-human-body/)

## Data Sources

- **Open-Meteo.com** - [API Web Service](https://open-meteo.com/)
- **OpenFEMA Data Sets** - [FEMA.gov](https://www.fema.gov/openfema)
- **Weather API** - [OpenWeatherMap](https://openweathermap.org/api)
- **CO2 Signal** - [CO2 Signal API](https://www.co2signal.com/)



