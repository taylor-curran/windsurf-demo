from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# 1. Health check route
@app.route('/health')
def health_check():
    return jsonify({
        "status": "ok",
        "uptime": "72 hours"
    })

# 2. List items route
@app.route('/items')
def list_items():
    # In a real app, this might fetch from a database
    items = [
        {"id": 1, "name": "Widget"},
        {"id": 2, "name": "Gadget"}
    ]
    return jsonify(items)

# 3. Retrieve single item by ID
@app.route('/items/<int:item_id>')
def get_item(item_id):
    dummy_db = {1: "Widget", 2: "Gadget"}
    name = dummy_db.get(item_id)
    if not name:
        abort(404, description="Item not found")
    return jsonify({
        "id": item_id,
        "name": name
    })

# 4. Create new item (POST)
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json() or {}
    if 'name' not in data:
        abort(400, description="Missing 'name' in request body")
    # Simulate inserting into a database with ID 3
    new_item = {
        "id": 3,
        "name": data['name']
    }
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(debug=True)
