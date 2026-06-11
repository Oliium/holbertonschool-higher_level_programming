#!/usr/bin/python3
"""Petite API REST avec Flask : le grand registre des utilisateurs."""
from flask import Flask, jsonify, request

app = Flask(__name__)

# Notre carnet d'adresses : la clé c'est le username.
le_carnet = {}


@app.route("/")
def home():
    """Le tapis de bienvenue."""
    return "Welcome to the Flask API!"


@app.route("/status")
def status():
    """Petit check de santé : tout va bien ?"""
    return "OK"


@app.route("/data")
def data():
    """Donne juste la liste des pseudos enregistrés."""
    return jsonify(list(le_carnet.keys()))


@app.route("/users/<username>")
def get_user(username):
    """Sort la fiche complète d'un utilisateur, ou râle en 404."""
    if username not in le_carnet:
        return jsonify({"error": "User not found"}), 404
    return jsonify(le_carnet[username])


@app.route("/add_user", methods=["POST"])
def add_user():
    """Inscrit un nouveau venu dans le carnet."""
    nouveau = request.get_json(silent=True)
    if nouveau is None:
        return jsonify({"error": "Invalid JSON"}), 400

    pseudo = nouveau.get("username")
    if not pseudo:
        return jsonify({"error": "Username is required"}), 400
    if pseudo in le_carnet:
        return jsonify({"error": "Username already exists"}), 409

    le_carnet[pseudo] = nouveau
    return jsonify({"message": "User added", "user": nouveau}), 201


if __name__ == "__main__":
    app.run()
