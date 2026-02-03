from checker import Checker, Event
from datetime import datetime, timedelta
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

def build_aaiscloud_calendar_url(days):
    pst = ZoneInfo("America/Los_Angeles")
    date = datetime.now(pst).replace(hour=0, minute=0, second=0, microsecond=0)
    end = date + timedelta(days=days)
    
    start_date = date.strftime("%Y-%m-%dT00:00:00")
    end_date = end.strftime("%Y-%m-%dT23:59:59")
    
    params = {
        'allowUnlimitedResults': 'true',
        'fields': (
            'ActivityId,ActivityName,StartDate,ActivityTypeCode,CampusName,'
            'BuildingCode,RoomNumber,LocationName,StartDateTime,EndDateTime,'
            'InstructorName:strjoin2(" ", " ", " "),'
            'Days:strjoin2(" ", " ", " "),'
            'CanView:strjoin2(" ", " ", " "),'
            'SectionId,EventId,'
            'EventImage:strjoin2(" ", " ", " "),'
            'ParentActivityId,ParentActivityName'
        ),
        'entityProps': '',
        '_s': '1',
        'filter': f"(((EventMeetingByActivityId.IsPrivate==0)&&(EventMeetingByActivityId.Event.IsPrivate==0))&&((ActivityTypeCode==2)&&(StartDateTime >= \"{start_date}\" && StartDateTime <= \"{end_date}\")))",
        'sortOrder': '+StartDateTime',
        'page': '1',
        'start': '0',
        # 'limit': '50',
        'sort': '[{"property":"StartDateTime","direction":"ASC"}]'
    }
    
    url = f"https://www.aaiscloud.com/UCAMerced/~api/calendar/activityList?{urlencode(params, safe=':,()\"')}"
    
    return url

def get_aaiscloud_headers():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.aaiscloud.com/UCAMerced/default.aspx',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    return headers

import requests
class AaiscloudChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "aaiscloud")
        self.session = requests.Session()
    
    async def check(self):
        url = build_aaiscloud_calendar_url(days=1)
        headers = get_aaiscloud_headers()
        response = self.session.get(url=url, headers=headers)
        response_json = response.json()
        data = response_json['data']

        for event in data:
            poster = event[17]
            title = event[1]
            start = event[8]
            end = event[9]
            building = event[7]
            id = event[0]
            url  = f"https://www.aaiscloud.com/UCAMerced/~api/hover/geteventcontentforeventmeeting/{id}"
            self.events.append(Event(
                source_url=self.source_url,
                source_type=self.source_type,
                poster=poster,
                title=title,
                start=start,
                end=end,
                building=building,
                url=url
            ))

# aaiscloud = AaiscloudChecker("hello")
# aaiscloud.check()
# events = aaiscloud.get_events()
# for event in events:
#     fields = [
#         event.poster,
#         event.title,
#         event.start,
#         event.end,
#         event.building,
#         event.url
#     ]
#     output = ", ".join(str(item) for item in fields if item)

#     print(output)