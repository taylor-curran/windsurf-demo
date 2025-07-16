from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

# In-memory data stores
cars = [
    {"id": 1, "model": "Toyota Prius", "status": "available"},
    {"id": 2, "model": "Honda Civic", "status": "available"},
    {"id": 3, "model": "Tesla Model 3", "status": "available"}
]
trips = []  # Each entry: {trip_id, car_id, start_time, end_time, distance_km}
next_trip_id = 1

# 1. Home route
@app.route('/')
def home():
    return "<h1>RideTracker API</h1><p>Manage cars and trips for our Uber-like service.</p>"

# 2. List all cars and their status
@app.route('/cars')
def list_cars():
    return jsonify(cars)

# 3. Start a trip (POST)
@app.route('/trips/start', methods=['POST'])
def start_trip():
    global next_trip_id
    data = request.get_json() or {}
    car_id = data.get('car_id')
    car = next((c for c in cars if c['id'] == car_id), None)
    if not car or car['status'] != 'available':
        abort(400, description="Car not available or invalid car_id")

    car['status'] = 'in_use'
    trip = {
        "trip_id": next_trip_id,
        "car_id": car_id,
        "start_time": datetime.utcnow().isoformat() + 'Z',
        "end_time": None,
        "distance_km": None
    }
    trips.append(trip)
    next_trip_id += 1
    return jsonify(trip), 201

# 4. End a trip (POST)
@app.route('/trips/end', methods=['POST'])
def end_trip():
    data = request.get_json() or {}
    trip_id = data.get('trip_id')
    distance = data.get('distance_km')
    trip = next((t for t in trips if t['trip_id'] == trip_id), None)
    if not trip or trip['end_time'] is not None:
        abort(400, description="Invalid or already ended trip_id")

    car = next((c for c in cars if c['id'] == trip['car_id']), None)
    trip['end_time'] = datetime.utcnow().isoformat() + 'Z'
    trip['distance_km'] = distance or 0
    car['status'] = 'available'
    return jsonify(trip)

# 5. Get trip history
@app.route('/trips')
def get_trips():
    return jsonify(trips)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
