import http.server
import socketserver
import json

PORT = 8000

# Default location (New York City)
drone_location = {
    "latitude": 40.7128,
    "longitude": -74.0060
}
location_history = [drone_location.copy()]

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve files out of the 'public' directory
        super().__init__(*args, directory='public', **kwargs)

    def do_GET(self):
        if self.path == '/api/location':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(drone_location).encode())
            return
        elif self.path == '/api/history':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(location_history).encode())
            return

        # For all other paths, let SimpleHTTPRequestHandler serve the file
        # from the 'public' directory as specified in __init__
        super().do_GET()

    def do_POST(self):
        if self.path == '/api/location':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)

                if 'latitude' in data and 'longitude' in data:
                    global drone_location
                    drone_location = {
                        "latitude": float(data['latitude']),
                        "longitude": float(data['longitude'])
                    }
                    location_history.append(drone_location.copy())
                    print(f"Drone location updated to: {drone_location}")
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "Location updated"}).encode())
                else:
                    self.send_error(400, "Invalid location data")
            except Exception as e:
                print(f"Error processing POST request: {e}")
                self.send_error(500, "Server error")
        else:
            self.send_error(404, "Not Found")


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
