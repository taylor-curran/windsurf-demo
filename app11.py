from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

# In-memory data stores
books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "price": 9.99},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 7.99},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 8.99}
]
orders = []  # Each entry: {order_id, book_id, quantity, total_price, timestamp}
next_order_id = 1

# 1. Home route
@app.route('/')
def home():
    return "<h1>BookStore API</h1><p>Browse books and place orders.</p>"

# 2. List all books
@app.route('/books')
def list_books():
    return jsonify(books)

# 3. Get details for a specific book
@app.route('/books/<int:book_id>')
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        abort(404, description="Book not found")
    return jsonify(book)

# 4. Place an order (POST)
@app.route('/order', methods=['POST'])
def place_order():
    global next_order_id
    data = request.get_json() or {}
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)

    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        abort(400, description="Invalid book_id")
    if quantity < 1:
        abort(400, description="Quantity must be at least 1")

    total_price = round(book['price'] * quantity, 2)
    order = {
        "order_id": next_order_id,
        "book_id": book_id,
        "quantity": quantity,
        "total_price": total_price,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
    orders.append(order)
    next_order_id += 1
    return jsonify(order), 201

# 5. Get order history
@app.route('/orders')
def get_orders():
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
