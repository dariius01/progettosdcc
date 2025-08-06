from ai import genera_notizia_da_articoli

if __name__ == "__main__":
    tema = "Federer vince a Wimbledon"

    articoli_web = [
        {
            "titolo": "Federer trionfa ancora",
            "sottotitolo": "Lo svizzero conquista il suo 9º titolo",
            "testo": "Roger Federer ha battuto il suo avversario in tre set, confermandosi ancora una volta campione."
        }
    ]

    articoli_manuali = [
        {
            "titolo": "Federer leggenda",
            "sottotitolo": "Un altro trionfo per il re dell'erba",
            "testo": "Federer continua a scrivere la storia del tennis con una prestazione impeccabile."
        }
    ]

    notizia = genera_notizia_da_articoli(articoli_web, articoli_manuali, tema)

    print("TITOLO:", notizia["titolo"])
    print("SOTTOTITOLO:", notizia["sottotitolo"])
    print("TESTO:", notizia["testo"])
    # print("GREZZO:", notizia["testo_grezzo"])  # Se vuoi vedere il risultato completo dell'AI
