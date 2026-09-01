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

def is_row_in_table(event: Event):
    try:
        response: dict = (
                supabase.table("events")
                .select("*")
                .eq("title", event.get_title())
                .eq("start", event.get_start())
                .eq("building", event.get_building())
                .execute()
            )
        if not response.data:
            return False
        return True
    except Exception as e:
        print(f"Error while checking event in table: {e}")
        return False

def delete_specific_event(event: Event):
    response: dict = (
        supabase.table("events")
        .delete()
        .eq("source_url", event.source_url)
        .eq("poster", event.poster())
        .eq("title", event.get_title())
        .eq("start", event.get_start())
        .eq("end", event.get_end())
        .eq("building", event.get_building())
        .eq("url", event.get_url())
        .execute()
    )