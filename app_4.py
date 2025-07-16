from flask import Flask, render_template, jsonify, request
import numpy as np
import json
import random
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)
app.config['DEBUG'] = True

# Game configuration constants
GAME_WORLD_SIZE = 2500
MAX_AI_PLAYERS = 15
TOTAL_FOOD_ITEMS = 150
PLAYER_SPEED = 5.0

@app.route('/')
def main_game_page():
    """Serve the main game interface"""
    return render_template('game.html')

@app.route('/game_state')
def get_current_game_state():
    """Return the current state of the game world"""
    # Simulate game state with random data
    current_time = datetime.now().isoformat()
    game_data = {
        'timestamp': current_time,
        'world_size': GAME_WORLD_SIZE,
        'active_players': random.randint(5, MAX_AI_PLAYERS),
        'food_remaining': random.randint(50, TOTAL_FOOD_ITEMS),
        'status': 'active'
    }
    return jsonify(game_data)

@app.route('/update_player', methods=['POST'])
def handle_player_update():
    """Process player movement and state updates"""
    try:
        player_data = request.get_json()
        if not player_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate player data
        required_fields = ['player_id', 'x', 'y']
        if not all(field in player_data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        response = {
            'success': True,
            'player_id': player_data.get('player_id'),
            'updated_at': datetime.now().isoformat(),
            'message': 'Player updated successfully'
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/leaderboard')
def get_player_leaderboard():
    """Retrieve and return the current player rankings"""
    # Generate dynamic leaderboard data
    player_names = ['AlphaGamer', 'BetaWarrior', 'GammaHunter', 'DeltaChampion', 'EpsilonMaster', 'ZetaLegend']
    
    leaderboard_data = []
    for i, name in enumerate(player_names):
        player_entry = {
            'player_name': name,
            'current_score': random.randint(500, 2000),
            'position': i + 1,
            'games_played': random.randint(10, 100),
            'win_rate': round(random.uniform(0.3, 0.9), 2)
        }
        leaderboard_data.append(player_entry)
    
    # Sort by score descending
    leaderboard_data.sort(key=lambda x: x['current_score'], reverse=True)
    
    # Update positions after sorting
    for idx, player in enumerate(leaderboard_data):
        player['position'] = idx + 1
    
    response_data = {
        'rankings': leaderboard_data,
        'total_registered_players': len(leaderboard_data),
        'last_updated': datetime.now().isoformat()
    }
    return jsonify(response_data)

# Additional utility routes
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/stats')
def game_statistics():
    """Return general game statistics"""
    stats = {
        'world_size': GAME_WORLD_SIZE,
        'max_players': MAX_AI_PLAYERS,
        'food_capacity': TOTAL_FOOD_ITEMS,
        'player_speed': PLAYER_SPEED,
        'uptime': 'Unknown'  # Would be calculated in real implementation
    }
    return jsonify(stats)

if __name__ == '__main__':
    print(f"Starting game server on port 5000...")
    print(f"World size: {GAME_WORLD_SIZE}")
    print(f"Max AI players: {MAX_AI_PLAYERS}")
    app.run(host='0.0.0.0', port=5000, debug=True)