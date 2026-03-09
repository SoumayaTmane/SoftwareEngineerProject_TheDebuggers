# ==========================================================
# FILE: app.py (Main Backend)
# ----------------------------------------------------------
# TEAM RESPONSIBILITIES:
# - 
# ==========================================================
from flask import Flask, render_template, request, session, redirect, url_for
from auth import login_user

app = Flask(__name__)


app.secret_key = "debuggers_secret_key_2026" #used for flash mangment

@app.route('/')
def home():
    """ This is the landing page. We can change this to the login later! """
    return  render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    return login_user(request.form) 

@app.route('/dashboard')
def dashboard():
    
    if 'campus_id' in session:
        return f"Welcome to the Dashboard, {session['campus_id']}!"
    return redirect(url_for('home'))

#starting server
if __name__ == '__main__':
    app.run(debug=True)