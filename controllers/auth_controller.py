from flask import Blueprint, request, session, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.db_config import db
from models.admin_model import Admin
from models.client_model import Client

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register/client", methods=["POST"])
def register_client():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    existing = Client.query.filter_by(username=username).first()
    if existing:
        return jsonify({"error": "Username already exists"}), 400

    hashed_pw = generate_password_hash(password)
    new_client = Client(username=username, password=hashed_pw)
    db.session.add(new_client)
    db.session.commit()

    session["user_type"] = "client"
    session["user_id"] = new_client.id
    return jsonify({"message": "Client registered", "redirect": "/conoce"})

@auth_bp.route("/register/admin", methods=["POST"])
def register_admin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    existing = Admin.query.filter_by(username=username).first()
    if existing:
        return jsonify({"error": "Admin username already exists"}), 400

    hashed_pw = generate_password_hash(password)
    new_admin = Admin(username=username, password=hashed_pw)
    db.session.add(new_admin)
    db.session.commit()

    session["user_type"] = "admin"
    session["user_id"] = new_admin.id
    return jsonify({"message": "Admin registered", "redirect": "/admin"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user_type = data.get("user_type")

    if user_type == "admin":
        user = Admin.query.filter_by(username=username).first()
    else:
        user = Client.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Wrong password"}), 401

    session["user_type"] = user_type
    session["user_id"] = user.id
    session["user_name"] = user.username

    if user_type == "admin":
        return jsonify({"message": "Login success", "redirect": "/admin"})
    else:
        return jsonify({"message": "Login success", "redirect": "/consulta"})

@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()  # Limpia la sesión
    return jsonify({"message": "Logout successful", "redirect": "/"})  # Respuesta JSON

@auth_bp.route("/session", methods=["GET"])
def check_session():
    if "user_id" in session:
        return jsonify({"message": "Authenticated"})
    return jsonify({"error": "Not authenticated"}), 401
