# The Codebound Chronicles - Terminal RPG

A cyberpunk-themed terminal CLI RPG game built with Python Flask and modern web technologies. Experience a branching narrative set in the year 2125 where reality is just a program and you are an Anomaly with the power to see through the digital facade.

## Features

- **Cyberpunk Terminal Theme**: Authentic retro terminal appearance with green text on black background
- **Branching Story RPG**: Experience "The Codebound Chronicles" with multiple story paths and endings
- **Skill System**: Master Decryption, Manipulation, and Reconstruction abilities
- **Reputation System**: Build relationships with Codekeepers, Resistance, or remain Neutral
- **Save/Load System**: Persistent game saves using JSON files
- **Real-time Updates**: Live game state updates and action feedback
- **Responsive Design**: Works on desktop and mobile devices

## Game Mechanics

### Player Stats
- **Level**: Increases with experience, unlocks new abilities
- **HP**: Health points, represents your digital integrity
- **EXP**: Experience points, gained from story choices and revelations
- **Credits**: Digital currency for transactions in the Source
- **Inventory**: Items and evidence collected during your journey

### Skills System
- **Decryption**: Unlock secrets hidden within the Source
- **Manipulation**: Rewrite the code of objects and environments
- **Reconstruction**: Rebuild corrupted data and fragmented memories

### Reputation System
- **Codekeepers**: Your standing with the ruling organization
- **Resistance**: Your connection to those who question the system
- **Neutral**: Your reputation among independent factions

### Story Stages
- **Stage 1**: The Awakening - Your arrival in Nexis
- **Stage 2**: The Trials Begin - Digital challenges and alliances
- **Stage 3**: The Revelation - Discovering the Grand Code
- **Stage 4**: The Final Choice - Determining the future of reality

### Multiple Endings
- **The Collapse**: Restore freedom but face chaos
- **The New Order**: Seize control as the new architect
- **The Balance**: Find a middle path between order and chaos
- **The Anomaly**: Reject all systems and become truly free

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

1. **Registration/Login**: First, register with your username and NPM, then login to access the game
2. **Begin Your Journey**: Start with "The Awakening" and choose your path
3. **Make Story Choices**: Each decision affects your skills, reputation, and story progression
4. **Build Your Character**: Develop your skills in Decryption, Manipulation, and Reconstruction
5. **Choose Your Allegiance**: Build reputation with Codekeepers, Resistance, or remain Neutral
6. **Discover the Truth**: Uncover the secrets of the Source and the Grand Code
7. **Determine the Future**: Make the final choice that will shape reality itself
8. **Save Your Progress**: Use the save/load system to continue your adventure later

## Game Controls

- **Story Choice Buttons**: Click to make story decisions that affect your journey
- **Real-time Updates**: Game state updates automatically
- **Game Log**: View your adventure history and story progression
- **Status Panel**: Monitor your stats, skills, reputation, and inventory
- **Save/Load System**: Save your progress and load previous games
- **Restart Adventure**: Start a fresh journey at any time or after completing the story

## Technical Details

- **Backend**: Python Flask web framework
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: External CSS file with cyberpunk terminal-inspired theme and animations
- **Scripts**: External JavaScript file with game logic and UI functionality
- **Architecture**: RESTful API design with JSON responses
- **State Management**: Server-side game state with client-side UI updates
- **Story System**: Branching narrative with multiple paths and endings
- **Save System**: JSON-based persistent save files with Docker volume support
- **Code Organization**: Separated concerns with external CSS and JS files
- **Containerization**: Docker support with production configuration
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
- Adding new story branches and endings
- Creating new skills and abilities
- Implementing additional reputation mechanics
- Improving the UI/UX
- Adding sound effects and music integration
- Expanding the cyberpunk world and lore

## License

This project is open source and available under the MIT License.

---

**Ready to begin your journey? Start the game and discover the truth behind The Codebound Chronicles!**