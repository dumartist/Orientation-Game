let gameState = {
    player: {
        name: 'Player',
        level: 1,
        hp: 100,
        max_hp: 100,
        exp: 0,
        exp_to_next: 100,
        gold: 50,
        inventory: [],
        location: 'start',
        quests: []
    },
    game_log: [],
    available_actions: [],
    current_stage: 1,
    story_progress: []
};

// Initialize game
document.addEventListener('DOMContentLoaded', function() {
    loadGameState();
    updateActions();
});

async function loadGameState() {
    try {
        const response = await fetch('/api/game-state');
        const data = await response.json();
        gameState = data;
        updateUI();
    } catch (error) {
        console.error('Error loading game state:', error);
    }
}

async function performAction(action, target = '') {
    const messageBox = document.getElementById('messageBox');
    messageBox.innerHTML = '<div class="loading"></div> Loading...';

    try {
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action, target })
        });

        const result = await response.json();
        
        if (result.success) {
            messageBox.textContent = result.message;
            await loadGameState();
            updateActions();
        } else {
            messageBox.textContent = result.message || 'Action failed!';
        }
    } catch (error) {
        console.error('Error performing action:', error);
        messageBox.textContent = 'Error performing action!';
    }
}

async function updateActions() {
    try {
        const response = await fetch('/api/update-actions');
        const data = await response.json();
        gameState.available_actions = data.available_actions;
    } catch (error) {
        console.error('Error updating actions:', error);
    }
}

        function updateUI() {
            // Update player stats
            document.getElementById('playerName').textContent = gameState.player.name;
            document.getElementById('playerLevel').textContent = gameState.player.level;
            document.getElementById('playerHP').textContent = `${gameState.player.hp}/${gameState.player.max_hp}`;
            document.getElementById('playerEXP').textContent = `${gameState.player.exp}/${gameState.player.exp_to_next}`;
            document.getElementById('playerGold').textContent = gameState.player.gold;

            // Update HP bar
            const hpPercentage = (gameState.player.hp / gameState.player.max_hp) * 100;
            document.getElementById('hpBar').style.width = `${hpPercentage}%`;

            // Update EXP bar
            const expPercentage = (gameState.player.exp / gameState.player.exp_to_next) * 100;
            document.getElementById('expBar').style.width = `${expPercentage}%`;

            // Update inventory
            const inventoryList = document.getElementById('inventoryList');
            if (gameState.player.inventory.length === 0) {
                inventoryList.innerHTML = '<div class="inventory-item">Empty</div>';
            } else {
                inventoryList.innerHTML = gameState.player.inventory.map(item => 
                    `<div class="inventory-item">${item}</div>`
                ).join('');
            }

            // Update quests
            const questList = document.getElementById('questList');
            if (gameState.player.quests.length === 0) {
                questList.innerHTML = '<div class="quest-item">No active quests</div>';
            } else {
                questList.innerHTML = gameState.player.quests.map(quest => 
                    `<div class="quest-item">
                        <div class="quest-name">${quest.name}</div>
                        <div class="quest-description">${quest.description}</div>
                        <div class="quest-progress">Progress: ${quest.progress}/${quest.target}</div>
                    </div>`
                ).join('');
            }

            // Update story elements
            updateStoryUI();

            // Update game log
            const gameLog = document.getElementById('gameLog');
            gameLog.innerHTML = gameState.game_log.map(entry => {
                const timestamp = entry.timestamp ? `<span class="log-entry timestamp">[${entry.timestamp}]</span> ` : '';
                const className = entry.type ? `log-entry ${entry.type}` : 'log-entry';
                return `<div class="${className}">${timestamp}${entry.message}</div>`;
            }).join('');
            
            gameLog.scrollTop = gameLog.scrollHeight;
        }

        function updateStoryUI() {
            const storyStages = {
                1: {
                    title: 'The Awakening',
                    description: 'You wake up in a mysterious cave. What do you do?',
                    choices: {
                        a: 'Explore the cave carefully',
                        b: 'Rush out of the cave',
                        c: 'Search for supplies',
                        d: 'Meditate and rest'
                    }
                },
                2: {
                    title: 'The Crossroads',
                    description: 'You emerge from the cave to find three paths. Which do you take?',
                    choices: {
                        a: 'Take the forest path',
                        b: 'Follow the river',
                        c: 'Climb the mountain',
                        d: 'Return to the cave'
                    }
                },
                3: {
                    title: 'The Challenge',
                    description: 'Your journey continues. What challenge do you face?',
                    choices: {
                        a: 'Solve the ancient puzzle',
                        b: 'Fight the guardian',
                        c: 'Negotiate peacefully',
                        d: 'Use stealth'
                    }
                },
                4: {
                    title: 'The Final Choice',
                    description: 'You reach the heart of the adventure. What is your destiny?',
                    choices: {
                        a: 'Become a legendary hero',
                        b: 'Seek ultimate power',
                        c: 'Find inner peace',
                        d: 'Return home changed'
                    }
                }
            };

            if (gameState.current_stage === 'complete') {
                document.getElementById('storyTitle').textContent = 'Story Complete!';
                document.getElementById('storyDescription').textContent = 'You have completed your journey.';
                document.getElementById('storyChoices').innerHTML = '<button class="story-btn" onclick="restartGame()">Restart Adventure</button>';
            } else if (storyStages[gameState.current_stage]) {
                const stage = storyStages[gameState.current_stage];
                document.getElementById('storyTitle').textContent = stage.title;
                document.getElementById('storyDescription').textContent = stage.description;
                
                const choicesHTML = Object.entries(stage.choices).map(([key, text]) => 
                    `<button class="story-btn" onclick="performAction('story_choice', '${key}')">${key.toUpperCase()}) ${text}</button>`
                ).join('');
                
                document.getElementById('storyChoices').innerHTML = choicesHTML;
            }
        }

        function restartGame() {
            // Reset game state
            gameState = {
                player: {
                    name: 'Player',
                    level: 1,
                    hp: 100,
                    max_hp: 100,
                    exp: 0,
                    exp_to_next: 100,
                    gold: 50,
                    inventory: [],
                    location: 'start',
                    quests: []
                },
                game_log: [],
                available_actions: [],
                current_stage: 1,
                story_progress: []
            };
            
            updateUI();
        }

// Auto-refresh game state every 5 seconds
setInterval(loadGameState, 5000);
