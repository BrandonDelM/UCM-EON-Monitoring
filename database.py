from dotenv import load_dotenv
from supabase import create_client, Client
import os

"""
Source_Url
Source_Type
Poster
Title
Start
End
Building
URL

"""

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def add_to_database():
    response = (
        supabase.table("events")
        .insert({
            "source_url": "",
            "source_type": "",
            "poster": "",
            "title": "",
            "start": "",
            "end": "",
            "building": "",
            "url": ""
        })
        .execute()
    )

def check_database_for_changes(url, updates):
    response: dict = (
        supabase.table("events")
        .select("source_url")
        .eq(url)
        .execute()
    )

    events = response.get("data")