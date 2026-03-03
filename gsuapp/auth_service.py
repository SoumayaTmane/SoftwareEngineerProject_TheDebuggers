from flask import jsonify
from config import supabase
from utils.security import check_password

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