from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

# In-memory data stores
properties = [
    {"id": 1, "name": "Cozy Cottage", "status": "available"},
    {"id": 2, "name": "City Loft", "status": "available"},
    {"id": 3, "name": "Beach House", "status": "available"}
]
bookings = []  # Each entry: {booking_id, property_id, guest_name, check_in, check_out}
next_booking_id = 1

# 1. Home route
@app.route('/')
def home():
    return "<h1>StayTracker API</h1><p>Manage properties and bookings for our Airbnb-like service.</p>"

# 2. List all properties and their status
@app.route('/properties')
def list_properties():
    return jsonify(properties)

# 3. Book a property (POST)
@app.route('/book', methods=['POST'])
def book_property():
    global next_booking_id
    data = request.get_json() or {}
    prop_id = data.get('property_id')
    guest = data.get('guest_name')
    check_in = data.get('check_in')
    check_out = data.get('check_out')

    prop = next((p for p in properties if p['id'] == prop_id), None)
    if not prop or prop['status'] != 'available':
        abort(400, description="Property not available or invalid property_id")
    if not guest or not check_in or not check_out:
        abort(400, description="Missing booking details")

    prop['status'] = 'booked'
    booking = {
        "booking_id": next_booking_id,
        "property_id": prop_id,
        "guest_name": guest,
        "check_in": check_in,
        "check_out": check_out
    }
    bookings.append(booking)
    next_booking_id += 1
    return jsonify(booking), 201

# 4. Checkout a property (POST)
@app.route('/checkout', methods=['POST'])
def checkout_property():
    data = request.get_json() or {}
    booking_id = data.get('booking_id')
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        abort(400, description="Invalid booking_id")

    prop = next((p for p in properties if p['id'] == booking['property_id']), None)
    prop['status'] = 'available'
    bookings.remove(booking)
    return jsonify({"message": "Checked out successfully", "booking_id": booking_id})

# 5. Get booking history
@app.route('/bookings')
def get_bookings():
    return jsonify(bookings)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
