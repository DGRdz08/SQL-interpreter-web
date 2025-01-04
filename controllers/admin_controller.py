from flask import Blueprint, session, jsonify
from models.query_log_model import QueryLog, query_logs_schema
from models.admin_model import Admin

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/logs", methods=["GET"])
def get_logs():
    # Verificar que sea admin
    if session.get("user_type") != "admin":
        return jsonify({"error": "No tienes permisos"}), 403

    all_logs = QueryLog.query.all()
    return jsonify(query_logs_schema.dump(all_logs))
