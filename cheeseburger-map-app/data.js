// Sample cheeseburger consumption data
// Format: [latitude, longitude, country name, burgers per person per year]
const cheeseburgerData = [
    // North America
    { lat: 37.0902, lng: -95.7129, country: "United States", consumption: 85, population: "331M" },
    { lat: 56.1304, lng: -106.3468, country: "Canada", consumption: 62, population: "38M" },
    { lat: 23.6345, lng: -102.5528, country: "Mexico", consumption: 34, population: "128M" },

    // South America
    { lat: -14.2350, lng: -51.9253, country: "Brazil", consumption: 28, population: "213M" },
    { lat: -38.4161, lng: -63.6167, country: "Argentina", consumption: 45, population: "45M" },
    { lat: -9.1900, lng: -75.0152, country: "Peru", consumption: 18, population: "33M" },
    { lat: 4.5709, lng: -74.2973, country: "Colombia", consumption: 22, population: "51M" },

    // Europe
    { lat: 51.1657, lng: 10.4515, country: "Germany", consumption: 38, population: "83M" },
    { lat: 46.2276, lng: 2.2137, country: "France", consumption: 32, population: "67M" },
    { lat: 55.3781, lng: -3.4360, country: "United Kingdom", consumption: 48, population: "67M" },
    { lat: 41.8719, lng: 12.5674, country: "Italy", consumption: 25, population: "60M" },
    { lat: 40.4637, lng: -3.7492, country: "Spain", consumption: 29, population: "47M" },
    { lat: 52.1326, lng: 5.2913, country: "Netherlands", consumption: 42, population: "17M" },
    { lat: 50.5039, lng: 4.4699, country: "Belgium", consumption: 41, population: "11M" },
    { lat: 60.1282, lng: 18.6435, country: "Sweden", consumption: 36, population: "10M" },
    { lat: 52.2297, lng: 21.0122, country: "Poland", consumption: 31, population: "38M" },

    // Asia
    { lat: 35.8617, lng: 104.1954, country: "China", consumption: 12, population: "1.4B" },
    { lat: 36.2048, lng: 138.2529, country: "Japan", consumption: 26, population: "126M" },
    { lat: 20.5937, lng: 78.9629, country: "India", consumption: 5, population: "1.4B" },
    { lat: 35.9078, lng: 127.7669, country: "South Korea", consumption: 33, population: "52M" },
    { lat: 15.8700, lng: 100.9925, country: "Thailand", consumption: 14, population: "70M" },
    { lat: 1.3521, lng: 103.8198, country: "Singapore", consumption: 44, population: "5.7M" },
    { lat: 14.0583, lng: 108.2772, country: "Vietnam", consumption: 11, population: "98M" },
    { lat: -0.7893, lng: 113.9213, country: "Indonesia", consumption: 9, population: "274M" },

    // Middle East
    { lat: 23.8859, lng: 45.0792, country: "Saudi Arabia", consumption: 52, population: "35M" },
    { lat: 25.2048, lng: 55.2708, country: "United Arab Emirates", consumption: 58, population: "10M" },
    { lat: 29.3117, lng: 47.4818, country: "Kuwait", consumption: 54, population: "4.3M" },
    { lat: 31.0461, lng: 34.8516, country: "Israel", consumption: 47, population: "9.2M" },

    // Oceania
    { lat: -25.2744, lng: 133.7751, country: "Australia", consumption: 71, population: "26M" },
    { lat: -40.9006, lng: 174.8860, country: "New Zealand", consumption: 68, population: "5M" },

    // Africa
    { lat: -30.5595, lng: 22.9375, country: "South Africa", consumption: 24, population: "60M" },
    { lat: 26.8206, lng: 30.8025, country: "Egypt", consumption: 16, population: "102M" },
    { lat: 9.1450, lng: 40.4897, country: "Ethiopia", consumption: 3, population: "115M" },
    { lat: 6.5244, lng: 3.3792, country: "Nigeria", consumption: 8, population: "206M" },
    { lat: -1.2921, lng: 36.8219, country: "Kenya", consumption: 7, population: "54M" }
];

// Color coding based on consumption levels
function getColor(consumption) {
    if (consumption >= 76) return '#ffffcc';
    if (consumption >= 51) return '#c2e699';
    if (consumption >= 26) return '#78c679';
    if (consumption >= 11) return '#31a354';
    return '#006837';
}

// Get radius based on consumption (for circle markers)
function getRadius(consumption) {
    return Math.sqrt(consumption) * 50000;
}
