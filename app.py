# ==========================================================
# FILE: app.py (Main Backend)
# ----------------------------------------------------------
# TEAM RESPONSIBILITIES:
# - Soumaya: Initializing Supabase, Flask, and Server setup.
# - EYERUH: Create the login function & Supabase query logic.
# - FAIZAN: Handle validation (errors)
# ==========================================================
import os
import secrets
import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# This line loads the variables from the .env file
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def hash_password(password):
    """Hash a password using werkzeug"""
    return generate_password_hash(password)

def check_password(password, stored_hash):
    """Check if password matches stored hash"""
    return check_password(stored_hash, password)

def generate_reset_token():
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

# ==========================================================
# LOGIN FUNCTION (Eyeruh's Space)
# ==========================================================

def login_user(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Invalid credentials"}), 400

    user = supabase.table("users").select("*").eq("username", username).execute()

    if not user.data:
        return jsonify({"error": "Invalid credentials"}), 401

    stored_hash = user.data[0]["password_hash"]

    if check_password(password, stored_hash):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# ==========================================================
# PASSWORD RESET API ENDPOINTS (New Feature)
# ==========================================================

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    """
    Endpoint to request password reset
    Sends reset link to user's email (GSU email)
    """
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # Check if user exists
    user = supabase.table("users").select("*").eq("email", email).execute()
    
    if not user.data:
        # Return generic message for security (don't reveal if email exists)
        return jsonify({"message": "If your email is registered, you will receive a password reset link."}), 200
    
    # Generate reset token and expiry (valid for 1 hour)
    reset_token = generate_reset_token()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    
    # Store token in database
    supabase.table("users").update({
        "reset_token": reset_token,
        "reset_token_expires_at": expires_at.isoformat()
    }).eq("email", email).execute()
    
    # For development, we'll return the reset link in response
    reset_link = f"{request.host_url}reset-password.html?token={reset_token}&email={email}"
    
    print(f"Password reset link: {reset_link}")
    
    # In production, you would send an actual email here
    return jsonify({
        "message": "Password reset link has been sent to your email.",
        "reset_link": reset_link  # Remove this line in production!
    }), 200

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    """
    Endpoint to reset password using token
    """
    data = request.get_json()
    email = data.get('email')
    token = data.get('token')
    new_password = data.get('new_password')
    
    # Validate inputs
    if not email or not token or not new_password:
        return jsonify({"error": "All fields are required"}), 400
    
    # Validate password strength
    if len(new_password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400
    
    # Find user with valid reset token
    user = supabase.table("users").select("*").eq("email", email).eq("reset_token", token).execute()
    
    if not user.data:
        return jsonify({"error": "Invalid or expired reset token"}), 400
    
    user_data = user.data[0]
    
    # Check if token expired
    expires_at = datetime.datetime.fromisoformat(user_data.get('reset_token_expires_at'))
    if expires_at < datetime.datetime.utcnow():
        return jsonify({"error": "Reset token has expired. Please request a new one."}), 400
    
    # Hash new password and update
    new_password_hash = hash_password(new_password)
    
    supabase.table("users").update({
        "password_hash": new_password_hash,
        "reset_token": None,
        "reset_token_expires_at": None
    }).eq("email", email).execute()
    
    return jsonify({"message": "Password has been reset successfully!"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    """API endpoint for login"""
    data = request.get_json()
    return login_user(data)

# ==========================================================
# FRONTEND ROUTES
# ==========================================================

@app.route('/')
def home():
    """Landing page"""
    return "<h1>The Debuggers: Project Online</h1><p>Database Connection: ACTIVE</p>"

@app.route('/login.html')
def login_page():
    """Serve login page"""
    return app.send_static_file('login.html')

@app.route('/forgot-password.html')
def forgot_password_page():
    """Serve forgot password page"""
    return app.send_static_file('forgot-password.html')

@app.route('/reset-password.html')
def reset_password_page():
    """Serve reset password page"""
    return app.send_static_file('reset-password.html')

# ==========================================================
# STARTING SERVER
# ==========================================================

if __name__ == '__main__':
    app.run(debug=True)