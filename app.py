# ==========================================================
# FILE: app.py (Main Backend)
# ----------------------------------------------------------
# TEAM RESPONSIBILITIES:
# - Soumaya: Initializing Supabase, Flask, and Server setup.
# - EYERUH: Create the login function & Supabase query logic.
# - FAIZAN: Handle validation (errors)
# ==========================================================
import os
from dotenv import load_dotenv
from flask import Flask
from supabase import create_client, Client


app = Flask(__name__)

# This line loads the variables from the .env file
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

@app.route('/')
def home():
    """ This is the landing page. We can change this to the login later! """
    return "<h1>The Debuggers: Project Online</h1><p>Database Connection: ACTIVE</p>"

#Eyeruh' space




#Faizan's space



#starting server
if __name__ == '__main__':
    app.run(debug=True)