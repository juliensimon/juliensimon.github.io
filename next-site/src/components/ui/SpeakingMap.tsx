'use client';

import { useEffect, useRef } from 'react';

interface City {
  name: string;
  lat: number;
  lng: number;
  country: string;
}

interface Region {
  name: string;
  color: string;
  cities: City[];
}

const REGIONS: Region[] = [
  {
    name: 'Americas',
    color: '#e74c3c',
    cities: [
      { name: 'Seattle', lat: 47.6062, lng: -122.3321, country: 'USA' },
      { name: 'Portland', lat: 45.5152, lng: -122.6784, country: 'USA' },
      { name: 'San Francisco', lat: 37.7749, lng: -122.4194, country: 'USA' },
      { name: 'San Jose', lat: 37.3382, lng: -121.8863, country: 'USA' },
      { name: 'Los Angeles', lat: 34.0522, lng: -118.2437, country: 'USA' },
      { name: 'Las Vegas', lat: 36.1699, lng: -115.1398, country: 'USA' },
      { name: 'San Diego', lat: 32.7157, lng: -117.1611, country: 'USA' },
      { name: 'Austin', lat: 30.2672, lng: -97.7431, country: 'USA' },
      { name: 'Dallas', lat: 32.7767, lng: -96.7970, country: 'USA' },
      { name: 'New Orleans', lat: 29.9511, lng: -90.0715, country: 'USA' },
      { name: 'Atlanta', lat: 33.7490, lng: -84.3880, country: 'USA' },
      { name: 'Washington DC', lat: 38.9072, lng: -77.0369, country: 'USA' },
      { name: 'Boston', lat: 42.3601, lng: -71.0589, country: 'USA' },
      { name: 'New York', lat: 40.7128, lng: -74.0060, country: 'USA' },
      { name: 'Montreal', lat: 45.5017, lng: -73.5673, country: 'Canada' },
      { name: 'Sao Paulo', lat: -23.5505, lng: -46.6333, country: 'Brazil' },
      { name: 'Rio de Janeiro', lat: -22.9068, lng: -43.1729, country: 'Brazil' },
    ],
  },
  {
    name: 'Asia Pacific',
    color: '#f39c12',
    cities: [
      { name: 'Wellington', lat: -41.2866, lng: 174.7756, country: 'New Zealand' },
      { name: 'Singapore', lat: 1.3521, lng: 103.8198, country: 'Singapore' },
      { name: 'Mumbai', lat: 19.0760, lng: 72.8777, country: 'India' },
      { name: 'Chennai', lat: 13.0827, lng: 80.2707, country: 'India' },
      { name: 'Bangalore', lat: 12.9716, lng: 77.5946, country: 'India' },
    ],
  },
  {
    name: 'Africa',
    color: '#9b59b6',
    cities: [
      { name: 'Cape Town', lat: -33.9249, lng: 18.4241, country: 'South Africa' },
      { name: 'Stellenbosch', lat: -33.9321, lng: 18.8602, country: 'South Africa' },
      { name: 'Johannesburg', lat: -26.2041, lng: 28.0473, country: 'South Africa' },
      { name: 'Mauritius', lat: -20.3484, lng: 57.5522, country: 'Mauritius' },
    ],
  },
  {
    name: 'EMEA',
    color: '#27ae60',
    cities: [
      { name: 'Dubai', lat: 25.2048, lng: 55.2708, country: 'UAE' },
      { name: 'Tel Aviv', lat: 32.0853, lng: 34.7818, country: 'Israel' },
      { name: 'Istanbul', lat: 41.0082, lng: 28.9784, country: 'Turkey' },
      { name: 'Kiev', lat: 50.4501, lng: 30.5234, country: 'Ukraine' },
      { name: 'Bucharest', lat: 44.4268, lng: 26.1025, country: 'Romania' },
      { name: 'Sofia', lat: 42.6977, lng: 23.3219, country: 'Bulgaria' },
      { name: 'Athens', lat: 37.9838, lng: 23.7275, country: 'Greece' },
      { name: 'Zagreb', lat: 45.8150, lng: 15.9819, country: 'Croatia' },
      { name: 'Warsaw', lat: 52.2297, lng: 21.0122, country: 'Poland' },
      { name: 'Gdansk', lat: 54.3520, lng: 18.6466, country: 'Poland' },
      { name: 'Cracow', lat: 50.0647, lng: 19.9450, country: 'Poland' },
      { name: 'Tallinn', lat: 59.4370, lng: 24.7536, country: 'Estonia' },
      { name: 'Riga', lat: 56.9496, lng: 24.1052, country: 'Latvia' },
      { name: 'Stockholm', lat: 59.3293, lng: 18.0686, country: 'Sweden' },
      { name: 'Helsinki', lat: 60.1699, lng: 24.9384, country: 'Finland' },
      { name: 'Oslo', lat: 59.9139, lng: 10.7522, country: 'Norway' },
      { name: 'Copenhagen', lat: 55.6761, lng: 12.5683, country: 'Denmark' },
      { name: 'Cambridge', lat: 52.2053, lng: 0.1218, country: 'UK' },
      { name: 'Edinburgh', lat: 55.9533, lng: -3.1883, country: 'UK' },
      { name: 'Manchester', lat: 53.4808, lng: -2.2426, country: 'UK' },
      { name: 'London', lat: 51.5074, lng: -0.1278, country: 'UK' },
      { name: 'Dublin', lat: 53.3498, lng: -6.2603, country: 'Ireland' },
      { name: 'Kilkenny', lat: 52.6541, lng: -7.2448, country: 'Ireland' },
      { name: 'Amsterdam', lat: 52.3676, lng: 4.9041, country: 'Netherlands' },
      { name: 'Brussels', lat: 50.8503, lng: 4.3517, country: 'Belgium' },
      { name: 'Berlin', lat: 52.5200, lng: 13.4050, country: 'Germany' },
      { name: 'Frankfurt', lat: 50.1109, lng: 8.6821, country: 'Germany' },
      { name: 'Hamburg', lat: 53.5511, lng: 9.9937, country: 'Germany' },
      { name: 'Munich', lat: 48.1351, lng: 11.5820, country: 'Germany' },
      { name: 'Europa-Park', lat: 48.2667, lng: 7.7167, country: 'Germany' },
      { name: 'Zurich', lat: 47.3769, lng: 8.5417, country: 'Switzerland' },
      { name: 'Geneva', lat: 46.2044, lng: 6.1432, country: 'Switzerland' },
      { name: 'Milan', lat: 45.4642, lng: 9.1900, country: 'Italy' },
      { name: 'Rome', lat: 41.9028, lng: 12.4964, country: 'Italy' },
      { name: 'Rimini', lat: 44.0582, lng: 12.5645, country: 'Italy' },
      { name: 'Monaco', lat: 43.7384, lng: 7.4246, country: 'Monaco' },
      { name: 'Barcelona', lat: 41.3851, lng: 2.1734, country: 'Spain' },
      { name: 'Madrid', lat: 40.4168, lng: -3.7038, country: 'Spain' },
      { name: 'Lisbon', lat: 38.7223, lng: -9.1393, country: 'Portugal' },
      { name: 'Porto', lat: 41.1579, lng: -8.6291, country: 'Portugal' },
      { name: 'Paris', lat: 48.8566, lng: 2.3522, country: 'France' },
      { name: 'Lyon', lat: 45.7578, lng: 4.8320, country: 'France' },
      { name: 'Marseille', lat: 43.2965, lng: 5.3698, country: 'France' },
      { name: 'Toulouse', lat: 43.6047, lng: 1.4442, country: 'France' },
      { name: 'Nantes', lat: 47.2184, lng: -1.5536, country: 'France' },
      { name: 'Bordeaux', lat: 44.8378, lng: -0.5792, country: 'France' },
      { name: 'Lille', lat: 50.6292, lng: 3.0573, country: 'France' },
      { name: 'Strasbourg', lat: 48.5734, lng: 7.7521, country: 'France' },
      { name: 'Grenoble', lat: 45.1885, lng: 5.7245, country: 'France' },
      { name: 'Rennes', lat: 48.1173, lng: -1.6778, country: 'France' },
      { name: 'Montpellier', lat: 43.6108, lng: 3.8767, country: 'France' },
      { name: 'Cannes', lat: 43.5528, lng: 7.0174, country: 'France' },
      { name: 'Luxembourg', lat: 49.6116, lng: 6.1319, country: 'Luxembourg' },
      { name: 'Budapest', lat: 47.4979, lng: 19.0402, country: 'Hungary' },
    ],
  },
];

export default function SpeakingMap() {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);

  useEffect(() => {
    if (mapInstanceRef.current || !mapRef.current) return;

    // Dynamic import to avoid SSR issues (Leaflet requires window)
    import('leaflet').then((L) => {
      if (!mapRef.current || mapInstanceRef.current) return;

      // Create the map
      const map = L.map(mapRef.current, {
        center: [30, 10],
        zoom: 2,
        zoomControl: true,
        attributionControl: true,
      });

      // CartoDB dark_all tile layer - free, no API key, dark aesthetic
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19,
      }).addTo(map);

      // Add circle markers for each city
      REGIONS.forEach((region) => {
        region.cities.forEach((city) => {
          const marker = L.circleMarker([city.lat, city.lng], {
            radius: 6,
            fillColor: region.color,
            fillOpacity: 0.85,
            color: '#ffffff',
            weight: 1,
          }).addTo(map);

          marker.bindPopup(
            `<div style="font-family:sans-serif;font-size:13px;color:#0f172a"><strong>${city.name}</strong><br/>${city.country}</div>`
          );
        });
      });

      mapInstanceRef.current = map;
    });

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  return (
    <div className="glass-card rounded-xl overflow-hidden">
      <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossOrigin=""
      />
      <div ref={mapRef} className="w-full h-[400px] sm:h-[500px]" />
      <div className="flex flex-wrap gap-4 p-4 justify-center">
        {REGIONS.map((r) => (
          <div key={r.name} className="flex items-center gap-1.5 text-xs text-text-muted">
            <span className="w-3 h-3 rounded-full inline-block" style={{ backgroundColor: r.color }} />
            {r.name} ({r.cities.length})
          </div>
        ))}
      </div>
    </div>
  );
}
