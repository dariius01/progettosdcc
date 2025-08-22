from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timezone, timedelta

db = SQLAlchemy()

# DB Notizia
class Notizia(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(200))
    sottotitolo = db.Column(db.String(200))
    testo = db.Column(db.Text)
    data_creazione = db.Column(db.DateTime, default=datetime.utcnow)
    data_modifica = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 

    def to_dict(self):
        local_tz = timezone(timedelta(hours=2))
        return {
            'id': self.id,
            'titolo': self.titolo,
            'sottotitolo': self.sottotitolo,
            'testo': self.testo,
            'data_creazione': self.data_creazione.replace(tzinfo=timezone.utc).astimezone(local_tz).isoformat(),
            'data_modifica': self.data_modifica.replace(tzinfo=timezone.utc).astimezone(local_tz).isoformat()
        }
from werkzeug.security import generate_password_hash, check_password_hash



# DB User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))  

    notizie = db.relationship('Notizia', backref='autore', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "email": self.email}
