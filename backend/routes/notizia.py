from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import db, Notizia
from services.ricerca_service import cerca_notizie_web
from services.ai_service import genera_notizia_da_articoli

notizia_bp = Blueprint('notizia', __name__, url_prefix='/api')


## GET notizie realizzate da utente loggato
@notizia_bp.route('/notizie', methods=['GET'])
@jwt_required()
def get_notizie():
    current_user_id = int(get_jwt_identity())
    notizie = Notizia.query.filter_by(user_id=current_user_id).all()
    return jsonify([n.to_dict() for n in notizie])


## GET notizia singola 
@notizia_bp.route('/notizie/<int:id>', methods=['GET'])
@jwt_required()
def get_notizia(id):
    current_user_id = int(get_jwt_identity())
    notizia = db.session.get(Notizia, id)

    if not notizia or notizia.user_id != current_user_id:
        return jsonify({"errore": "Notizia non trovata o accesso non autorizzato"}), 404

    return jsonify(notizia.to_dict())


## ELIMINA notizia
@notizia_bp.route('/notizie/<int:id>', methods=['DELETE'])
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
@notizia_bp.route('/notizie/<int:id>', methods=['PUT'])
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


## SALVA NOTIZIA
@notizia_bp.route('/salva-notizia', methods=['POST'])
@jwt_required()
def salva_notizia():
    
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


## GENERA NOTIZIA
@notizia_bp.route('/genera-notizia', methods=['POST'])
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


## RICERCA WEB
@notizia_bp.route('/ricerca-notizie', methods=['GET'])
def ricerca_notizie():
    query = request.args.get('q', '')

    if not query:
        return jsonify({"errore": "Parametro 'q' mancante"}), 400

    try:
        risultati = cerca_notizie_web(query)
        return jsonify(risultati)
    except Exception as e:
        return jsonify({"errore": "Errore nella ricerca", "dettagli": str(e)}), 500
