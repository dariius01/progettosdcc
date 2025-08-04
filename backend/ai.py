import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def genera_notizia_da_ai(prompt: str) -> dict:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Sei un giornalista sportivo."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    testo_generato = response.choices[0].message.content

    sezioni = {"titolo": "", "sottotitolo": "", "testo": ""}
    for riga in testo_generato.splitlines():
        if riga.lower().startswith("titolo:"):
            sezioni["titolo"] = riga[7:].strip()
        elif riga.lower().startswith("sottotitolo:"):
            sezioni["sottotitolo"] = riga[12:].strip()
        elif riga.lower().startswith("testo:"):
            sezioni["testo"] = riga[6:].strip()

    return sezioni

def genera_prompt_da_articoli(articoli: list[dict], tema: str) -> str:
    testi = []
    for art in articoli:
        testo = (
            f"Titolo: {art.get('titolo', '')}\n"
            f"Sottotitolo: {art.get('sottotitolo', '')}\n"
            f"Testo: {art.get('testo', '')}\n"
        )
        testi.append(testo)

    testo_completo = "\n\n---\n\n".join(testi)
    prompt = (
        f"Usa i seguenti articoli per scrivere una notizia sportiva professionale e accattivante sul tema '{tema}'. "
        "La notizia deve essere chiara, sintetica e informativa, rivolta a un pubblico appassionato di sport. "
        "Segui questo formato preciso:\n"
        "Titolo: un titolo efficace e coinvolgente, massimo 10 parole\n"
        "Sottotitolo: una breve frase che approfondisce il titolo\n"
        "Testo: un riassunto dettagliato ma conciso, massimo 500 caratteri, che includa i fatti principali, "
        "le emozioni e un tocco di originalità.\n"
        "Evita ripetizioni e usa un linguaggio semplice e diretto.\n\n"
        f"Ecco gli articoli da cui attingere informazioni:\n\n{testo_completo}\n"
    )
    return prompt


def genera_notizia_da_articoli(articoli_web: list[dict], articoli_manuali: list[dict], tema: str) -> dict:
    tutti_articoli = articoli_web + articoli_manuali
    prompt = genera_prompt_da_articoli(tutti_articoli, tema)
    return genera_notizia_da_ai(prompt)
