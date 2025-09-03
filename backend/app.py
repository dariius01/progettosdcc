from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from models.models import db
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from routes.auth import auth_bp
from routes.notizia import notizia_bp
from flask import Flask, request
import os
import logging

load_dotenv()
app = Flask(__name__)

# Configurazione Cors
CORS(app,
     origins=["http://localhost:4200", "http://frontend:80"],
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])


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

# Logging per container
logging.basicConfig(level=logging.DEBUG)

@app.before_request
def log_request_info():
    logging.info(f"[{request.remote_addr}] {request.method} {request.path}")


# ROUTES
app.register_blueprint(auth_bp)
app.register_blueprint(notizia_bp)

if __name__ == '__main__':
    print("🚀 Avvio server Flask...")
    app.run(debug=True, host='0.0.0.0', port=5000)
