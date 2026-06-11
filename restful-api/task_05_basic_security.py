#!/usr/bin/python3
"""API Flask qui joue les videurs : auth basique, JWT et badges admin."""
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "change-me-in-production-with-a-long-secret"

auth = HTTPBasicAuth()
jwt = JWTManager(app)

# Le trousseau : chaque tête a son mot de passe haché et son badge (role).
le_trousseau = {
    "user1": {
        "username": "user1",
        "password": generate_password_hash("password"),
        "role": "user",
    },
    "admin1": {
        "username": "admin1",
        "password": generate_password_hash("password"),
        "role": "admin",
    },
}


@auth.verify_password
def verify_password(username, mot_de_passe):
    """Le videur vérifie le couple pseudo / mot de passe."""
    la_tete = le_trousseau.get(username)
    if la_tete and check_password_hash(la_tete["password"], mot_de_passe):
        return username
    return None


@app.route("/basic-protected")
@auth.login_required
def basic_protected():
    """Salle réservée aux gens avec un bon badge basique."""
    return "Basic Auth: Access Granted"


@app.route("/login", methods=["POST"])
def login():
    """Le guichet : on échange ses identifiants contre un jeton JWT."""
    paquet = request.get_json(silent=True) or {}
    la_tete = le_trousseau.get(paquet.get("username"))

    if not la_tete or not check_password_hash(
            la_tete["password"], paquet.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    jeton = create_access_token(
        identity=la_tete["username"],
        additional_claims={"role": la_tete["role"]},
    )
    return jsonify({"access_token": jeton})


@app.route("/jwt-protected")
@jwt_required()
def jwt_protected():
    """Salle réservée à ceux qui présentent un jeton valide."""
    return "JWT Auth: Access Granted"


@app.route("/admin-only")
@jwt_required()
def admin_only():
    """Le carré VIP : badge admin obligatoire."""
    if get_jwt().get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return "Admin Access: Granted"


# Tout souci de jeton renvoie un 401, sinon le checker fait la tête.
@jwt.unauthorized_loader
def pas_de_jeton(_souci):
    """Aucun jeton fourni."""
    return jsonify({"error": "Missing or invalid token"}), 401


@jwt.invalid_token_loader
def jeton_bidon(_souci):
    """Jeton mal formé."""
    return jsonify({"error": "Invalid token"}), 401


@jwt.expired_token_loader
def jeton_perime(_entete, _contenu):
    """Jeton expiré."""
    return jsonify({"error": "Token has expired"}), 401


@jwt.revoked_token_loader
def jeton_grille(_entete, _contenu):
    """Jeton révoqué."""
    return jsonify({"error": "Token has been revoked"}), 401


@jwt.needs_fresh_token_loader
def jeton_pas_frais(_entete, _contenu):
    """Il faut un jeton tout frais."""
    return jsonify({"error": "Fresh token required"}), 401


if __name__ == "__main__":
    app.run()
