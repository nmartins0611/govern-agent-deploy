// Initialize the map
const map = L.map('map').setView([20, 0], 2);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18,
    minZoom: 2
}).addTo(map);

// Add markers for each country
cheeseburgerData.forEach(item => {
    const circle = L.circle([item.lat, item.lng], {
        color: getColor(item.consumption),
        fillColor: getColor(item.consumption),
        fillOpacity: 0.6,
        radius: getRadius(item.consumption),
        weight: 2
    }).addTo(map);

    // Create popup content
    const popupContent = `
        <div style="min-width: 200px;">
            <h4>${item.country}</h4>
            <p><strong>🍔 Consumption:</strong> ${item.consumption} burgers/year</p>
            <p><strong>👥 Population:</strong> ${item.population}</p>
            <p><strong>📊 Level:</strong> ${getConsumptionLevel(item.consumption)}</p>
        </div>
    `;

    circle.bindPopup(popupContent);

    // Add tooltip on hover
    circle.bindTooltip(`${item.country}: ${item.consumption} burgers/year`, {
        permanent: false,
        direction: 'top'
    });
});

// Function to get consumption level description
function getConsumptionLevel(consumption) {
    if (consumption >= 76) return 'Extreme';
    if (consumption >= 51) return 'Very High';
    if (consumption >= 26) return 'High';
    if (consumption >= 11) return 'Medium';
    return 'Low';
}

// Populate top 5 countries
function displayTopCountries() {
    const sorted = [...cheeseburgerData].sort((a, b) => b.consumption - a.consumption);
    const top5 = sorted.slice(0, 5);

    const listElement = document.getElementById('top-countries');
    listElement.innerHTML = top5.map(item =>
        `<li><strong>${item.country}</strong>: ${item.consumption} burgers/year</li>`
    ).join('');
}

// Display statistics on page load
displayTopCountries();

// Calculate and display global statistics
function displayGlobalStats() {
    const totalConsumption = cheeseburgerData.reduce((sum, item) => sum + item.consumption, 0);
    const avgConsumption = (totalConsumption / cheeseburgerData.length).toFixed(1);

    console.log(`Global Average: ${avgConsumption} cheeseburgers per person per year`);
    console.log(`Countries tracked: ${cheeseburgerData.length}`);
}

displayGlobalStats();

// Add zoom controls hint
map.on('zoomend', function() {
    const zoom = map.getZoom();
    if (zoom < 3) {
        console.log('Zoom in to see individual countries more clearly!');
    }
});
