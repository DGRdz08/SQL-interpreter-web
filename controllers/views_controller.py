from flask import Blueprint, render_template, session, redirect, url_for

views_bp = Blueprint("views_bp", __name__)

@views_bp.route("/")
def index():
    return render_template("index.html") #Pagina principal

@views_bp.route("/admin")
def admin_page():
    if session.get("user_type") != "admin": return redirect(url_for("views_bp.index")) #Si no eres admin, te manda a la pagina principal
    return render_template("admin.html") #Pagina de admin

@views_bp.route("/conoce")
def conoce():
    return render_template("conoce.html")

@views_bp.route("/consulta")
def consulta():
    if "user_id" not in session: return redirect(url_for("views_bp.index"))
    return render_template("consulta.html")

@views_bp.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")