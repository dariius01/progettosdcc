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

    terms = query.split()  # divide la query in singole parole
    query_or = " OR ".join(terms)

    params = {
        'q': query_or, 
        'apiKey': news_api_key,
        'pageSize': 10,
        'language': 'it',
        'sortBy': 'relevancy',
        'searchIn': 'title,description',
        'from': (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()

        dati = response.json()
        articoli = dati.get('articles', [])

        articoli_filtrati = []
        for art in articoli:
            articoli_filtrati.append({
                'titolo': art.get('title', ''),
                'sottotitolo': art.get('description', ''),
                'testo': art.get('content', ''),
                'url': art.get('url', ''),
                'data_pubblicazione': art.get('publishedAt', ''),
                'source': art.get('source', {}).get('name', '')
            })

        return articoli_filtrati

    except requests.exceptions.RequestException as e:
        logging.error(f"Errore nella chiamata a NewsAPI: {e}")
        return []
