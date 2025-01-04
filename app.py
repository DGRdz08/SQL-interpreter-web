from flask import Flask
from config import Config
from models.db_config import db, ma
from werkzeug.security import generate_password_hash
from models.admin_model import Admin

#Controllers
from controllers.views_controller import views_bp
from controllers.auth_controller import auth_bp
from controllers.csv_controller import csv_bp
from controllers.query_controller import query_bp
from controllers.admin_controller import admin_bp

def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    # Registrar blueprints
    app.register_blueprint(views_bp, url_prefix="")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(csv_bp, url_prefix="/csv")
    app.register_blueprint(query_bp, url_prefix="/query")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.add_url_rule("/", endpoint="views_bp.index")

    with app.app_context():
        db.create_all()
        create_default_admin(app)  # Inicializar administrador predeterminado

    return app

def create_default_admin(app):
    if not Admin.query.filter_by(username="adminuser").first():
        hashed_pw = generate_password_hash("adminpassword")
        admin = Admin(username="adminuser", password=hashed_pw)
        db.session.add(admin)
        db.session.commit()
