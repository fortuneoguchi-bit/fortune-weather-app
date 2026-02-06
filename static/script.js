// Fortune Weather App - Main JavaScript File
// Backend API base URL
const BACKEND_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:5000' 
    : window.location.origin; // Use same origin when deployed

// Tab switching functionality
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.search-content').forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(`${tab}-search`).classList.add('active');
    });
});

// Search by city
function searchByCity() {
    const city = document.getElementById('cityInput').value.trim();
    const country = document.getElementById('countryInput').value.trim();
    
    if (!city) {
        showError('Please enter a city name');
        return;
    }
    
    const query = country ? `${city},${country}` : city;
    fetchWeather(`q=${query}`);
}

// Search by coordinates
function searchByCoordinates() {
    const lat = document.getElementById('latInput').value.trim();
    const lon = document.getElementById('lonInput').value.trim();
    
    if (!lat || !lon) {
        showError('Please enter both latitude and longitude');
        return;
    }
    
    fetchWeather(`lat=${lat}&lon=${lon}`);
}

// Search Nigerian city
function searchNigerianCity() {
    const city = document.getElementById('nigeriaSelect').value;
    
    if (!city) {
        showError('Please select a city');
        return;
    }
    
    fetchWeather(`q=${city},NG`);
}

// Quick search for popular cities
function quickSearch(city) {
    fetchWeather(`q=${city},NG`);
}

// Fetch weather data from Flask backend
async function fetchWeather(query) {
    const display = document.getElementById('weatherDisplay');
    display.innerHTML = '<div class="loading">⏳ Loading weather data...</div>';

    try {
        // Fetch current weather from Flask backend
        const currentResponse = await fetch(
            `${BACKEND_URL}/api/weather/current?${query}`
        );
        
        if (!currentResponse.ok) {
            const errorData = await currentResponse.json();
            throw new Error(errorData.error || 'City not found or invalid coordinates');
        }
        
        const currentData = await currentResponse.json();
        
        // Fetch 5-day forecast from Flask backend
        const forecastResponse = await fetch(
            `${BACKEND_URL}/api/weather/forecast?${query}`
        );
        
        if (!forecastResponse.ok) {
            throw new Error('Unable to fetch forecast data');
        }
        
        const forecastData = await forecastResponse.json();
        
        displayWeather(currentData, forecastData);
    } catch (error) {
        console.error('Weather fetch error:', error);
        showError(error.message + '. Please try again.');
    }
}

// Display weather information
function displayWeather(current, forecast) {
    const display = document.getElementById('weatherDisplay');
    
    // Get daily forecasts (one per day)
    const dailyForecasts = forecast.list.filter((item, index) => index % 8 === 0).slice(0, 5);
    
    const html = `
        <div class="weather-dashboard">
            <div class="weather-card current-weather">
                <div class="weather-main">
                    <div class="city-name">${current.name}</div>
                    <div class="country">${current.sys.country}</div>
                    <div class="temperature">${Math.round(current.main.temp)}°C</div>
                    <div class="description">${current.weather[0].description}</div>
                    <div class="weather-details">
                        <div class="detail-item">
                            <div class="detail-label">Feels Like</div>
                            <div class="detail-value">${Math.round(current.main.feels_like)}°C</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Humidity</div>
                            <div class="detail-value">${current.main.humidity}%</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Wind Speed</div>
                            <div class="detail-value">${current.wind.speed} m/s</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Pressure</div>
                            <div class="detail-value">${current.main.pressure} hPa</div>
                        </div>
                    </div>
                </div>
                <div class="weather-icon">
                    <img src="https://openweathermap.org/img/wn/${current.weather[0].icon}@4x.png" 
                         alt="${current.weather[0].description}">
                </div>
            </div>

            <div class="weather-card">
                <h3>Additional Info</h3>
                <div class="weather-details">
                    <div class="detail-item">
                        <div class="detail-label">Visibility</div>
                        <div class="detail-value">${(current.visibility / 1000).toFixed(1)} km</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Cloudiness</div>
                        <div class="detail-value">${current.clouds.all}%</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Min Temp</div>
                        <div class="detail-value">${Math.round(current.main.temp_min)}°C</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Max Temp</div>
                        <div class="detail-value">${Math.round(current.main.temp_max)}°C>
                    </div>
                </div>
            </div>

            <div class="weather-card">
                <h3>Sun Times</h3>
                <div class="weather-details">
                    <div class="detail-item">
                        <div class="detail-label">Sunrise</div>
                        <div class="detail-value">${new Date(current.sys.sunrise * 1000).toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit'})}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Sunset</div>
                        <div class="detail-value">${new Date(current.sys.sunset * 1000).toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit'})}</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="forecast-section">
            <h2>5-Day Forecast</h2>
            <div class="forecast-grid">
                ${dailyForecasts.map(day => `
                    <div class="forecast-item">
                        <div class="forecast-day">${new Date(day.dt * 1000).toLocaleDateString('en-US', {weekday: 'short', month: 'short', day: 'numeric'})}</div>
                        <div class="forecast-icon">
                            <img src="https://openweathermap.org/img/wn/${day.weather[0].icon}@2x.png" 
                                 alt="${day.weather[0].description}">
                        </div>
                        <div class="forecast-temp">${Math.round(day.main.temp)}°C</div>
                        <div style="color: #666; font-size: 0.9em; text-transform: capitalize;">${day.weather[0].description}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    display.innerHTML = html;
}

// Show error message
function showError(message) {
    const display = document.getElementById('weatherDisplay');
    display.innerHTML = `<div class="error">❌ ${message}</div>`;
}

// Load default weather for Lagos on page load
window.addEventListener('load', () => {
    fetchWeather('q=Lagos,NG');
});

// Enter key support for inputs
document.getElementById('cityInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchByCity();
});

document.getElementById('countryInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchByCity();
});
