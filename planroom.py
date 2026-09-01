import requests
from icalendar import Calendar
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv("PLAN_TOKEN")
COOKIE = os.getenv("PLAN_COOKIE")

url = f"https://www.ucmplanroom.com/projects/ical.ics?jwt={TOKEN}"
session = requests.Session()
session.cookies.set("__Secure-PHPSESSID", COOKIE, domain="www.ucmplanroom.com")
r = session.get(url)
cal = Calendar.from_ical(r.text)
for event in cal.walk("VEVENT"):
    poster = event.get("ORGANIZER")

    poster = str(poster).replace("MAILTO:", "") if poster is not None else None

    title = event.get("SUMMARY")
    title = str(title).strip() if title is not None else None

    start = event.get("DTSTART")
    start = start.dt.isoformat() if start else None

    end = event.get("DTEND")
    end = end.dt.isoformat() if end else None

    building = event.get("LOCATION")
    building = str(building).strip() if building is not None else None

    url = event.get("URL")
    url = str(url).strip() if url is not None else None

    print(poster, title, start, end, building, url)