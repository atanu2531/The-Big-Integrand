import requests
import time
import random

BACKEND_URL = "http://localhost:8000/api/location"

# Starting point (NYC)
lat, lon = 40.7128, -74.0060

print("Seeding drone trajectory data...")

for i in range(10):
    # Simulate movement
    lat += random.uniform(-0.001, 0.001)
    lon += random.uniform(-0.001, 0.001)

    payload = {"latitude": lat, "longitude": lon}
    try:
        response = requests.post(BACKEND_URL, json=payload)
        if response.status_code == 200:
            print(f"[{i+1}/10] Posted: {payload}")
        else:
            print(f"Failed to post: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.1)

print("Seeding complete.")
