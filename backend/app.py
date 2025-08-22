from datetime import timedelta
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from models import db, Notizia, User
from services import cerca_notizie_web
from ai import genera_notizia_da_articoli
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity,
    set_access_cookies, unset_jwt_cookies
)
from dotenv import load_dotenv
import re
import os


load_dotenv()
app = Flask(__name__)

# Configurazione Cors
CORS(app, origins=["http://localhost:4200"], supports_credentials=True)

# Configurazione
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  
app.config['JWT_COOKIE_SECURE'] = False 
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
db.init_app(app)

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
MIN_LEN_PASSWORD=8


# ROUTES

## REGISTRAZIONE
@app.route('/api/register', methods=['POST', 'OPTIONS'])
@cross_origin(origin='http://localhost:4200', supports_credentials=True)
def register():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not email:
        return jsonify({'errore': 'L\'email è obbligatoria'}), 400
    if not password:
        return jsonify({'errore': 'La password è obbligatoria'}), 400
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'errore': 'L\'email non è valida'}), 400
    if len(password) < MIN_LEN_PASSWORD:
        return jsonify({'errore': f'La password deve contenere almeno {MIN_LEN_PASSWORD} caratteri'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'errore': 'Email già registrata'}), 409

    try:
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'messaggio': 'Utente registrato con successo'}), 201
    
    except Exception as e:
        db.session.rollback() # Annulla la sessione in caso di errore
        return jsonify({'errore': f'Errore di registrazione: {str(e)}'}), 500


## LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'errore': 'Email e password sono obbligatori'}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        response = jsonify({'messaggio': 'Login effettuato'})
        set_access_cookies(response, access_token)
        return response, 200

    return jsonify({'errore': 'Email o password non validi'}), 401


@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    response = make_response(jsonify({"msg": "Logout effettuato"}), 200)
    response.set_cookie('access_token_cookie', '', expires=0, httponly=True, samesite='Lax')
    return response


## GET notizie realizzate da utente loggato
@app.route('/api/notizie', methods=['GET'])
@jwt_required()
def get_notizie():
    current_user_id = int(get_jwt_identity())
    notizie = Notizia.query.filter_by(user_id=current_user_id).all()
    return jsonify([n.to_dict() for n in notizie])


## GET notizia singola 
@app.route('/api/notizie/<int:id>', methods=['GET'])
@jwt_required()
def get_notizia(id):
    current_user_id = int(get_jwt_identity())
    notizia = db.session.get(Notizia, id)

    if not notizia or notizia.user_id != current_user_id:
        return jsonify({"errore": "Notizia non trovata o accesso non autorizzato"}), 404

    return jsonify(notizia.to_dict())


## ELIMINA notizia
@app.route('/api/notizie/<int:id>', methods=['DELETE'])
@jwt_required()
def elimina_notizia(id):
    current_user_id = int(get_jwt_identity())
    notizia = db.session.get(Notizia, id)

    if not notizia or notizia.user_id != current_user_id:
        return jsonify({"errore": "Notizia non trovata o accesso non autorizzato"}), 404

    try:
        db.session.delete(notizia)
        db.session.commit()
        return jsonify({"success": True, "message": "Notizia eliminata"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


## MODIFICA notizia
@app.route('/api/notizie/<int:id>', methods=['PUT'])
@jwt_required()
def modifica_notizia(id):
    current_user_id = int(get_jwt_identity())
    notizia = db.session.get(Notizia, id)

    if not notizia or notizia.user_id != current_user_id:
        return jsonify({"errore": "Notizia non trovata o accesso non autorizzato"}), 404

    dati = request.get_json()
    if not dati:
        return jsonify({"errore": "Dati non validi"}), 400

    try:
        notizia.titolo = dati.get('titolo', notizia.titolo)
        notizia.sottotitolo = dati.get('sottotitolo', notizia.sottotitolo)
        notizia.testo = dati.get('testo', notizia.testo)
        db.session.commit()
        return jsonify({"messaggio": "Notizia aggiornata"}), 200
    
    except:
        db.session.rollback()
        return jsonify({"errore": "Si è verificato un errore durante l'aggiornamento della notizia"}), 500


## GGENERA NOTIZIA
@app.route('/api/genera-notizia', methods=['POST'])
def genera_notizia_da_articoli_route():
    dati = request.get_json()

    try:
        articolo = genera_notizia_da_articoli(
        dati.get("articoli_web", []),
        dati.get("articoli_manuali", []),
        dati.get("tema", ""))
        return jsonify(articolo), 200
    
    except Exception as e:
        print(f"Errore nella generazione della notizia: {e}") 
        return jsonify({"errore": "Si è verificato un errore interno durante la generazione della notizia."}), 500


## SALVA NOTIZIA
@app.route('/api/salva-notizia', methods=['POST'])
@jwt_required()
def salva_notizia_route():
    
    dati = request.get_json()

    titolo = dati.get("titolo", "")
    sottotitolo = dati.get("sottotitolo", "")
    testo = dati.get("testo", "")

    if not isinstance(titolo, str) or not isinstance(testo, str):
        return jsonify({"errore": "Titolo e testo devono essere stringhe"}), 422

    if not titolo or not testo:
        return jsonify({"errore": "Titolo e testo sono obbligatori"}), 400

    try:
        current_user_id = get_jwt_identity()
        notizia = Notizia(
            titolo=titolo,
            sottotitolo=sottotitolo,
            testo=testo,
            user_id=current_user_id
        )
        db.session.add(notizia)
        db.session.commit()
        return jsonify(notizia.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"errore": "Si è verificato un errore durante il salvataggio della notizia"}), 500


## RICERCA WEB
@app.route('/api/ricerca-notizie', methods=['GET'])
def ricerca_notizie():
    query = request.args.get('q', '')

    if not query:
        return jsonify({"errore": "Parametro 'q' mancante"}), 400

    try:
        risultati = cerca_notizie_web(query)
        return jsonify(risultati)
    except Exception as e:
        return jsonify({"errore": "Errore nella ricerca", "dettagli": str(e)}), 500


if __name__ == '__main__':
    print("🚀 Avvio server Flask...")
    app.run(debug=True, host='0.0.0.0', port=5000)
