from dotenv import load_dotenv
from supabase import create_client, Client
from checker import Checker, Event
import os

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def add_to_database(events: list[Event], source_url: str, source_type: str):
    records = [
        {
            "source_url": source_url,
            "source_type": source_type,
            "poster": event.get_poster(),
            "title": event.get_title(),
            "start": event.get_start(),
            "end": event.get_end(),
            "building": event.get_building(),
            "url": event.get_url()
        }
        for event in events
    ]
    try:
        response = (
            supabase.table("events")
            .insert(records)
            .execute()
        )
        return f"Added {len(records)} events to database for {source_type} {source_url}"
    except Exception as e:
        return f"Error while adding events to table: {e}"

def delete_specific_rows(url: str):
    response: dict = (
        supabase.table("events")
        .delete()
        .eq("source_url", url)
        .execute()
    )