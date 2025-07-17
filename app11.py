from flask import Flask, jsonify, request, abort
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

app = Flask(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
limiter.init_app(app)

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
@limiter.limit("30 per minute")
def home():
    return "<h1>BookStore API</h1><p>Browse books and place orders.</p>"

# 2. List all books
@app.route('/books')
@limiter.limit("10 per minute")
def list_books():
    return jsonify(books)

# 3. Get details for a specific book
@app.route('/books/<int:book_id>')
@limiter.limit("20 per minute")
def get_book(book_id):
    if book_id < 1 or book_id > 10000:
        abort(400, description="Invalid book ID")
    
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        abort(404, description="Book not found")
    return jsonify(book)

# 4. Place an order (POST)
@app.route('/order', methods=['POST'])
@limiter.limit("5 per minute")
def place_order():
    global next_order_id
    
    if not request.is_json:
        abort(400, description="Content-Type must be application/json")
    
    try:
        data = request.get_json(force=True)
    except Exception:
        abort(400, description="Invalid JSON")
    
    if not isinstance(data, dict):
        abort(400, description="Request body must be a JSON object")
    
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)
    
    if not isinstance(book_id, int) or book_id < 1 or book_id > 10000:
        abort(400, description="Invalid book_id: must be integer between 1 and 10000")
    
    if not isinstance(quantity, int) or quantity < 1 or quantity > 100:
        abort(400, description="Invalid quantity: must be integer between 1 and 100")

    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        abort(400, description="Invalid book_id")
        return  # This line will never be reached, but helps with type checking
    
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
@limiter.limit("10 per minute")
def get_orders():
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
