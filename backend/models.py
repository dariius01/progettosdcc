from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Notizia(db.Model):
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
