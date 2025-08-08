// Authentication form handlers
document.addEventListener('DOMContentLoaded', function() {
    // Login form handler
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const npm = document.getElementById('npm').value.trim();
            const messageDiv = document.getElementById('message');
            
            if (!npm) {
                messageDiv.textContent = 'Please enter your NPM';
                messageDiv.className = 'error-message';
                return;
            }
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ npm: npm })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    messageDiv.textContent = result.message;
                    messageDiv.className = 'success-message';
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1000);
                } else {
                    messageDiv.textContent = result.message;
                    messageDiv.className = 'error-message';
                }
            } catch (error) {
                messageDiv.textContent = 'Connection error. Please try again.';
                messageDiv.className = 'error-message';
            }
        });
    }
    
    // Register form handler
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value.trim();
            const npm = document.getElementById('npm').value.trim();
            const messageDiv = document.getElementById('message');
            
            if (!username || !npm) {
                messageDiv.textContent = 'Please fill in all fields';
                messageDiv.className = 'error-message';
                return;
            }
            
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        username: username,
                        npm: npm 
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    messageDiv.textContent = result.message;
                    messageDiv.className = 'success-message';
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 2000);
                } else {
                    messageDiv.textContent = result.message;
                    messageDiv.className = 'error-message';
                }
            } catch (error) {
                messageDiv.textContent = 'Connection error. Please try again.';
                messageDiv.className = 'error-message';
            }
        });
    }
});
