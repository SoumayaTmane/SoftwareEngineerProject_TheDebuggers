# ==========================================================
# FILE: app.py (Main Backend)
# ----------------------------------------------------------
# TEAM RESPONSIBILITIES:
# - 
# ==========================================================
from flask import Flask, flash, render_template, request, session, redirect, url_for
from auth import login_user
from config import supabase

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
    # 1. THE SECURITY CHECK
    
    if 'campus_id' not in session:
        flash("Please log in to view the dashboard.")
        return redirect(url_for('home'))
    all_items = []
    all_buildings = []

    # 2. THE DATA FETCHING
    # we now go to Supabase.
    try:
        response = (
            supabase.table("post")
            .select("""*,  building(building_name), user_account!post_reporterid_fkey(f_name, l_name)""")
            .execute()
        )
        all_items = response.data
        
        build_res = supabase.table("building").select("buildingid, building_name").execute()
        all_buildings = build_res.data
    except Exception as e:
        print(f"Error fetching data: {e}")
        

    # 3. THE RENDERING
    # We send the items to the  dashboard.html template.
    return render_template('dashboard.html', items=all_items, buildings=all_buildings)

@app.route('/report-item', methods=['POST'])
def report_item():
    # 1. Who is logged in?
    user_id = session.get('campus_id')
    
    if not user_id:
        return redirect(url_for('home'))

    # 2. Get the info from the modal form
    new_post = {
        "item_name": request.form.get('item_name'),
        "description": request.form.get('description'),
        "buildingid": int(request.form.get('building_id')), 
        "reporterid": user_id,  # This links the post to the user account!
        "status": request.form.get('status')
    }

    # 3. Save to Supabase
    try:
        supabase.table("post").insert(new_post).execute()
        # A success message for the dashboard
        return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"Error inserting post: {e}")
        return "There was an error saving your report.", 500

# This route allows users to delete a post. Only staff can delete any post, while students can only delete their own posts.
@app.route('/delete-post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    user_id = session.get('campus_id')
    user_role = session.get('role')

    if not user_id:
        return redirect(url_for('home'))

    try:
        if user_role == 'staff':
            supabase.table("post").delete().eq("postid", post_id).execute()
        else:
            supabase.table("post").delete().eq("postid", post_id).eq("reporterid", user_id).execute()
        
        flash("Post successfully deleted!", "success") 
    except Exception as e:
        print(f"Delete error: {e}")
        flash("Error deleting post.", "danger")
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear() # This wipes the campus_id and role from the session
    
    return redirect(url_for('home')) # Sends them back to the login page


#starting server
if __name__ == '__main__':
    app.run(debug=True)