from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Notizia
from services import cerca_notizie_web
from ai import genera_notizia_da_articoli
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()  

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Recupera tutte le notizie
@app.route('/api/notizie', methods=['GET'])
def get_notizie():
    try:
        notizie = Notizia.query.all()
        if not notizie:
            return jsonify({"messaggio": "Nessuna notizia trovata"}), 404
        return jsonify([n.to_dict() for n in notizie])
    except Exception as e:
        return jsonify({"errore": f"Errore interno: {str(e)}"}), 500


# Recupera una notizia specifica per ID
@app.route('/api/notizie/<int:id>', methods=['GET'])
def get_notizia(id):
    try:
        notizia = Notizia.query.get(id)
        if not notizia:
            return jsonify({"errore": "Notizia non trovata"}), 404
        return jsonify(notizia.to_dict())
    except Exception as e:
        return jsonify({"errore": f"Errore interno: {str(e)}"}), 500


#Elimina notizia
@app.route('/api/notizie/<int:id>', methods=['DELETE'])
def elimina_notizia(id):
    notizia = Notizia.query.get(id)
    if not notizia:
        return jsonify({"errore": "Notizia non trovata"}), 404
    try:
        db.session.delete(notizia)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Errore durante l'eliminazione: {str(e)}"}), 500
    return jsonify({"success": True, "message": "Notizia eliminata"})

# Modifica una notizia (facoltativo)
@app.route('/api/notizie/<int:id>', methods=['PUT'])
def modifica_notizia(id):
    notizia = Notizia.query.get(id)
    if not notizia:
        return jsonify({"errore": "Notizia non trovata"}), 404
    
    try:
        dati = request.get_json()
        if not dati:
            return jsonify({"errore": "Dati JSON non validi"}), 400
        
        notizia.titolo = dati.get('titolo', notizia.titolo)
        notizia.sottotitolo = dati.get('sottotitolo', notizia.sottotitolo)
        notizia.testo = dati.get('testo', notizia.testo)
        db.session.commit()
        return jsonify({"messaggio": "Notizia aggiornata"})
    except Exception as e:
        return jsonify({"errore": "Errore durante l'aggiornamento della notizia", "dettagli": str(e)}), 500

# Genera una notizia 
@app.route('/api/genera-notizia', methods=['POST'])
def genera_notizia_da_articoli_route():
    dati = request.get_json()
    articoli_web = dati.get("articoli_web", [])
    articoli_manuali = dati.get("articoli_manuali", [])
    tema = dati.get("tema", "")

    articolo_generato = genera_notizia_da_articoli(articoli_web, articoli_manuali, tema)

    # Non salva più la notizia, ma ritorna solo i dati generati
    return jsonify(articolo_generato), 200

@app.route('/api/salva-notizia', methods=['POST'])
def salva_notizia_route():
    dati = request.get_json()
    titolo = dati.get("titolo", "")
    sottotitolo = dati.get("sottotitolo", "")
    testo = dati.get("testo", "")

    if not titolo or not testo:
        return jsonify({"errore": "Titolo e testo sono obbligatori"}), 400

    nuova_notizia = Notizia(
        titolo=titolo,
        sottotitolo=sottotitolo,
        testo=testo
    )
    db.session.add(nuova_notizia)
    db.session.commit()

    return jsonify(nuova_notizia.to_dict()), 201

@app.route('/api/ricerca-notizie', methods=['GET'])
def ricerca_notizie():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"errore": "Parametro 'q' mancante"}), 400

    try:
        risultati = cerca_notizie_web(query)
        return jsonify(risultati)
    except Exception as e:
        return jsonify({"errore": "Errore nella ricerca delle notizie", "dettagli": str(e)}), 500




"""@app.route('/api/aggiungi-articolo', methods=['POST'])
def aggiungi_articolo():
    dati = request.get_json()
    nuova = Notizia(
        nome=dati.get('nome'),
        titolo=dati.get('titolo'),
        sottotitolo=dati.get('sottotitolo'),
        testo=dati.get('testo')
    )
    db.session.add(nuova)
    db.session.commit()
    return jsonify(nuova.to_dict()), 201
"""

if __name__ == '__main__':
    print("🚀 Avvio server Flask...")
    app.run(debug=True, host='0.0.0.0', port=5000)
