from flask import Flask, render_template, request, jsonify, session
import os
import random
import json
from datetime import datetime
import uuid

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
            'location': 'start',
            'quests': []
        }
        self.game_log = []
        self.available_actions = []
        self.current_stage = 1
        self.story_progress = []
        self.save_id = None
        self.save_name = None
        self.save_date = None

    def to_dict(self):
        """Convert game state to dictionary for JSON serialization"""
        return {
            'player': self.player,
            'game_log': self.game_log,
            'available_actions': self.available_actions,
            'current_stage': self.current_stage,
            'story_progress': self.story_progress,
            'save_id': self.save_id,
            'save_name': self.save_name,
            'save_date': self.save_date
        }

    def from_dict(self, data):
        """Load game state from dictionary"""
        self.player = data.get('player', self.player)
        self.game_log = data.get('game_log', [])
        self.available_actions = data.get('available_actions', [])
        self.current_stage = data.get('current_stage', 1)
        self.story_progress = data.get('story_progress', [])
        self.save_id = data.get('save_id')
        self.save_name = data.get('save_name')
        self.save_date = data.get('save_date')

# Initialize game state
game_state = GameState()

# Save file management
SAVE_DIR = 'saves'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_save_file_path(save_id):
    """Get the file path for a save file"""
    return os.path.join(SAVE_DIR, f'{save_id}.json')

def save_game_to_file(save_name):
    """Save current game state to a JSON file"""
    save_id = str(uuid.uuid4())
    save_data = game_state.to_dict()
    save_data['save_id'] = save_id
    save_data['save_name'] = save_name
    save_data['save_date'] = datetime.now().isoformat()
    
    file_path = get_save_file_path(save_id)
    try:
        with open(file_path, 'w') as f:
            json.dump(save_data, f, indent=2)
        return save_id
    except Exception as e:
        print(f"Error saving game: {e}")
        return None

def load_game_from_file(save_id):
    """Load game state from a JSON file"""
    file_path = get_save_file_path(save_id)
    try:
        with open(file_path, 'r') as f:
            save_data = json.load(f)
        game_state.from_dict(save_data)
        return True
    except Exception as e:
        print(f"Error loading game: {e}")
        return False

def get_all_saves():
    """Get list of all available save files"""
    saves = []
    if os.path.exists(SAVE_DIR):
        for filename in os.listdir(SAVE_DIR):
            if filename.endswith('.json'):
                save_id = filename[:-5]  # Remove .json extension
                file_path = get_save_file_path(save_id)
                try:
                    with open(file_path, 'r') as f:
                        save_data = json.load(f)
                    saves.append({
                        'save_id': save_id,
                        'save_name': save_data.get('save_name', 'Unknown'),
                        'save_date': save_data.get('save_date', ''),
                        'player_level': save_data.get('player', {}).get('level', 1),
                        'current_stage': save_data.get('current_stage', 1)
                    })
                except Exception as e:
                    print(f"Error reading save file {filename}: {e}")
    return saves

def delete_save_file(save_id):
    """Delete a save file"""
    file_path = get_save_file_path(save_id)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"Error deleting save file: {e}")
    return False

@app.route('/')
def index():
    """Main game interface"""
    return render_template('index.html')

@app.route('/api/game-state')
def get_game_state():
    """Get current game state"""
    return jsonify({
        'player': game_state.player,
        'game_log': game_state.game_log[-20:],  # Last 20 entries
        'available_actions': game_state.available_actions,
        'current_stage': game_state.current_stage,
        'story_progress': game_state.story_progress
    })

@app.route('/api/action', methods=['POST'])
def perform_action():
    """Handle player actions"""
    data = request.get_json()
    action = data.get('action', '')
    target = data.get('target', '')
    
    response = {'success': False, 'message': '', 'log_entry': ''}
    
    if action == 'story_choice':
        response = make_story_choice(target)
    elif action == 'explore':
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

def make_story_choice(choice):
    """Handle story choices and branching narratives"""
    story_stages = {
        1: {
            'title': 'The Awakening',
            'description': 'You wake up in a mysterious cave. What do you do?',
            'choices': {
                'a': {
                    'text': 'Explore the cave carefully',
                    'outcome': 'You find ancient markings and gain 20 EXP',
                    'exp_gain': 20,
                    'gold_gain': 10,
                    'next_stage': 2
                },
                'b': {
                    'text': 'Rush out of the cave',
                    'outcome': 'You escape quickly but trip and lose 10 HP',
                    'hp_loss': 10,
                    'exp_gain': 5,
                    'next_stage': 2
                },
                'c': {
                    'text': 'Search for supplies',
                    'outcome': 'You find a health potion and some gold',
                    'item_gain': 'Health Potion',
                    'gold_gain': 25,
                    'exp_gain': 15,
                    'next_stage': 2
                },
                'd': {
                    'text': 'Meditate and rest',
                    'outcome': 'You feel refreshed and gain wisdom',
                    'hp_gain': 20,
                    'exp_gain': 10,
                    'next_stage': 2
                }
            }
        },
        2: {
            'title': 'The Crossroads',
            'description': 'You emerge from the cave to find three paths. Which do you take?',
            'choices': {
                'a': {
                    'text': 'Take the forest path',
                    'outcome': 'You enter a dark forest filled with mystery',
                    'exp_gain': 25,
                    'location_change': 'forest',
                    'next_stage': 3
                },
                'b': {
                    'text': 'Follow the river',
                    'outcome': 'You discover a peaceful village by the water',
                    'exp_gain': 20,
                    'gold_gain': 30,
                    'location_change': 'village',
                    'next_stage': 3
                },
                'c': {
                    'text': 'Climb the mountain',
                    'outcome': 'You find a dragon\'s lair and must fight!',
                    'exp_gain': 50,
                    'enemy_encounter': 'dragon',
                    'next_stage': 3
                },
                'd': {
                    'text': 'Return to the cave',
                    'outcome': 'You find a hidden passage you missed before',
                    'exp_gain': 15,
                    'item_gain': 'Ancient Key',
                    'next_stage': 3
                }
            }
        },
        3: {
            'title': 'The Challenge',
            'description': 'Your journey continues. What challenge do you face?',
            'choices': {
                'a': {
                    'text': 'Solve the ancient puzzle',
                    'outcome': 'Your intelligence helps you unlock a treasure',
                    'exp_gain': 40,
                    'gold_gain': 100,
                    'item_gain': 'Magic Scroll',
                    'next_stage': 4
                },
                'b': {
                    'text': 'Fight the guardian',
                    'outcome': 'A fierce battle awaits you',
                    'exp_gain': 60,
                    'enemy_encounter': 'guardian',
                    'next_stage': 4
                },
                'c': {
                    'text': 'Negotiate peacefully',
                    'outcome': 'Your diplomacy skills pay off',
                    'exp_gain': 30,
                    'gold_gain': 50,
                    'alliance_gain': 'guardian',
                    'next_stage': 4
                },
                'd': {
                    'text': 'Use stealth',
                    'outcome': 'You sneak past unnoticed',
                    'exp_gain': 25,
                    'stealth_bonus': True,
                    'next_stage': 4
                }
            }
        },
        4: {
            'title': 'The Final Choice',
            'description': 'You reach the heart of the adventure. What is your destiny?',
            'choices': {
                'a': {
                    'text': 'Become a legendary hero',
                    'outcome': 'You choose the path of greatness',
                    'exp_gain': 100,
                    'title_gain': 'Legendary Hero',
                    'ending': 'hero'
                },
                'b': {
                    'text': 'Seek ultimate power',
                    'outcome': 'Power comes with a price...',
                    'exp_gain': 150,
                    'dark_power': True,
                    'ending': 'dark_lord'
                },
                'c': {
                    'text': 'Find inner peace',
                    'outcome': 'You discover true wisdom',
                    'exp_gain': 80,
                    'wisdom_gain': True,
                    'ending': 'sage'
                },
                'd': {
                    'text': 'Return home changed',
                    'outcome': 'You bring knowledge back to your people',
                    'exp_gain': 60,
                    'knowledge_gain': True,
                    'ending': 'teacher'
                }
            }
        }
    }
    
    if game_state.current_stage not in story_stages:
        return {'success': False, 'message': 'Story complete!', 'log_entry': ''}
    
    stage_data = story_stages[game_state.current_stage]
    if choice not in stage_data['choices']:
        return {'success': False, 'message': 'Invalid choice!', 'log_entry': ''}
    
    choice_data = stage_data['choices'][choice]
    
    # Apply choice effects
    if 'exp_gain' in choice_data:
        game_state.player['exp'] += choice_data['exp_gain']
    if 'gold_gain' in choice_data:
        game_state.player['gold'] += choice_data['gold_gain']
    if 'hp_loss' in choice_data:
        game_state.player['hp'] = max(1, game_state.player['hp'] - choice_data['hp_loss'])
    if 'hp_gain' in choice_data:
        game_state.player['hp'] = min(game_state.player['max_hp'], game_state.player['hp'] + choice_data['hp_gain'])
    if 'item_gain' in choice_data:
        game_state.player['inventory'].append(choice_data['item_gain'])
    if 'location_change' in choice_data:
        game_state.player['location'] = choice_data['location_change']
    
    # Check for level up
    if game_state.player['exp'] >= game_state.player['exp_to_next']:
        level_up()
    
    # Record story progress
    game_state.story_progress.append({
        'stage': game_state.current_stage,
        'choice': choice,
        'outcome': choice_data['outcome']
    })
    
    # Move to next stage or end
    if 'next_stage' in choice_data:
        game_state.current_stage = choice_data['next_stage']
    elif 'ending' in choice_data:
        game_state.current_stage = 'complete'
    
    return {
        'success': True,
        'message': choice_data['outcome'],
        'log_entry': f'[STORY] {choice_data["outcome"]}',
        'next_stage': game_state.current_stage if game_state.current_stage != 'complete' else None,
        'ending': choice_data.get('ending', None)
    }

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
    """Update available actions based on current stage"""
    if game_state.current_stage == 'complete':
        game_state.available_actions = ['restart_game']
    else:
        game_state.available_actions = ['story_choice_a', 'story_choice_b', 'story_choice_c', 'story_choice_d']
    
    return jsonify({'available_actions': game_state.available_actions})

@app.route('/api/save-game', methods=['POST'])
def save_game():
    """Save current game state"""
    data = request.get_json()
    save_name = data.get('save_name', f'Game Save {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    
    save_id = save_game_to_file(save_name)
    if save_id:
        game_state.save_id = save_id
        game_state.save_name = save_name
        game_state.save_date = datetime.now().isoformat()
        
        game_state.game_log.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'message': f'Game saved as "{save_name}"',
            'type': 'save'
        })
        
        return jsonify({
            'success': True,
            'message': f'Game saved successfully as "{save_name}"',
            'save_id': save_id
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to save game'
        })

@app.route('/api/load-game', methods=['POST'])
def load_game():
    """Load a saved game"""
    data = request.get_json()
    save_id = data.get('save_id')
    
    if not save_id:
        return jsonify({
            'success': False,
            'message': 'No save ID provided'
        })
    
    if load_game_from_file(save_id):
        game_state.game_log.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'message': f'Game loaded: {game_state.save_name}',
            'type': 'load'
        })
        
        return jsonify({
            'success': True,
            'message': f'Game loaded successfully: {game_state.save_name}',
            'game_state': game_state.to_dict()
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to load game'
        })

@app.route('/api/list-saves')
def list_saves():
    """Get list of all available save files"""
    saves = get_all_saves()
    return jsonify({
        'success': True,
        'saves': saves
    })

@app.route('/api/delete-save', methods=['POST'])
def delete_save():
    """Delete a save file"""
    data = request.get_json()
    save_id = data.get('save_id')
    
    if not save_id:
        return jsonify({
            'success': False,
            'message': 'No save ID provided'
        })
    
    if delete_save_file(save_id):
        return jsonify({
            'success': True,
            'message': 'Save file deleted successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to delete save file'
        })

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Get debug mode from environment variable
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
