import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

news_api_key = os.getenv("NEWS_API_KEY")
BASE_URL = 'https://newsapi.org/v2/everything'

def cerca_notizie_web(query):
    if not news_api_key:
        logging.error("Chiave API per NewsAPI non trovata!")
        return []

    params = {
        'q': query,
        'apiKey': news_api_key,
        'pageSize': 10     # Limita il numero di articoli
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()  # solleva eccezione se status_code non è 2xx

        dati = response.json()
        articoli = dati.get('articles', [])

        # Filtra solo campi essenziali per il tuo progetto
        articoli_filtrati = []
        for art in articoli:
            articoli_filtrati.append({
                'titolo': art.get('title', ''),
                'sottotitolo': art.get('description', ''),
                'testo': art.get('content', ''),
                'url': art.get('url', ''),
                'data_pubblicazione': art.get('publishedAt', '')
            })

        return articoli_filtrati

    except requests.exceptions.RequestException as e:
        logging.error(f"Errore nella chiamata a NewsAPI: {e}")
        return []
