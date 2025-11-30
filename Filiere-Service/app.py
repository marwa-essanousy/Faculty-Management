import os
import socket
import uuid
import atexit
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from py_eureka_client import eureka_client

# ---------------- Configuration ----------------
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka/")
APP_NAME = os.getenv("APP_NAME", "FILIERE-SERVICE")
PORT = int(os.getenv("PORT", 5001))

# MySQL / SQLAlchemy config
DB_USER = os.getenv("DB_USER", "filiere_user")
DB_PASS = os.getenv("DB_PASS", "secure_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "filiere_db")
DATABASE_URL = os.getenv("DATABASE_URL",
                         f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# ---------------- App & DB init ----------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# ---------------- Model (équivalent JPA Entity) ----------------
class Filiere(db.Model):
    __tablename__ = "filiere"
    # On garde le même nom de colonne idFiliere pour correspondance avec Java
    idFiliere = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    libelle = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "idFiliere": self.idFiliere,
            "code": self.code,
            "libelle": self.libelle
        }


# Create tables si besoin (au démarrage)
with app.app_context():
    db.create_all()


# ---------------- Routes / Controllers ----------------
@app.route("/filieres", methods=["GET"])
def list_filieres():
    filieres = Filiere.query.all()
    return jsonify([f.to_dict() for f in filieres]), 200


@app.route("/filieres/<int:id_filiere>", methods=["GET"])
def get_filiere(id_filiere):
    f = Filiere.query.get_or_404(id_filiere)
    return jsonify(f.to_dict()), 200


@app.route("/filieres", methods=["POST"])
def create_filiere():
    data = request.get_json() or {}
    code = data.get("code")
    libelle = data.get("libelle")
    if not code or not libelle:
        abort(400, description="Les champs 'code' et 'libelle' sont requis.")
    # unique code check
    if Filiere.query.filter_by(code=code).first():
        abort(400, description="Un enregistrement avec ce code existe déjà.")
    f = Filiere(code=code, libelle=libelle)
    db.session.add(f)
    db.session.commit()
    return jsonify(f.to_dict()), 201


@app.route("/filieres/<int:id_filiere>", methods=["PUT"])
def update_filiere(id_filiere):
    data = request.get_json() or {}
    f = Filiere.query.get_or_404(id_filiere)
    if "code" in data:
        # si on change le code, vérifier l'unicité
        new_code = data["code"]
        if new_code != f.code and Filiere.query.filter_by(code=new_code).first():
            abort(400, description="Un enregistrement avec ce code existe déjà.")
        f.code = new_code
    if "libelle" in data:
        f.libelle = data["libelle"]
    db.session.commit()
    return jsonify(f.to_dict()), 200


@app.route("/filieres/<int:id_filiere>", methods=["DELETE"])
def delete_filiere(id_filiere):
    f = Filiere.query.get_or_404(id_filiere)
    db.session.delete(f)
    db.session.commit()
    return "", 204


# Health check (Eureka / Gateway)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200


# ---------------- Eureka registration ----------------
# Instance id unique
INSTANCE_ID = f"{socket.gethostname()}:{APP_NAME}:{uuid.uuid4()}"

def register_to_eureka():
    # instance_host : IP que Eureka peut joindre (localhost si tout est sur la même machine)
    host_ip = os.getenv("INSTANCE_HOST", socket.gethostbyname(socket.gethostname()))
    eureka_client.init(
        eureka_server=EUREKA_SERVER,
        app_name=APP_NAME,
        instance_port=PORT,
        instance_host=host_ip,
        instance_ip=host_ip,
        health_check_url=f"http://{host_ip}:{PORT}/health",
        # home_page_url=f"http://{host_ip}:{PORT}/",  # optionnel
    )
    print(f"[Eureka] Registered {APP_NAME} at {EUREKA_SERVER} (host={host_ip}, port={PORT})")


def deregister_from_eureka():
    try:
        eureka_client.stop()
        print("[Eureka] Deregistered")
    except Exception as e:
        print("[Eureka] Error during deregistration:", e)


atexit.register(deregister_from_eureka)


# ---------------- Run ----------------
if __name__ == "__main__":
    register_to_eureka()
    # debug=False recommended en local tu peux mettre debug=True si tu veux
    app.run(host="0.0.0.0", port=PORT)
