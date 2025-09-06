import requests
import logging
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")
BASE_URL = 'https://newsapi.org/v2/everything'

def cerca_notizie_web(query):
    if not news_api_key:
        logging.error("Chiave API per NewsAPI non trovata!")
        return []

    # Pulizia e preparazione query
    terms = query.lower().split()
    query_phrase = f'"{query}"'
    query_and = " AND ".join(terms)
    final_query = f'{query_phrase} OR {query_and}'

    def fetch_news(days):
        params = {
            'q': final_query,
            'apiKey': news_api_key,
            'pageSize': 15,
            'language': 'it',
            'sortBy': 'relevancy',
            'searchIn': 'title,description',
            'from': (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json().get('articles', [])

    try:
        articoli = fetch_news(7)  
        if not articoli:
            articoli = fetch_news(30)  

        def è_rilevante(art):
            testo = f"{art.get('title', '')} {art.get('description', '')} {art.get('content', '')}".lower()
            return all(t in testo for t in terms)

        articoli_filtrati = [
            {
                'titolo': art.get('title', ''),
                'sottotitolo': art.get('description', ''),
                'testo': art.get('content', ''),
                'url': art.get('url', ''),
                'data_pubblicazione': art.get('publishedAt', ''),
                'source': art.get('source', {}).get('name', '')
            }
            for art in articoli if è_rilevante(art)
        ]

        return articoli_filtrati

    except requests.exceptions.RequestException as e:
        logging.error(f"Errore nella chiamata a NewsAPI: {e}")
        return []
