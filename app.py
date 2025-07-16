from flask import Flask, render_template, jsonify, request
import numpy as np
import json

app = Flask(__name__)

# Game state
WORLD_SIZE = 2000
NUM_AI_PLAYERS = 10
NUM_FOOD = 100

@app.route('/')
def index():
    return render_template('game.html')

@app.route('/game_state')
def game_state():
    # In a real implementation, this would update AI positions and return current game state
    return jsonify({'status': 'ok'})

@app.route('/update_player', methods=['POST'])
def update_player():
    # Handle player position updates
    data = request.get_json()
    return jsonify({'status': 'ok'})

@app.route('/leaderboard')
def leaderboard():
    # Example route that returns top players
    mock_leaderboard = [
        {'name': 'Player1', 'score': 1500, 'rank': 1},
        {'name': 'Player2', 'score': 1200, 'rank': 2},
        {'name': 'Player3', 'score': 950, 'rank': 3},
        {'name': 'Player4', 'score': 800, 'rank': 4},
        {'name': 'Player5', 'score': 650, 'rank': 5}
    ]
    return jsonify({
        'leaderboard': mock_leaderboard,
        'total_players': len(mock_leaderboard)
    })

if __name__ == '__main__':
    app.run(debug=True)