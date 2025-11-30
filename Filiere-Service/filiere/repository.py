# filiere/repository.py
from filiere.models import Filiere
from app import db

def find_all():
    return Filiere.query.all()

def find_by_id(id_filiere):
    return Filiere.query.get(id_filiere)

def find_by_code(code):
    return Filiere.query.filter_by(code=code).first()

def save(filiere: Filiere):
    db.session.add(filiere)
    db.session.commit()
    return filiere

def delete(filiere: Filiere):
    db.session.delete(filiere)
    db.session.commit()
