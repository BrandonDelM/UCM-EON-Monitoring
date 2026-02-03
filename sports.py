from checker import Checker, Event
import requests

def get_sports_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }
    url = "https://ucmercedbobcats.com/services/archives.ashx/stories?index=1&page_size=30&sport=0&season=0"
    return headers, url
    # r = requests.get(url, headers=headers)
    # if r.status_code ==  200:
    #     response_json = r.json()
    #     return response_json['data']
    # return None

class SportsChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "sports")
    
    async def check(self):
        headers, url = get_sports_data()
        r = await self.get_request(url, headers=headers)
        if r.status_code == 200:
            response_json = r.json()
            data = response_json['data']
        else:
            return "Couldn't retrieve data for sports", 400

        for headline in data:
            poster = headline['sport_title'] if headline['sport_title'] else None
            title = headline['story_headline'] if headline['story_headline'] else None
            start = headline['story_postdate'] if headline['story_postdate'] else None
            path = headline['story_path'] if headline['story_path'] else None
            url = f"https://ucmercedbobcats.com{path}" if path else None
            self.events.append(Event(
                source_url=self.source_url,
                source_type=self.source_type,
                poster=poster,
                title=title,
                start=start,
                url=url
            ))