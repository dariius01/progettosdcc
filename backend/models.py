from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Notizia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    titolo = db.Column(db.String(200))
    sottotitolo = db.Column(db.String(200))
    testo = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'titolo': self.titolo,
            'sottotitolo': self.sottotitolo,
            'testo': self.testo
        }
