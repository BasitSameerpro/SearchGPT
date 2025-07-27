import os
import requests
import time
from dotenv import load_dotenv


# Load keys from env file
load_dotenv()
key = os.getenv("Brave_API")

def Brave_SERP(query,count=5) -> dict:
    url = 'https://api.search.brave.com/res/v1/web/search'
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": key
    }
    params = {
        'q':query,
        'count':count
    }
    links = []
    time.sleep(1) # I have added this because i am using brave search free api which only allows 1 request per sec. You can change it if you want
    response = requests.get(url,headers=headers,params=params)
    if response.status_code==200:
        results = response.json()
        for i,result in enumerate(results.get("web",{}).get('results',[]),1):
            link = {
                'num' : i,
                'title': result['title'],
                'url': result['url']
            }
            links.append(link)
        return links
        
    else:
        print(f"[Error Ocured]: {response.status_code}")
        print(response.text)