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
    query_phrase = f'"{query}"'  # frase esatta tra virgolette
    query_and = " AND ".join(terms)  # tutte le parole devono comparire

    final_query = f'{query_phrase} OR {query_and}'

    params = {
        'q': final_query,
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

        # Filtro di rilevanza generico: l'articolo deve contenere tutti i termini
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
