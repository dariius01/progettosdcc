import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
def genera_notizia_da_ai(prompt: str) -> dict:
    try:
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
        sezioni = parse_articolo(testo_generato)
        return {
            "titolo": sezioni["titolo"],
            "sottotitolo": sezioni["sottotitolo"],
            "testo": sezioni["testo"],
            "testo_grezzo": testo_generato  # qui il testo completo
        }
    except Exception as e:
        return {"titolo": "", "sottotitolo": "", "testo": f"Errore AI: {str(e)}"}

    
def parse_articolo(testo_generato: str) -> dict:
    sezioni = {"titolo": "", "sottotitolo": "", "testo": ""}
    current_section = None

    for riga in testo_generato.splitlines():
        riga_strip = riga.strip()
        if riga_strip.lower().startswith("titolo:"):
            current_section = "titolo"
            sezioni[current_section] = riga_strip[7:].strip()
        elif riga_strip.lower().startswith("sottotitolo:"):
            current_section = "sottotitolo"
            sezioni[current_section] = riga_strip[12:].strip()
        elif riga_strip.lower().startswith("testo:"):
            current_section = "testo"
            sezioni[current_section] = riga_strip[6:].strip()
        elif current_section:
            # Aggiungi righe multilinea alla sezione corrente
            sezioni[current_section] += " " + riga_strip

    # Optional: strip finale per pulire spazi residui
    for key in sezioni:
        sezioni[key] = sezioni[key].strip()

    return sezioni


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
        "La notizia deve essere chiara, sintetica e informativa, rivolta a un pubblico appassionato di sport. "
        "Segui questo formato preciso:\n"
        "Titolo: un titolo efficace e coinvolgente, massimo 10 parole\n"
        "Sottotitolo: una breve frase che approfondisce il titolo\n"
        "Testo: un riassunto dettagliato ma conciso, massimo 500 caratteri, che includa i fatti principali, "
        "le emozioni e un tocco di originalità.\n"
        "Evita ripetizioni e usa un linguaggio semplice e diretto.\n\n"

        "Articoli web:\n"
        f"{format_articoli(articoli_web)}\n\n"

        "Articoli manuali:\n"
        f"{format_articoli(articoli_manuali)}\n"
    )
    return prompt


def genera_notizia_da_articoli(articoli_web: list[dict], articoli_manuali: list[dict], tema: str) -> dict:
    prompt = genera_prompt_da_articoli(articoli_web, articoli_manuali, tema)
    return genera_notizia_da_ai(prompt)
