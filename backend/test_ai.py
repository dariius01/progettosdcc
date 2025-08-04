from ai import genera_notizia_da_ai 

if __name__ == "__main__":
    tema = "Federer"
    notizia = genera_notizia_da_ai(tema)
    print("Titolo:", notizia["titolo"])
    print("Sottotitolo:", notizia["sottotitolo"])
    print("Testo:", notizia["testo"])
