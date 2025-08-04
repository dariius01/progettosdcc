import requests
from dotenv import load_dotenv
import os

load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")
BASE_URL = 'https://newsapi.org/v2/everything'

def cerca_notizie_web(query):
    params = {
        'q': query,
        'apiKey': news_api_key
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()['articles']
    return []
