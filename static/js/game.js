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
        location: 'town',
        quests: []
    },
    game_log: [],
    available_actions: []
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

    // Update game log
    const gameLog = document.getElementById('gameLog');
    gameLog.innerHTML = gameState.game_log.map(entry => {
        const timestamp = entry.timestamp ? `<span class="log-entry timestamp">[${entry.timestamp}]</span> ` : '';
        const className = entry.type ? `log-entry ${entry.type}` : 'log-entry';
        return `<div class="${className}">${timestamp}${entry.message}</div>`;
    }).join('');
    
    gameLog.scrollTop = gameLog.scrollHeight;
}

// Auto-refresh game state every 5 seconds
setInterval(loadGameState, 5000);
