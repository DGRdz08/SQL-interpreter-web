# Pasos para hacer uso del proyecto
```bash
Crea un entorno virtual para el proyecto
    asigna un nombre a tu entorno
        python3 -m venv entorno
    activa el entorno
        source entorno/bin/activate
    en caso de querer desactivar el entorno
        deactivate
    para instalar los modulos necesarios
        pip install -r requirements.txt

Abre un terminal integrado al archivo run.py
    python3 run.py

Credenciales de administrador
    uduario:        adminuser
    contraseña:     adminpassword

Registrate, sigue el tutorial y usa
# Estructura del Proyecto

```plaintext
mi_proyecto/
├── app.py
├── config.py
├── requirements.txt
├── run.py
├── controllers/
│   ├── auth_controller.py
│   ├── csv_controller.py
│   ├── query_controller.py
│   ├── views_controller.py
│   └── admin_controller.py
├── models/
│   ├── db_config.py
│   ├── admin_model.py
│   ├── client_model.py
│   └── query_log_model.py
├── services/
│   ├── concurrency_service.py
│   ├── interpreter_service.py
│   ├── SQLLexer.py        
│   ├── SQLParser.py
│   └── data_handler.py
├── static/
│   ├── styles.css
│   ├── script.js
│   ├── images/
│   └── uploads/
│       └── (subcarpetas por usuario)
└── templates/
    ├── index.html
    ├── admin.html
    ├── conoce.html
    ├── consulta.html
    └── nosotros.html
