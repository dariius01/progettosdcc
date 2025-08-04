import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def genera_notizia_da_ai(tema: str) -> dict:
    prompt = (
        f"Scrivi una breve notizia sportiva su '{tema}' nel seguente formato:\n"
        "Titolo:\nSottotitolo:\nTesto (massimo 500 caratteri):"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "Sei un giornalista sportivo."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    testo_generato = response.choices[0].message.content

    # Split del testo nei tre campi (puoi adattare la logica)
    sezioni = {"titolo": "", "sottotitolo": "", "testo": ""}
    for riga in testo_generato.splitlines():
        if riga.lower().startswith("titolo:"):
            sezioni["titolo"] = riga[7:].strip()
        elif riga.lower().startswith("sottotitolo:"):
            sezioni["sottotitolo"] = riga[12:].strip()
        elif riga.lower().startswith("testo:"):
            sezioni["testo"] = riga[6:].strip()

    return sezioni
