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
        

    pass

# def is_change(table, events):
    # new = []

    # create_table(table)
    
    # table_items = get_all_rows_from_table(table)
    # if not table_items:
    #     add_many_to_table(events,table)
    #     return events

    # table_set = set(table_items) if table_items else set()

    # for event in events:
    #     if event not in table_set:
    #         new.append(event)
    # return new

# def log_changes(table, events):
#     create_table(table)
    
#     clear_table(table)
#     add_many_to_table(events,table)

def database_format(poster="", title="", start="", end="", building="", link=""):
    return (poster,title,start,end,building,link)