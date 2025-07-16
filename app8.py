from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

# In-memory data stores
animals = [
    {"id": 1, "name": "Lion"},
    {"id": 2, "name": "Elephant"},
    {"id": 3, "name": "Giraffe"}
]
feeding_log = []  # Each entry: {animal_id, food, timestamp}

# 1. Home route
@app.route('/')
def home():
    return "<h1>Zoo Keeper Feeding Tracker</h1><p>Use the API to manage feedings.</p>"

# 2. List all animals
@app.route('/animals')
def list_animals():
    return jsonify(animals)

# 3. Record feeding for an animal (POST)
@app.route('/feed/<int:animal_id>', methods=['POST'])
def feed_animal(animal_id):
    # Check animal exists
    animal = next((a for a in animals if a['id'] == animal_id), None)
    if not animal:
        abort(404, description="Animal not found")

    data = request.get_json() or {}
    food = data.get('food')
    if not food:
        abort(400, description="Missing 'food' in request body")

    entry = {
        "animal_id": animal_id,
        "animal": animal['name'],
        "food": food,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
    feeding_log.append(entry)
    return jsonify(entry), 201

# 4. Get feeding history
@app.route('/history')
def get_history():
    return jsonify(feeding_log)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
