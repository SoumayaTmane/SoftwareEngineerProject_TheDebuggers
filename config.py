import os
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = None

if url and key:
    try:
        from supabase import create_client
        supabase = create_client(url, key)
    except Exception as e:
        print(f"Supabase connection failed: {e}")
        supabase = None 

