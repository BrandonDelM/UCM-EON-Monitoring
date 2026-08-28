from dotenv import load_dotenv
import os
import requests
import json

url = "https://api.short.io/api/links?domain_id=199414&limit=50"

load_dotenv()
authorization = os.getenv("SHORTURL")
headers = {
    "accept": "application/json",
    "Authorization": authorization
}

response = requests.get(url, headers=headers)

# print(json.loads(response.text)['links'])
links = json.loads(response.text)['links']
for link in links:
    print(link['originalURL'])