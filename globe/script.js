// City data with coordinates and information
const cities = {
    americas: [
        { name: "Seattle", lat: 47.6062, lng: -122.3321, country: "USA", region: "Pacific Northwest" },
        { name: "Portland", lat: 45.5152, lng: -122.6784, country: "USA", region: "Pacific Northwest" },
        { name: "San Francisco", lat: 37.7749, lng: -122.4194, country: "USA", region: "California" },
        { name: "San Jose", lat: 37.3382, lng: -121.8863, country: "USA", region: "California" },
        { name: "Los Angeles", lat: 34.0522, lng: -118.2437, country: "USA", region: "California" },
        { name: "San Diego", lat: 32.7157, lng: -117.1611, country: "USA", region: "California" },
        { name: "Austin", lat: 30.2672, lng: -97.7431, country: "USA", region: "Texas" },
        { name: "Dallas", lat: 32.7767, lng: -96.7970, country: "USA", region: "Texas" },
        { name: "New Orleans", lat: 29.9511, lng: -90.0715, country: "USA", region: "Louisiana" },
        { name: "Atlanta", lat: 33.7490, lng: -84.3880, country: "USA", region: "Georgia" },
        { name: "Washington DC", lat: 38.9072, lng: -77.0369, country: "USA", region: "District of Columbia" },
        { name: "Boston", lat: 42.3601, lng: -71.0589, country: "USA", region: "Massachusetts" },
        { name: "New York", lat: 40.7128, lng: -74.0060, country: "USA", region: "New York" },
        { name: "Montreal", lat: 45.5017, lng: -73.5673, country: "Canada", region: "Quebec" },
        { name: "Sao Paulo", lat: -23.5505, lng: -46.6333, country: "Brazil", region: "Sao Paulo" },
        { name: "Rio de Janeiro", lat: -22.9068, lng: -43.1729, country: "Brazil", region: "Rio de Janeiro" }
    ],
    "asia-pacific": [
        { name: "Wellington", lat: -41.2866, lng: 174.7756, country: "New Zealand", region: "Wellington" },
        { name: "Singapore", lat: 1.3521, lng: 103.8198, country: "Singapore", region: "Singapore" },
        { name: "Mumbai", lat: 19.0760, lng: 72.8777, country: "India", region: "Maharashtra" },
        { name: "Chennai", lat: 13.0827, lng: 80.2707, country: "India", region: "Tamil Nadu" },
        { name: "Bangalore", lat: 12.9716, lng: 77.5946, country: "India", region: "Karnataka" }
    ],
    "africa": [
        { name: "Cape Town", lat: -33.9249, lng: 18.4241, country: "South Africa", region: "Western Cape" },
        { name: "Johannesburg", lat: -26.2041, lng: 28.0473, country: "South Africa", region: "Gauteng" },
        { name: "Mauritius", lat: -20.3484, lng: 57.5522, country: "Mauritius", region: "Port Louis" }
    ],
    emea: [
        { name: "Dubai", lat: 25.2048, lng: 55.2708, country: "UAE", region: "Dubai" },
        { name: "Tel Aviv", lat: 32.0853, lng: 34.7818, country: "Israel", region: "Tel Aviv" },
        { name: "Istanbul", lat: 41.0082, lng: 28.9784, country: "Turkey", region: "Istanbul" },
        { name: "Kiev", lat: 50.4501, lng: 30.5234, country: "Ukraine", region: "Kiev" },
        { name: "Lviv", lat: 49.8397, lng: 24.0297, country: "Ukraine", region: "Lviv" },
        { name: "Bucharest", lat: 44.4268, lng: 26.1025, country: "Romania", region: "Bucharest" },
        { name: "Cluj-Napoca", lat: 46.7712, lng: 23.6236, country: "Romania", region: "Cluj" },
        { name: "Sofia", lat: 42.6977, lng: 23.3219, country: "Bulgaria", region: "Sofia" },
        { name: "Skopje", lat: 42.0027, lng: 21.4262, country: "North Macedonia", region: "Skopje" },
        { name: "Athens", lat: 37.9838, lng: 23.7275, country: "Greece", region: "Attica" },
        { name: "Thessaloniki", lat: 40.6401, lng: 22.9444, country: "Greece", region: "Central Macedonia" },
        { name: "Zagreb", lat: 45.8150, lng: 15.9819, country: "Croatia", region: "Zagreb" },
        { name: "Warsaw", lat: 52.2297, lng: 21.0122, country: "Poland", region: "Masovia" },
        { name: "Gdansk", lat: 54.3520, lng: 18.6466, country: "Poland", region: "Pomerania" },
        { name: "Cracow", lat: 50.0647, lng: 19.9450, country: "Poland", region: "Lesser Poland" },
        { name: "Tallinn", lat: 59.4370, lng: 24.7536, country: "Estonia", region: "Harju" },
        { name: "Riga", lat: 56.9496, lng: 24.1052, country: "Latvia", region: "Riga" },
        { name: "Stockholm", lat: 59.3293, lng: 18.0686, country: "Sweden", region: "Stockholm" },
        { name: "Helsinki", lat: 60.1699, lng: 24.9384, country: "Finland", region: "Uusimaa" },
        { name: "Oslo", lat: 59.9139, lng: 10.7522, country: "Norway", region: "Oslo" },
        { name: "Edinburgh", lat: 55.9533, lng: -3.1883, country: "UK", region: "Scotland" },
        { name: "Glasgow", lat: 55.8642, lng: -4.2518, country: "UK", region: "Scotland" },
        { name: "Dublin", lat: 53.3498, lng: -6.2603, country: "Ireland", region: "Leinster" },
        { name: "Manchester", lat: 53.4808, lng: -2.2426, country: "UK", region: "England" },
        { name: "London", lat: 51.5074, lng: -0.1278, country: "UK", region: "England" },
        { name: "Amsterdam", lat: 52.3676, lng: 4.9041, country: "Netherlands", region: "North Holland" },
        { name: "Utrecht", lat: 52.0907, lng: 5.1214, country: "Netherlands", region: "Utrecht" },
        { name: "Brussels", lat: 50.8503, lng: 4.3517, country: "Belgium", region: "Brussels" },
        { name: "Berlin", lat: 52.5200, lng: 13.4050, country: "Germany", region: "Berlin" },
        { name: "Frankfurt", lat: 50.1109, lng: 8.6821, country: "Germany", region: "Hesse" },
        { name: "Hamburg", lat: 53.5511, lng: 9.9937, country: "Germany", region: "Hamburg" },
        { name: "Munich", lat: 48.1351, lng: 11.5820, country: "Germany", region: "Bavaria" },
        { name: "Zurich", lat: 47.3769, lng: 8.5417, country: "Switzerland", region: "Zurich" },
        { name: "Geneva", lat: 46.2044, lng: 6.1432, country: "Switzerland", region: "Geneva" },
        { name: "Milan", lat: 45.4642, lng: 9.1900, country: "Italy", region: "Lombardy" },
        { name: "Rome", lat: 41.9028, lng: 12.4964, country: "Italy", region: "Lazio" },
        { name: "Monaco", lat: 43.7384, lng: 7.4246, country: "Monaco", region: "Monaco" },
        { name: "Marseille", lat: 43.2965, lng: 5.3698, country: "France", region: "Provence-Alpes-Côte d'Azur" },
        { name: "Toulouse", lat: 43.6047, lng: 1.4442, country: "France", region: "Occitanie" },
        { name: "Nantes", lat: 47.2184, lng: -1.5536, country: "France", region: "Pays de la Loire" },
        { name: "Rennes", lat: 48.1173, lng: -1.6778, country: "France", region: "Brittany" },
        { name: "Montpellier", lat: 43.6108, lng: 3.8767, country: "France", region: "Occitanie" },
        { name: "Paris", lat: 48.8566, lng: 2.3522, country: "France", region: "Île-de-France" },
        { name: "Lille", lat: 50.6292, lng: 3.0573, country: "France", region: "Hauts-de-France" },
        { name: "Lyon", lat: 45.7578, lng: 4.8320, country: "France", region: "Auvergne-Rhône-Alpes" },
        { name: "Barcelona", lat: 41.3851, lng: 2.1734, country: "Spain", region: "Catalonia" },
        { name: "Madrid", lat: 40.4168, lng: -3.7038, country: "Spain", region: "Madrid" },
        { name: "Porto", lat: 41.1579, lng: -8.6291, country: "Portugal", region: "Porto" },
        { name: "Lisbon", lat: 38.7223, lng: -9.1393, country: "Portugal", region: "Lisbon" },
        { name: "Copenhagen", lat: 55.6761, lng: 12.5683, country: "Denmark", region: "Capital Region" }
    ]
};

let map;
let markers = [];

// Initialize the map
function initMap() {
    // Create the map
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: { lat: 20, lng: 0 },
        styles: [
            {
                featureType: 'water',
                elementType: 'geometry',
                stylers: [{ color: '#e8f4f8' }]
            },
            {
                featureType: 'landscape',
                elementType: 'geometry',
                stylers: [{ color: '#f5f5f5' }]
            },
            {
                featureType: 'administrative',
                elementType: 'geometry.stroke',
                stylers: [{ color: '#b8d4da' }, { lightness: 10 }]
            },
            {
                featureType: 'road',
                elementType: 'geometry',
                stylers: [{ color: '#ffffff' }]
            },
            {
                featureType: 'poi',
                elementType: 'geometry',
                stylers: [{ color: '#f5f5f5' }]
            }
        ]
    });

    // Add markers for all cities
    addMarkers();
}

// Create custom marker icon
function createCustomMarker(region) {
    const colors = {
        'americas': '#e74c3c',
        'asia-pacific': '#f39c12',
        'south-africa': '#9b59b6',
        'emea': '#27ae60'
    };

    return {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: colors[region],
        fillOpacity: 1,
        strokeColor: '#ffffff',
        strokeWeight: 3,
        scale: 8
    };
}

// Add markers to the map
function addMarkers() {
    Object.keys(cities).forEach(region => {
        cities[region].forEach(city => {
            const marker = new google.maps.Marker({
                position: { lat: city.lat, lng: city.lng },
                map: map,
                title: `${city.name}, ${city.country}`,
                icon: createCustomMarker(region),
                animation: google.maps.Animation.DROP
            });

            // Create info window content
            const infoWindow = new google.maps.InfoWindow({
                content: `
                    <div class="info-window">
                        <h3>${city.name}</h3>
                        <p><strong>Country:</strong> ${city.country}</p>
                        <p><strong>Region:</strong> ${city.region}</p>
                    </div>
                `
            });

            // Add click event to marker
            marker.addListener('click', () => {
                infoWindow.open(map, marker);
                // Add bounce animation
                marker.setAnimation(google.maps.Animation.BOUNCE);
                setTimeout(() => {
                    marker.setAnimation(null);
                }, 750);
            });

            // Add hover effects
            marker.addListener('mouseover', () => {
                marker.setScale(10);
            });

            marker.addListener('mouseout', () => {
                marker.setScale(8);
            });

            markers.push(marker);
        });
    });
}

// Function to fit map bounds to show all markers
function fitMapToMarkers() {
    if (markers.length > 0) {
        const bounds = new google.maps.LatLngBounds();
        markers.forEach(marker => {
            bounds.extend(marker.getPosition());
        });
        map.fitBounds(bounds);
    }
}

// Function to filter markers by region
function filterMarkers(region) {
    markers.forEach((marker, index) => {
        const cityData = getAllCities()[index];
        if (region === 'all' || cityData.region === region) {
            marker.setVisible(true);
        } else {
            marker.setVisible(false);
        }
    });
}

// Helper function to get all cities in a flat array
function getAllCities() {
    const allCities = [];
    Object.keys(cities).forEach(region => {
        cities[region].forEach(city => {
            allCities.push({ ...city, region });
        });
    });
    return allCities;
}

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Add click handlers to legend items for filtering
    const legendItems = document.querySelectorAll('.legend-item');
    legendItems.forEach(item => {
        item.addEventListener('click', () => {
            const region = item.querySelector('.legend-dot').classList[1];
            filterMarkers(region);
        });
    });

    // Add double-click to legend to show all markers
    legendItems.forEach(item => {
        item.addEventListener('dblclick', () => {
            filterMarkers('all');
        });
    });
});

// Handle window resize
window.addEventListener('resize', () => {
    if (map) {
        google.maps.event.trigger(map, 'resize');
    }
}); 