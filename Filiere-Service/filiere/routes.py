# filiere/routes.py
from flask import Blueprint, jsonify, request, abort
from filiere.services import FiliereServiceImpl
from filiere.mappers import FiliereMapper

bp = Blueprint("filiere_bp", __name__)

# instanciation du mapper + service (comparable à injection par constructeur en Java)
mapper = FiliereMapper()
service = FiliereServiceImpl(mapper=mapper)

@bp.route("/filieres", methods=["GET"])
def list_filieres():
    dtos = service.getAllFilieres()
    return jsonify([dto.__dict__ for dto in dtos]), 200

@bp.route("/filieres/<int:id_filiere>", methods=["GET"])
def get_filiere(id_filiere):
    try:
        dto = service.getFiliereById(id_filiere)
        return jsonify(dto.__dict__), 200
    except LookupError:
        abort(404)

@bp.route("/filieres", methods=["POST"])
def create_filiere():
    data = request.get_json() or {}
    try:
        dto = service.addFiliere(data)
        return jsonify(dto.__dict__), 201
    except ValueError as e:
        abort(400, description=str(e))

@bp.route("/filieres/<int:id_filiere>", methods=["PUT"])
def update_filiere(id_filiere):
    data = request.get_json() or {}
    try:
        dto = service.updateFiliere(data, id_filiere)
        return jsonify(dto.__dict__), 200
    except LookupError:
        abort(404)
    except ValueError as e:
        abort(400, description=str(e))

@bp.route("/filieres/<int:id_filiere>", methods=["DELETE"])
def delete_filiere(id_filiere):
    try:
        service.deleteFiliere(id_filiere)
        return "", 204
    except LookupError:
        abort(404)
