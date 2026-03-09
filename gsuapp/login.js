// ===================================
// GSU LOST & FOUND - LOGIN VALIDATION
// ===================================

// Get form elements
const loginForm = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const loginButton = document.getElementById('loginButton');
const buttonText = document.getElementById('buttonText');
const loadingSpinner = document.getElementById('loadingSpinner');

// Get error message elements
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const emailError = document.getElementById('emailError');
const passwordError = document.getElementById('passwordError');

// ===================================
// VALIDATION FUNCTIONS
// ===================================

/**
 * Validate email format
 * Ensures it's a GSU email (@gsu.edu)
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@gsu\.edu$/i;
    return emailRegex.test(email);
}

/**
 * Check if field is empty
 */
function isEmpty(value) {
    return value.trim() === '';
}

/**
 * Show field-specific error
 */
function showFieldError(inputElement, errorElement, message) {
    inputElement.classList.add('error');
    errorElement.textContent = message;
    errorElement.classList.add('show');
}

/**
 * Clear field-specific error
 */
function clearFieldError(inputElement, errorElement) {
    inputElement.classList.remove('error');
    errorElement.textContent = '';
    errorElement.classList.remove('show');
}

/**
 * Show generic error message (prevents user enumeration)
 */
function showGenericError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideGenericError();
    }, 5000);
}

/**
 * Hide generic error message
 */
function hideGenericError() {
    errorMessage.style.display = 'none';
    errorText.textContent = '';
}

/**
 * Show loading state on button
 */
function showLoading() {
    loginButton.disabled = true;
    buttonText.style.display = 'none';
    loadingSpinner.style.display = 'inline-block';
}

/**
 * Hide loading state on button
 */
function hideLoading() {
    loginButton.disabled = false;
    buttonText.style.display = 'inline';
    loadingSpinner.style.display = 'none';
}

// ===================================
// REAL-TIME VALIDATION (As user types)
// ===================================

emailInput.addEventListener('input', () => {
    clearFieldError(emailInput, emailError);
    hideGenericError();
});

passwordInput.addEventListener('input', () => {
    clearFieldError(passwordInput, passwordError);
    hideGenericError();
});

// ===================================
// FORM SUBMISSION HANDLER
// ===================================

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Clear previous errors
    clearFieldError(emailInput, emailError);
    clearFieldError(passwordInput, passwordError);
    hideGenericError();
    
    // Get form values
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    
    let hasError = false;
    
    // ===================================
    // VALIDATION STEP 1: Check for empty fields
    // ===================================
    
    if (isEmpty(email) && isEmpty(password)) {
        showGenericError('Please fill in all fields.');
        showFieldError(emailInput, emailError, 'Email is required');
        showFieldError(passwordInput, passwordError, 'Password is required');
        return;
    }
    
    if (isEmpty(email)) {
        showGenericError('Please fill in all fields.');
        showFieldError(emailInput, emailError, 'Email is required');
        hasError = true;
    }
    
    if (isEmpty(password)) {
        showGenericError('Please fill in all fields.');
        showFieldError(passwordInput, passwordError, 'Password is required');
        hasError = true;
    }
    
    if (hasError) return;
    
    // ===================================
    // VALIDATION STEP 2: Validate email format
    // ===================================
    
    if (!validateEmail(email)) {
        showFieldError(emailInput, emailError, 'Please enter a valid GSU email (@student.gsu.edu)');
        return;
    }
    
    // ===================================
    // VALIDATION STEP 3: Attempt login with Supabase
    // ===================================
    
    try {
        showLoading();
        
        // Call your Supabase authentication function here
        const result = await authenticateUser(email, password);
        
        if (result.success) {
            // Successful login - redirect to dashboard
            window.location.href = 'dashboard.html';
        } else {
            // Failed login - show GENERIC error (prevents user enumeration)
            showGenericError('Invalid username or password. Please try again.');
            hideLoading();
        }
        
    } catch (error) {
        // Network or server error
        showGenericError('An error occurred. Please try again later.');
        console.error('Login error:', error);
        hideLoading();
    }
});

// ===================================
// SUPABASE AUTHENTICATION FUNCTION
// ===================================

/**
 * Authenticate user with Supabase
 * Replace this with your actual Supabase code
 */
async function authenticateUser(email, password) {
    // TODO: Replace with actual Supabase authentication
    
    /* EXAMPLE SUPABASE CODE:
    
    const { data, error } = await supabase.auth.signInWithPassword({
        email: email,
        password: password
    });
    
    if (error) {
        return { success: false, error: error.message };
    }
    
    return { success: true, user: data.user };
    
    */
    
    // TEMPORARY MOCK FOR TESTING
    return new Promise((resolve) => {
        setTimeout(() => {
            // Simulate failed login for demo
            resolve({ success: false });
        }, 1500);
    });
}

// ===================================
// REMEMBER ME FUNCTIONALITY (Optional)
// ===================================

const rememberMeCheckbox = document.getElementById('rememberMe');

// Load saved email on page load
window.addEventListener('DOMContentLoaded', () => {
    const savedEmail = localStorage.getItem('rememberedEmail');
    if (savedEmail) {
        emailInput.value = savedEmail;
        rememberMeCheckbox.checked = true;
    }
});

// Save email when form is submitted successfully
function saveEmailIfRemembered() {
    if (rememberMeCheckbox.checked) {
        localStorage.setItem('rememberedEmail', emailInput.value);
    } else {
        localStorage.removeItem('rememberedEmail');
    }
}

// ===================================
// KEYBOARD ACCESSIBILITY
// ===================================

// Allow Enter key to submit from any input field
emailInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        loginForm.dispatchEvent(new Event('submit'));
    }
});

passwordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        loginForm.dispatchEvent(new Event('submit'));
    }
});
