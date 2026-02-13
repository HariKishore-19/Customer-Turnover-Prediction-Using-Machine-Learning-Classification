document.addEventListener('DOMContentLoaded', function() {
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const loginMessage = document.getElementById('loginMessage');
    const signupMessage = document.getElementById('signupMessage');

    // Toggle between login and signup forms
    signUpButton.addEventListener('click', () => {
        container.classList.add('right-panel-active');
    });

    signInButton.addEventListener('click', () => {
        container.classList.remove('right-panel-active');
    });

    // Login form submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        // Clear previous messages
        loginMessage.textContent = '';
        loginMessage.className = 'message';
        
        // Simple validation
        if (!email || !password) {
            showMessage(loginMessage, 'Please fill in all fields', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showMessage(loginMessage, 'Please enter a valid email address', 'error');
            return;
        }
        
        // Simulate API call
        simulateLogin(email, password);
    });

    // Signup form submission
    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('signupName').value;
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('signupPassword').value;
        const confirmPassword = document.getElementById('signupConfirmPassword').value;
        
        // Clear previous messages
        signupMessage.textContent = '';
        signupMessage.className = 'message';
        
        // Validation
        if (!name || !email || !password || !confirmPassword) {
            showMessage(signupMessage, 'Please fill in all fields', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showMessage(signupMessage, 'Please enter a valid email address', 'error');
            return;
        }
        
        if (password.length < 6) {
            showMessage(signupMessage, 'Password must be at least 6 characters long', 'error');
            return;
        }
        
        if (password !== confirmPassword) {
            showMessage(signupMessage, 'Passwords do not match', 'error');
            return;
        }
        
        // Simulate API call
        simulateSignup(name, email, password);
    });

    // Email validation function
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Show message function
    function showMessage(element, message, type) {
        element.textContent = message;
        element.className = `message ${type}`;
    }

    // Simulate login API call
    function simulateLogin(email, password) {
        // Show loading state
        const loginBtn = loginForm.querySelector('button[type="submit"]');
        const originalText = loginBtn.textContent;
        loginBtn.textContent = 'Signing In...';
        loginBtn.disabled = true;
        
        // Simulate API delay
        setTimeout(() => {
            // Check if user exists in localStorage
            const users = JSON.parse(localStorage.getItem('users')) || [];
            const user = users.find(u => u.email === email && u.password === password);
            
            if (user) {
                showMessage(loginMessage, 'Login successful! Redirecting...', 'success');
                
                // Store user session
                sessionStorage.setItem('currentUser', JSON.stringify(user));
                
                // Redirect to dashboard after delay
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1500);
            } else {
                showMessage(loginMessage, 'Invalid email or password', 'error');
            }
            
            // Reset button
            loginBtn.textContent = originalText;
            loginBtn.disabled = false;
        }, 1500);
    }

    // Simulate signup API call
    function simulateSignup(name, email, password) {
        // Show loading state
        const signupBtn = signupForm.querySelector('button[type="submit"]');
        const originalText = signupBtn.textContent;
        signupBtn.textContent = 'Creating Account...';
        signupBtn.disabled = true;
        
        // Simulate API delay
        setTimeout(() => {
            // Check if user already exists
            const users = JSON.parse(localStorage.getItem('users')) || [];
            const userExists = users.some(u => u.email === email);
            
            if (userExists) {
                showMessage(signupMessage, 'User with this email already exists', 'error');
                signupBtn.textContent = originalText;
                signupBtn.disabled = false;
                return;
            }
            
            // Create new user
            const newUser = {
                id: Date.now(),
                name: name,
                email: email,
                password: password,
                createdAt: new Date().toISOString()
            };
            
            // Save to localStorage
            users.push(newUser);
            localStorage.setItem('users', JSON.stringify(users));
            
            showMessage(signupMessage, 'Account created successfully! Please sign in.', 'success');
            
            // Clear form
            signupForm.reset();
            
            // Switch to login form after delay
            setTimeout(() => {
                container.classList.remove('right-panel-active');
            }, 2000);
            
            // Reset button
            signupBtn.textContent = originalText;
            signupBtn.disabled = false;
        }, 1500);
    }

    // Forgot password functionality
    document.querySelector('.forgot-password').addEventListener('click', function(e) {
        e.preventDefault();
        const email = prompt('Please enter your email to reset password:');
        if (email && isValidEmail(email)) {
            alert(`Password reset instructions have been sent to ${email}`);
        } else if (email) {
            alert('Please enter a valid email address');
        }
    });
});