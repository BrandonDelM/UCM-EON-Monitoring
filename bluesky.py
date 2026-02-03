from dotenv import load_dotenv
from atproto import Client
from checker import Checker, Event
import os

load_dotenv()

def init_bluesky_client():
    client = Client()
    identifier = os.getenv("BLUESKY_IDENTIFIER")
    password = os.getenv("BLUESKY_PASSWORD")
    client.login(identifier, password)
    return client

def get_bluesky_feed(client):
    data = client.app.bsky.feed.get_feed({
        'feed': 'at://did:plc:s4isflup5rbcyn7rkm6o64wv/app.bsky.feed.generator/aaajx5bhjuexc',
        'limit': 30,
    }, headers={'Accept-Language': 'en'})
    
    return data

def construct_bluesky_url(post):
    try:
        did = post.post.author.did
    except:
        return None
    
    try:
        rkey = post.post.uri.split("/")[-1]
    except:
        return None
    url = f"https://bsky.app/profile/{did}/post/{rkey}" if rkey and did is not None else None
    return url

class BlueskyChecker(Checker):
    def __init__(self, source_url):
        super().__init__(source_url, "bluesky")
    
    async def check(self):
        client: Client = init_bluesky_client()
        data = get_bluesky_feed(client)
        feed = data.feed
        seen = set()
        for post in feed:
            url  = construct_bluesky_url(post)
            if url in seen:
                continue
            seen.add(url)
            
            poster = post.post.author.handle.strip()
            title = f"{post.post.record.text.replace('\n',' ')}"
            start = post.post.record.created_at
            
            self.events.append(Event(
                source_url=self.source_url,
                source_type=self.source_type,
                poster=poster,
                title=title,
                start=start,
                url=url
            ))

# bluesky = BlueskyChecker("https://bsky.app/profile/starringon.bsky.social/feed/aaajx5bhjuexc")
# bluesky.check()
# events = bluesky.get_events()
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