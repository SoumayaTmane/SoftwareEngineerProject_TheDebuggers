from flask import flash, redirect, url_for, session
from config import supabase

def login_user(form_data):
    # 1. Match the 'name' attribute from  HTML
    campus_id = form_data.get("campus_id") 
    password = form_data.get("password")

    if not campus_id or not password:
        flash("Please enter both CampusID and Password.")
        return redirect(url_for('home'))

    # 2. Search Supabase for the user
    user = supabase.table("user_account").select("*").eq("campusid", campus_id).execute()

    if not user.data:
        flash("Invalid CampusID or Password.")
        return redirect(url_for('home'))

    # 3. Verify the password 
    stored_password = user.data[0]["password"]
    #
    if password == stored_password:
        session['user_id'] = user.data[0]['campusid']
        session['campus_id'] = campus_id
        session['role'] = user.data[0]['role']
        return redirect(url_for('dashboard'))
    else:
        flash("Invalid CampusID or Password.")
        return redirect(url_for('home'))