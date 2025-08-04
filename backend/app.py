from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Notizia
from services import cerca_notizie_web
from ai import genera_notizia_da_articoli
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
db.init_app(app)

load_dotenv()  # carica le variabili da .env

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Recupera tutte le notizie
@app.route('/api/notizie', methods=['GET'])
def get_notizie():
    notizie = Notizia.query.all()
    return jsonify([n.to_dict() for n in notizie])

# Recupera una notizia specifica per ID
@app.route('/api/notizie/<int:notizia_id>', methods=['GET'])
def get_notizia(notizia_id):
    notizia = Notizia.query.get(id)
    if not notizia:
        return jsonify({"errore": "Notizia non trovata"}), 404
    return jsonify(notizia.to_dict())

#Elimina notizia
@app.route('/api/notizie/<int:id>', methods=['DELETE'])
def elimina_notizia(id):
    notizia = Notizia.query.get(id)
    if not notizia:
        return jsonify({"errore": "Notizia non trovata"}), 404
    db.session.delete(notizia)
    db.session.commit()
    return jsonify({"messaggio": "Notizia eliminata"})

# Modifica una notizia (facoltativo)
@app.route('/api/notizie/<int:id>', methods=['PUT'])
def modifica_notizia(id):
    notizia = Notizia.query.get(id)
    if not notizia:
        return jsonify({"errore": "Notizia non trovata"}), 404
    dati = request.get_json()
    notizia.titolo = dati.get('titolo', notizia.titolo)
    notizia.sottotitolo = dati.get('sottotitolo', notizia.sottotitolo)
    notizia.testo = dati.get('testo', notizia.testo)
    db.session.commit()
    return jsonify({"messaggio": "Notizia aggiornata"})

# Genera una notizia fittizia con IA (placeholder per ora)
@app.route('/api/genera-notizia', methods=['POST'])
def genera_notizia_da_articoli_route():
    dati = request.get_json()
    articoli_web = dati.get("articoli_web", [])
    articoli_manuali = dati.get("articoli_manuali", [])
    tema = dati.get("tema", "")

    articolo_generato = genera_notizia_da_articoli(articoli_web, articoli_manuali, tema)

    nuova_notizia = Notizia(
        titolo=articolo_generato["titolo"],
        sottotitolo=articolo_generato["sottotitolo"],
        testo=articolo_generato["testo"]
    )
    db.session.add(nuova_notizia)
    db.session.commit()

    return jsonify(nuova_notizia.to_dict()), 201

@app.route('/api/ricerca-notizie', methods=['GET'])
def ricerca_notizie():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"errore": "Parametro 'q' mancante"}), 400

    risultati = cerca_notizie_web(query)
    return jsonify(risultati)



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
