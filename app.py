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
from flask import Flask, app
from supabase import create_client

app = Flask(__name__)

# This line loads the variables from the .env file
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

#Eyeruh' space




#Faizan's space

#starting server
if __name__ == '__main__':
    app.run(debug=True)