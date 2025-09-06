import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def genera_notizia_da_ai(prompt: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sei un giornalista sportivo. Scrivi la notizia in un formato semplice: la prima riga è il titolo, la seconda il sottotitolo e il resto è il testo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        testo_generato = response.choices[0].message.content
        sezioni = parse_articolo_flessibile(testo_generato)
        return {
            "titolo": sezioni.get("titolo", ""),
            "sottotitolo": sezioni.get("sottotitolo", ""),
            "testo": sezioni.get("testo", ""),
        }
    
    except openai.AuthenticationError:
        return {"titolo": "", "sottotitolo": "", "testo": "Errore di autenticazione: la chiave API non è valida."}
    
    except Exception as e:
        return {"titolo": "", "sottotitolo": "", "testo": f"Errore AI: {str(e)}"}



def parse_articolo_flessibile(testo_generato: str) -> dict:
    """
    Analizza il testo generato dall'AI in modo flessibile.
    Cerca il titolo nella prima riga, il sottotitolo nella seconda e il resto nel testo.
    """
    righe = [riga.strip() for riga in testo_generato.splitlines() if riga.strip()]
    
    titolo = righe[0] if len(righe) > 0 else ""
    sottotitolo = righe[1] if len(righe) > 1 else ""
    testo = " ".join(righe[2:]) if len(righe) > 2 else ""

    return {
        "titolo": titolo,
        "sottotitolo": sottotitolo,
        "testo": testo
    }


def genera_prompt_da_articoli(articoli_web: list[dict], articoli_manuali: list[dict], tema: str) -> str:
    
    def format_articoli(lista):
        testi = []
        for art in lista:
            testi.append(
                f"Titolo: {art.get('titolo', '')}\n"
                f"Sottotitolo: {art.get('sottotitolo', '')}\n"
                f"Testo: {art.get('testo', '')}\n"
            )
        return "\n\n---\n\n".join(testi)

    prompt = (
        f"Usa i seguenti articoli per scrivere una notizia sportiva professionale e accattivante sul tema '{tema}'. "
        "La notizia DEVE avere come focus principale il termine indicato nel tema e menzionarlo esplicitamente almeno una volta nel testo. "
        "La notizia deve essere chiara, sintetica e informativa, rivolta a un pubblico appassionato di sport. "
        "Scrivi la notizia nel formato richiesto: la prima riga è il titolo, la seconda il sottotitolo (deve essere sempre presente), e il resto è il corpo del testo.\n"
        "Il titolo non deve superare le 10 parole. Il sottotitolo deve essere una breve frase che approfondisce il titolo.\n" 
        "Il testo deve essere un riassunto conciso e dettagliato, massimo 500 caratteri.\n"
        "Evita ripetizioni e usa un linguaggio semplice e diretto.\n\n"
        "Articoli web:\n"
        f"{format_articoli(articoli_web)}\n\n"
        "Articoli manuali:\n"
        f"{format_articoli(articoli_manuali)}\n"
    )
    return prompt


def genera_notizia_da_articoli(articoli_web: list[dict], articoli_manuali: list[dict], tema: str = "") -> dict:

    # Se il tema non è fornito, lo fornisco dai titoli degli articoli
    if not tema:
        if articoli_web and articoli_web[0].get("titolo"):
            tema = articoli_web[0]["titolo"]
        elif articoli_manuali and articoli_manuali[0].get("titolo"):
            tema = articoli_manuali[0]["titolo"]

    prompt = genera_prompt_da_articoli(articoli_web, articoli_manuali, tema)
    return genera_notizia_da_ai(prompt)
