import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app as app
from db import get_db_connection
from utils import allowed_file

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('form.html')

@main_bp.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    archivo = request.files['cv']

    # Obtener valores de experiencia, convertir a 1 o 0
    exp_publico = 1 if request.form.get('exp_publico') == 'si' else 0
    exp_produccion = 1 if request.form.get('exp_produccion') == 'si' else 0

    if archivo and allowed_file(archivo.filename):
        filename = f"{nombre}_{apellido}_{archivo.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        archivo.save(filepath)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO postulantes (nombre, apellido, experiencia_publico, experiencia_produccion, curriculum_path) VALUES (%s, %s, %s, %s, %s)",
                (nombre, apellido, exp_publico, exp_produccion, filename)
            )
            conn.commit()
            cursor.close()
            conn.close()

            flash('✅ Enviaste tu CV correctamente. Muchas gracias por postularte.')
        except Exception as err:
            flash(f'❌ Error al registrar el postulante: {err}')
        return redirect(url_for('main.index'))
    else:
        flash('❌ Formato de archivo no permitido.')
        return redirect(url_for('main.index'))
