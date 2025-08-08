from flask import Flask, render_template, request, jsonify, session
import os
import random
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Game state
class GameState:
    def __init__(self):
        self.player = {
            'name': 'Player',
            'level': 1,
            'hp': 100,
            'max_hp': 100,
            'exp': 0,
            'exp_to_next': 100,
            'gold': 50,
            'inventory': [],
            'location': 'town',
            'quests': []
        }
        self.game_log = []
        self.available_actions = []

# Initialize game state
game_state = GameState()

@app.route('/')
def index():
    """Main game interface"""
    return render_template('index.html')

@app.route('/api/game-state')
def get_game_state():
    """Get current game state"""
    return jsonify({
        'player': game_state.player,
        'game_log': game_state.game_log[-10:],  # Last 10 entries
        'available_actions': game_state.available_actions
    })

@app.route('/api/action', methods=['POST'])
def perform_action():
    """Handle player actions"""
    data = request.get_json()
    action = data.get('action', '')
    target = data.get('target', '')
    
    response = {'success': False, 'message': '', 'log_entry': ''}
    
    if action == 'explore':
        response = explore_area(target)
    elif action == 'fight':
        response = fight_enemy(target)
    elif action == 'rest':
        response = rest_player()
    elif action == 'shop':
        response = visit_shop()
    elif action == 'quest':
        response = accept_quest(target)
    
    if response['success']:
        game_state.game_log.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'message': response['log_entry'],
            'type': 'action'
        })
    
    return jsonify(response)

def explore_area(area):
    """Explore different areas"""
    areas = {
        'forest': {
            'name': 'Dark Forest',
            'enemies': ['Goblin', 'Wolf', 'Bandit'],
            'loot': ['Herb', 'Gold Coin', 'Rusty Sword'],
            'exp_gain': 10
        },
        'cave': {
            'name': 'Ancient Cave',
            'enemies': ['Troll', 'Bat', 'Spider'],
            'loot': ['Gem', 'Ancient Scroll', 'Magic Ring'],
            'exp_gain': 20
        },
        'dungeon': {
            'name': 'Abandoned Dungeon',
            'enemies': ['Skeleton', 'Zombie', 'Dark Knight'],
            'loot': ['Rare Weapon', 'Potion', 'Treasure'],
            'exp_gain': 30
        }
    }
    
    if area not in areas:
        return {'success': False, 'message': 'Unknown area', 'log_entry': ''}
    
    area_data = areas[area]
    enemy = random.choice(area_data['enemies'])
    loot = random.choice(area_data['loot'])
    exp_gain = area_data['exp_gain']
    
    # Random encounter
    if random.random() < 0.7:  # 70% chance of enemy encounter
        game_state.available_actions = [f'fight_{enemy.lower().replace(" ", "_")}']
        return {
            'success': True,
            'message': f'You encounter a {enemy}!',
            'log_entry': f'[EXPLORE] Found {enemy} in {area_data["name"]}'
        }
    else:
        # Found loot
        game_state.player['inventory'].append(loot)
        game_state.player['exp'] += exp_gain
        game_state.player['gold'] += random.randint(5, 15)
        
        # Level up check
        if game_state.player['exp'] >= game_state.player['exp_to_next']:
            level_up()
        
        return {
            'success': True,
            'message': f'You found {loot} and gained {exp_gain} EXP!',
            'log_entry': f'[EXPLORE] Found {loot} in {area_data["name"]} (+{exp_gain} EXP)'
        }

def fight_enemy(enemy_type):
    """Combat system"""
    enemies = {
        'goblin': {'hp': 30, 'damage': 10, 'exp': 15, 'gold': 10},
        'wolf': {'hp': 40, 'damage': 15, 'exp': 20, 'gold': 15},
        'bandit': {'hp': 50, 'damage': 20, 'exp': 25, 'gold': 20},
        'troll': {'hp': 80, 'damage': 25, 'exp': 40, 'gold': 30},
        'bat': {'hp': 25, 'damage': 8, 'exp': 12, 'gold': 8},
        'spider': {'hp': 35, 'damage': 12, 'exp': 18, 'gold': 12},
        'skeleton': {'hp': 60, 'damage': 22, 'exp': 35, 'gold': 25},
        'zombie': {'hp': 70, 'damage': 18, 'exp': 30, 'gold': 20},
        'dark_knight': {'hp': 100, 'damage': 30, 'exp': 50, 'gold': 40}
    }
    
    if enemy_type not in enemies:
        return {'success': False, 'message': 'Unknown enemy', 'log_entry': ''}
    
    enemy = enemies[enemy_type]
    enemy_hp = enemy['hp']
    
    # Simple combat simulation
    while enemy_hp > 0 and game_state.player['hp'] > 0:
        # Player attacks
        damage = random.randint(15, 25)
        enemy_hp -= damage
        
        # Enemy attacks back if still alive
        if enemy_hp > 0:
            enemy_damage = random.randint(enemy['damage'] - 5, enemy['damage'] + 5)
            game_state.player['hp'] -= enemy_damage
    
    if game_state.player['hp'] <= 0:
        # Player defeated
        game_state.player['hp'] = 1
        game_state.player['gold'] = max(0, game_state.player['gold'] - 10)
        return {
            'success': True,
            'message': 'You were defeated! Lost some gold and barely escaped.',
            'log_entry': f'[COMBAT] Defeated by {enemy_type.replace("_", " ").title()}'
        }
    else:
        # Victory
        game_state.player['exp'] += enemy['exp']
        game_state.player['gold'] += enemy['gold']
        
        # Level up check
        if game_state.player['exp'] >= game_state.player['exp_to_next']:
            level_up()
        
        return {
            'success': True,
            'message': f'Victory! Gained {enemy["exp"]} EXP and {enemy["gold"]} gold!',
            'log_entry': f'[COMBAT] Defeated {enemy_type.replace("_", " ").title()} (+{enemy["exp"]} EXP, +{enemy["gold"]} gold)'
        }

def rest_player():
    """Rest to restore HP"""
    cost = 10
    if game_state.player['gold'] >= cost:
        game_state.player['gold'] -= cost
        game_state.player['hp'] = game_state.player['max_hp']
        return {
            'success': True,
            'message': f'You rested and recovered all HP! Cost: {cost} gold',
            'log_entry': f'[REST] Recovered HP (-{cost} gold)'
        }
    else:
        return {
            'success': False,
            'message': 'Not enough gold to rest!',
            'log_entry': ''
        }

def visit_shop():
    """Shop system"""
    items = {
        'health_potion': {'name': 'Health Potion', 'cost': 20, 'effect': 'Restore 50 HP'},
        'sword': {'name': 'Iron Sword', 'cost': 100, 'effect': 'Increase damage'},
        'armor': {'name': 'Leather Armor', 'cost': 80, 'effect': 'Increase defense'}
    }
    
    return {
        'success': True,
        'message': 'Welcome to the shop!',
        'shop_items': items,
        'log_entry': '[SHOP] Visited the shop'
    }

def accept_quest(quest_id):
    """Quest system"""
    quests = {
        'goblin_hunt': {
            'name': 'Goblin Hunt',
            'description': 'Defeat 3 goblins',
            'reward': {'exp': 50, 'gold': 30},
            'target': 3,
            'progress': 0
        },
        'treasure_hunt': {
            'name': 'Treasure Hunt',
            'description': 'Find 5 treasures',
            'reward': {'exp': 75, 'gold': 50},
            'target': 5,
            'progress': 0
        }
    }
    
    if quest_id in quests:
        game_state.player['quests'].append(quests[quest_id])
        return {
            'success': True,
            'message': f'Quest accepted: {quests[quest_id]["name"]}',
            'log_entry': f'[QUEST] Accepted: {quests[quest_id]["name"]}'
        }
    else:
        return {
            'success': False,
            'message': 'Unknown quest',
            'log_entry': ''
        }

def level_up():
    """Handle player level up"""
    game_state.player['level'] += 1
    game_state.player['exp'] -= game_state.player['exp_to_next']
    game_state.player['exp_to_next'] = int(game_state.player['exp_to_next'] * 1.5)
    game_state.player['max_hp'] += 20
    game_state.player['hp'] = game_state.player['max_hp']
    
    game_state.game_log.append({
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'message': f'LEVEL UP! You are now level {game_state.player["level"]}!',
        'type': 'level_up'
    })

@app.route('/api/update-actions')
def update_actions():
    """Update available actions based on current location"""
    if game_state.player['location'] == 'town':
        game_state.available_actions = ['explore_forest', 'explore_cave', 'explore_dungeon', 'rest', 'shop', 'quest_goblin_hunt', 'quest_treasure_hunt']
    else:
        game_state.available_actions = ['return_to_town']
    
    return jsonify({'available_actions': game_state.available_actions})

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Get debug mode from environment variable
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
