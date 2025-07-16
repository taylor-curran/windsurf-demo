from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# 1. Home route
@app.route('/')
def home():
    return "<h1>Welcome to the Basic Flask App!</h1>"

# 2. About route
@app.route('/about')
def about():
    return jsonify({
        "app": "Basic Flask App",
        "version": "1.0",
        "author": "Your Name"
    })

# 3. Dynamic greeting route
@app.route('/hello/<username>')
def hello_user(username):
    return render_template('hello.html', username=username)

# 4. Data endpoint (POST request)
@app.route('/data', methods=['POST'])
def data_endpoint():
    # Expect JSON payload
    payload = request.get_json() or {}
    response = {
        "received": payload,
        "status": "success"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
