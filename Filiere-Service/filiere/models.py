# filiere/models.py
from app import db

class Filiere(db.Model):
    __tablename__ = "filiere"
    idFiliere = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    libelle = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "idFiliere": self.idFiliere,
            "code": self.code,
            "libelle": self.libelle
        }

    def update_from_dict(self, data: dict):
        if "code" in data:
            self.code = data["code"]
        if "libelle" in data:
            self.libelle = data["libelle"]
