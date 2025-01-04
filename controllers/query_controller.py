from flask import Blueprint, request, session, jsonify, Response
from services.interpreter_service import SQLInterpreter
from models.query_log_model import QueryLog, db
import datetime
import platform
import os
from io import BytesIO
from reportlab.pdfgen import canvas
import pandas as pd

query_bp = Blueprint("query_bp", __name__)
interpreter = SQLInterpreter()

@query_bp.route("/execute", methods=["POST"])
def execute_query():
    if "user_id" not in session:
        return jsonify({"error": "No estás autenticado"}), 401
    
    try:
        data = request.get_json()
        query_text = data.get("query_text")
        file_selected = data.get("filename")

        if not query_text:
            return jsonify({"error": "Query vacío"}), 400
        if not file_selected:
            return jsonify({"error": "No se ha seleccionado un archivo CSV"}), 400

        user_folder = f"static/uploads/user_{session['user_id']}/"
        filepath = os.path.join(user_folder, file_selected)
        if not os.path.exists(filepath):
            return jsonify({"error": "El archivo CSV no se encuentra"}), 400

        result = interpreter.execute_query(query_text, filepath)

        # Guardar el query en el historial
        _save_query_log(query_text, file_selected)

        # result podría ser un dict con 'error' o con la data
        if isinstance(result, dict) and "error" in result:
            return jsonify({"error": result["error"]}), 400

        # Si es SELECT: result es una lista de dicts
        # Si es INSERT/UPDATE/DELETE: result puede traer "message"
        return jsonify({"message": "OK", "data": result})

    except Exception as e:
        return jsonify({"error": f"Error al ejecutar la consulta: {str(e)}"}), 500

@query_bp.route("/download-pdf", methods=["POST"])  #Endpoint para descargar PDF
def download_pdf():

    data = request.get_json() or {}
    operation = data.get("operation", "").upper()  # SELECT, INSERT, etc.
    results_str = data.get("results", "")          # si es SELECT
    filename = data.get("filename", "")            # si es INSERT/UPDATE/DELETE

    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    if operation == "SELECT":
        # Renderizar 'results_str' línea por línea
        c.drawString(100, 750, "Resultados de la consulta (SELECT):")
        y = 730
        for line in results_str.split('\n'):
            c.drawString(100, y, line)
            y -= 15
        c.showPage()
        c.save()

    else:
        # INSERT, UPDATE o DELETE => convertir el CSV completo a PDF
        if not filename:
            # Si no hay filename, no podemos convertir
            c.drawString(100, 750, "No se proporcionó filename para convertir a PDF.")
            c.showPage()
            c.save()
        else:
            # Cargar CSV y volcarlo
            user_folder = f"static/uploads/user_{session['user_id']}/"
            filepath = os.path.join(user_folder, filename)
            if not os.path.exists(filepath):
                c.drawString(100, 750, f"Archivo {filepath} no encontrado.")
                c.showPage()
                c.save()
            else:
                df = pd.read_csv(filepath)
                cols = df.columns.tolist()

                # Encabezado
                c.drawString(100, 750, f"Contenido de {filename}:")
                x_start = 100
                y_start = 730
                line_height = 15

                # Imprimir nombre de columnas
                c.setFont("Helvetica-Bold", 10)
                header_line = " | ".join(cols)
                c.drawString(x_start, y_start, header_line)
                c.setFont("Helvetica", 10)
                y_start -= (line_height + 5)

                # Imprimir filas
                for idx, row in df.iterrows():
                    row_line = " | ".join(str(row[col]) for col in cols)
                    c.drawString(x_start, y_start, row_line)
                    y_start -= line_height
                    # Si baja demasiado, saltar página:
                    if y_start < 50:
                        c.showPage()
                        y_start = 750
                        c.setFont("Helvetica", 10)

                c.showPage()
                c.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    return Response(pdf_data, mimetype="application/pdf")

def _save_query_log(query_text, filename):
    user_type = session.get("user_type", "client")
    user_id = session.get("user_id", 0)
    ip = request.remote_addr or "unknown"
    browser = request.headers.get("User-Agent", "unknown")
    so = platform.system()
    url = request.base_url

    new_log = QueryLog(
        user_type=user_type,
        user_id=user_id,
        query_text=query_text,
        url=url,
        ip=ip,
        browser=browser,
        so=so,
        timestamp=datetime.datetime.now()
    )
    db.session.add(new_log)
    db.session.commit()
