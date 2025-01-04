from flask import Blueprint, request, session, jsonify
import os
from config import Config, allowed_file
from pathlib import Path
import pandas as pd

csv_bp = Blueprint("csv_bp", __name__)

@csv_bp.route("/upload", methods=["POST"])
def upload_csv():
    if "user_id" not in session:
        return jsonify({"error": "No estás autenticado"}), 401

    user_type = session["user_type"]
    user_id = session["user_id"]
    username = _get_username(user_type, user_id)

    if "file" not in request.files:
        return jsonify({"error": "No se ha recibido un archivo"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No se ha seleccionado un archivo"}), 400

    if file and allowed_file(file.filename):
        user_folder = os.path.join(Config.UPLOAD_FOLDER, f"user_{user_id}")
        Path(user_folder).mkdir(parents=True, exist_ok=True)

        filepath = os.path.join(user_folder, file.filename)
        file.save(filepath)

        try:
            # Leer las columnas del archivo CSV
            df = pd.read_csv(filepath)
            columns = list(df.columns)

            return jsonify({
                "message": f"Archivo {file.filename} subido con éxito",
                "filepath": filepath,
                "columns": columns
            })
        except Exception as e:
            return jsonify({"error": f"Error al procesar el archivo CSV: {str(e)}"}), 500
    else:
        return jsonify({"error": "Formato de archivo no permitido. Solo se permiten archivos CSV."}), 400

def _get_username(user_type, user_id):
    if user_type == "admin":
        from models.admin_model import Admin
        user = Admin.query.get(user_id)
    else:
        from models.client_model import Client
        user = Client.query.get(user_id)
    return user.username if user else "unknown"
