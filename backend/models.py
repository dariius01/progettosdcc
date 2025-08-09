from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Notizia(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(200))
    sottotitolo = db.Column(db.String(200))
    testo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'titolo': self.titolo,
            'sottotitolo': self.sottotitolo,
            'testo': self.testo,
            'created_at': self.created_at.isoformat()
        }
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))  


    notizie = db.relationship('Notizia', backref='autore', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "email": self.email}
