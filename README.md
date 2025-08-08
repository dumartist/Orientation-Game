# Terminal RPG - Adventure Awaits

A retro-style terminal CLI RPG game built with Python Flask and modern web technologies. Experience the nostalgia of classic text-based RPGs with a beautiful terminal-inspired interface.

## Features

- **Terminal CLI Theme**: Authentic retro terminal appearance with green text on black background
- **RPG Gameplay**: Level up, gain experience, collect gold, and battle enemies
- **Multiple Areas**: Explore Forest, Cave, and Dungeon with different enemies and loot
- **Quest System**: Accept and complete quests for rewards
- **Shop System**: Buy items and equipment
- **Real-time Updates**: Live game state updates and action feedback
- **Responsive Design**: Works on desktop and mobile devices

## Game Mechanics

### Player Stats
- **Level**: Increases with experience, unlocks new abilities
- **HP**: Health points, restored by resting (costs gold)
- **EXP**: Experience points, gained from battles and exploration
- **Gold**: Currency for buying items and resting
- **Inventory**: Items collected during adventures

### Areas to Explore
- **Dark Forest**: Goblin, Wolf, Bandit enemies
- **Ancient Cave**: Troll, Bat, Spider enemies  
- **Abandoned Dungeon**: Skeleton, Zombie, Dark Knight enemies

### Actions Available
- **Explore**: Visit different areas for encounters and loot
- **Rest**: Recover HP (costs 10 gold)
- **Shop**: Buy items and equipment
- **Quests**: Accept Goblin Hunt and Treasure Hunt quests

## Installation & Setup

### Option 1: Docker (Recommended)

#### Prerequisites
- Docker and Docker Compose installed

#### Quick Start with Docker

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd Orientation-Game
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Open your browser**
   Navigate to `http://localhost:5000` to start playing!

#### Docker Commands

```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Option 2: Local Python Installation

#### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

#### Installation Steps

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd Orientation-Game
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000` to start playing!

## How to Play

1. **Start Exploring**: Click "Explore Forest" to begin your adventure
2. **Battle Enemies**: When you encounter enemies, click the fight button
3. **Collect Loot**: Find items and gold during exploration
4. **Level Up**: Gain experience to increase your level and stats
5. **Complete Quests**: Accept quests for additional rewards
6. **Manage Resources**: Use gold wisely for resting and shopping

## Game Controls

- **Action Buttons**: Click to perform actions like exploring, fighting, or resting
- **Real-time Updates**: Game state updates automatically
- **Game Log**: View your adventure history in the left panel
- **Status Panel**: Monitor your stats, inventory, and active quests

## Technical Details

- **Backend**: Python Flask web framework
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: External CSS file with terminal-inspired theme and animations
- **Scripts**: External JavaScript file with game logic and UI functionality
- **Architecture**: RESTful API design with JSON responses
- **State Management**: Server-side game state with client-side UI updates
- **Code Organization**: Separated concerns with external CSS and JS files
- **Containerization**: Docker support with production and development configurations
- **Deployment**: Docker Compose for easy deployment and scaling

## File Structure

```
Orientation-Game/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main game interface
├── static/
│   ├── css/
│   │   └── style.css     # Terminal-themed styles
│   └── js/
│       └── game.js       # Game logic and UI functionality
├── music/                # Game music files
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Production Docker Compose setup

├── .dockerignore         # Docker build exclusions
└── README.md            # This file
```

## Contributing

Feel free to contribute to this project by:
- Adding new areas to explore
- Creating new enemy types
- Implementing additional game mechanics
- Improving the UI/UX
- Adding sound effects and music integration

## License

This project is open source and available under the MIT License.

---

**Ready to begin your adventure? Start the game and explore the mysterious world of Terminal RPG!**