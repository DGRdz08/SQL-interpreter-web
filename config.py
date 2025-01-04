import os

# Configuraciones generales de la aplicación
class Config:
    SECRET_KEY = "mi-super-secreto"  # Para sesiones, CSRF, etc.
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Carpeta de subida de archivos
    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_EXTENSIONS = {"csv"}

    # Ajustes de la base de datos
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'diego_db.sqlite')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
