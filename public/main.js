const map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

let droneMarker;

async function updateDroneLocation() {
    try {
        const response = await fetch('/api/location');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        if (data.latitude && data.longitude) {
            const latLng = [data.latitude, data.longitude];
            if (droneMarker) {
                droneMarker.setLatLng(latLng);
            } else {
                droneMarker = L.marker(latLng).addTo(map);
            }
            map.setView(latLng, 13);
        }
    } catch (error) {
        console.error('Error fetching drone location:', error);
    }
}

setInterval(updateDroneLocation, 3000);
updateDroneLocation();
