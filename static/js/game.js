let gameState = {
    player: {
        name: 'Anomaly',
        level: 1,
        hp: 100,
        max_hp: 100,
        exp: 0,
        exp_to_next: 100,
        credits: 50,
        inventory: [],
        location: 'nexis',
        quests: [],
        skills: {
            decryption: 1,
            manipulation: 1,
            reconstruction: 1
        },
        reputation: {
            codekeepers: 0,
            resistance: 0,
            neutral: 0
        }
    },
    game_log: [],
    available_actions: [],
    current_stage: 1,
    story_progress: []
};

// Initialize game
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing game...');
    loadGameState();
    updateActions();
});

async function loadGameState() {
    try {
        console.log('Loading game state...');
        const response = await fetch('/api/game-state');
        const data = await response.json();
        console.log('Game state loaded:', data);
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
    console.log('Updating UI...');
    
    // Check if Action Panel is visible
    const actionPanel = document.querySelector('.action-panel');
    console.log('Action Panel found:', !!actionPanel);
    if (actionPanel) {
        console.log('Action Panel styles:', {
            display: actionPanel.style.display,
            visibility: actionPanel.style.visibility,
            width: actionPanel.offsetWidth,
            height: actionPanel.offsetHeight
        });
    }
    
    // Update player stats
    document.getElementById('playerName').textContent = gameState.player.name;
    document.getElementById('playerLevel').textContent = gameState.player.level;
    document.getElementById('playerHP').textContent = `${gameState.player.hp}/${gameState.player.max_hp}`;
    document.getElementById('playerEXP').textContent = `${gameState.player.exp}/${gameState.player.exp_to_next}`;
    document.getElementById('playerCredits').textContent = gameState.player.credits;

    // Update skills
    if (gameState.player.skills) {
        document.getElementById('playerDecryption').textContent = gameState.player.skills.decryption || 1;
        document.getElementById('playerManipulation').textContent = gameState.player.skills.manipulation || 1;
        document.getElementById('playerReconstruction').textContent = gameState.player.skills.reconstruction || 1;
    }

    // Update reputation
    if (gameState.player.reputation) {
        document.getElementById('playerCodekeepers').textContent = gameState.player.reputation.codekeepers || 0;
        document.getElementById('playerResistance').textContent = gameState.player.reputation.resistance || 0;
        document.getElementById('playerNeutral').textContent = gameState.player.reputation.neutral || 0;
    }

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
    console.log('Updating story UI, current stage:', gameState.current_stage);
    const storyStages = {
        1: {
            title: 'The Awakening',
            description: 'You wake up in a sterile white room. The air hums with digital energy. You are in Nexis, the hidden heart of the Source.',
            choices: {
                a: 'Trust Lira and embrace your role',
                b: 'Question everything about this place',
                c: 'Focus on learning the three pillars',
                d: 'Investigate the whispers of corruption'
            }
        },
        2: {
            title: 'The Trials Begin',
            description: 'You are pitted against other recruits in digital trials. The shifting labyrinths of code test your abilities.',
            choices: {
                a: 'Focus on personal advancement',
                b: 'Build alliances with questioning recruits',
                c: 'Use your skills to help others',
                d: 'Sabotage the trials subtly'
            }
        },
        3: {
            title: 'The Revelation',
            description: 'Your investigation leads you to the Sanctum, the system\'s core. Here you find the Grand Code - the master program governing human consciousness.',
            choices: {
                a: 'Embrace the power of the Grand Code',
                b: 'Expose the truth to all humanity',
                c: 'Seek a third path - subtle reform',
                d: 'Destroy the Grand Code entirely'
            }
        },
        4: {
            title: 'The Final Choice',
            description: 'You stand before the Grand Code, the fate of reality in your hands. Your decision will determine the future of humanity.',
            choices: {
                a: 'The Collapse - Restore Freedom',
                b: 'The New Order - Seize Control',
                c: 'The Balance - Find Middle Ground',
                d: 'The Anomaly - Reject All Systems'
            }
        }
    };

    if (gameState.current_stage === 'complete') {
        document.getElementById('storyTitle').textContent = '🎉 STORY COMPLETE! 🎉';
        document.getElementById('storyDescription').textContent = 'Congratulations! You have completed your journey through The Codebound Chronicles. Your choices have shaped the future of reality itself.';
        document.getElementById('storyChoices').innerHTML = '<button class="story-btn" style="background-color: #ff8800; border-color: #ff8800; color: #000; font-weight: bold; font-size: 14px;" onclick="restartGame()">🎮 RESTART ADVENTURE</button>';
    } else if (storyStages[gameState.current_stage]) {
        const stage = storyStages[gameState.current_stage];
        console.log('Setting stage:', stage);
        
        const storyTitleElement = document.getElementById('storyTitle');
        const storyDescriptionElement = document.getElementById('storyDescription');
        const storyChoicesElement = document.getElementById('storyChoices');
        
        console.log('Story elements found:', {
            storyTitle: !!storyTitleElement,
            storyDescription: !!storyDescriptionElement,
            storyChoices: !!storyChoicesElement
        });
        
        if (storyTitleElement) storyTitleElement.textContent = stage.title;
        if (storyDescriptionElement) storyDescriptionElement.textContent = stage.description;
        
        const choicesHTML = Object.entries(stage.choices).map(([key, text]) => 
            `<button class="story-btn" onclick="performAction('story_choice', '${key}')">${key.toUpperCase()}) ${text}</button>`
        ).join('');
        
        console.log('Setting choices HTML:', choicesHTML);
        if (storyChoicesElement) storyChoicesElement.innerHTML = choicesHTML;
    }
}

async function restartGame() {
    // Show confirmation dialog
    if (!confirm('Are you sure you want to restart your adventure? This will reset all progress and start from the beginning.')) {
        return;
    }
    
    const messageBox = document.getElementById('messageBox');
    messageBox.innerHTML = '<div class="loading"></div> Restarting...';

    try {
        const response = await fetch('/api/restart-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const result = await response.json();
        
        if (result.success) {
            // Update the client-side game state with the server response
            gameState = result.game_state;
            messageBox.textContent = result.message;
            updateUI();
        } else {
            messageBox.textContent = result.message || 'Failed to restart game!';
        }
    } catch (error) {
        console.error('Error restarting game:', error);
        messageBox.textContent = 'Error restarting game!';
    }
}

// Save/Load functions
async function saveGame() {
    const saveName = document.getElementById('saveName').value.trim() || 
                   `Game Save ${new Date().toLocaleString()}`;
    
    const messageBox = document.getElementById('messageBox');
    messageBox.innerHTML = '<div class="loading"></div> Saving...';

    try {
        const response = await fetch('/api/save-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ save_name: saveName })
        });

        const result = await response.json();
        
        if (result.success) {
            messageBox.textContent = result.message;
            document.getElementById('saveName').value = '';
            await loadGameState();
        } else {
            messageBox.textContent = result.message || 'Failed to save game!';
        }
    } catch (error) {
        console.error('Error saving game:', error);
        messageBox.textContent = 'Error saving game!';
    }
}

async function showLoadMenu() {
    await listSaves();
    const saveList = document.getElementById('saveList');
    saveList.style.display = saveList.style.display === 'none' ? 'block' : 'none';
}

async function listSaves() {
    try {
        const response = await fetch('/api/list-saves');
        const result = await response.json();
        
        if (result.success) {
            displaySaveList(result.saves);
        } else {
            console.error('Failed to list saves');
        }
    } catch (error) {
        console.error('Error listing saves:', error);
    }
}

function displaySaveList(saves) {
    const saveList = document.getElementById('saveList');
    
    if (saves.length === 0) {
        saveList.innerHTML = '<div class="save-item">No save files found</div>';
        return;
    }

    const savesHTML = saves.map(save => {
        const saveDate = new Date(save.save_date).toLocaleString();
        return `
            <div class="save-item">
                <div class="save-item-header">
                    <span class="save-item-name">${save.save_name}</span>
                    <span class="save-item-date">${saveDate}</span>
                </div>
                <div class="save-item-details">
                    <span class="save-item-level">Level ${save.player_level}</span>
                    <span class="save-item-stage">Stage ${save.current_stage}</span>
                </div>
                <div class="save-item-actions">
                    <button class="save-item-btn" onclick="loadSave('${save.save_id}')">Load</button>
                    <button class="save-item-btn delete" onclick="deleteSave('${save.save_id}')">Delete</button>
                </div>
            </div>
        `;
    }).join('');

    saveList.innerHTML = savesHTML;
}

async function loadSave(saveId) {
    const messageBox = document.getElementById('messageBox');
    messageBox.innerHTML = '<div class="loading"></div> Loading...';

    try {
        const response = await fetch('/api/load-game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ save_id: saveId })
        });

        const result = await response.json();
        
        if (result.success) {
            messageBox.textContent = result.message;
            gameState = result.game_state;
            updateUI();
            document.getElementById('saveList').style.display = 'none';
        } else {
            messageBox.textContent = result.message || 'Failed to load game!';
        }
    } catch (error) {
        console.error('Error loading game:', error);
        messageBox.textContent = 'Error loading game!';
    }
}

async function deleteSave(saveId) {
    if (!confirm('Are you sure you want to delete this save file?')) {
        return;
    }

    try {
        const response = await fetch('/api/delete-save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ save_id: saveId })
        });

        const result = await response.json();
        
        if (result.success) {
            await listSaves(); // Refresh the save list
        } else {
            console.error('Failed to delete save:', result.message);
        }
    } catch (error) {
        console.error('Error deleting save:', error);
    }
}

// Auto-refresh game state every 5 seconds
setInterval(loadGameState, 5000);
