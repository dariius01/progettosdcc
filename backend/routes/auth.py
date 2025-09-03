from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity
from models.models import db, User
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
MIN_LEN_PASSWORD=8

## REGISTRAZIONE
@auth_bp.route('/register', methods=['POST'])
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
@auth_bp.route('/login', methods=['POST'])
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


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = make_response(jsonify({"msg": "Logout effettuato"}), 200)
    response.set_cookie('access_token_cookie', '', expires=0, httponly=True, samesite='Lax')
    return response
