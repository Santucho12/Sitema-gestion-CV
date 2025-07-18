import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app as app
from werkzeug.utils import secure_filename
from db import get_db_connection
from utils import allowed_file
import logging

main_bp = Blueprint('main', __name__)
logging.basicConfig(level=logging.INFO)

@main_bp.route('/')
## aca se muestra el formulario para que la gente se anote
def index():
    return render_template('index.html')

@main_bp.route('/submit', methods=['POST'])
## aca se procesa el formulario cuando alguien se anota
def submit():
    # aca se agarran todos los datos del form
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    sexo = request.form.get('sexo', '')
    fecha_nacimiento = request.form.get('fecha_nacimiento', '')
    direccion = request.form.get('direccion', '').strip()
    estado_civil = request.form.get('estado_civil', '')
    disponibilidad_horaria = request.form.get('disponibilidad_horaria', '')
    tipo_formacion = request.form.get('tipo_formacion', '')
    curso_manipulacion_alimentos = 1 if request.form.get('curso_manipulacion_alimentos') else 0
    atencion_publico = 1 if request.form.get('atencion_publico') else 0
    experiencia_administrativa = 1 if request.form.get('experiencia_administrativa') else 0
    experiencia_reparto = 1 if request.form.get('experiencia_reparto') else 0
    experiencia_produccion = 1 if request.form.get('experiencia_produccion') else 0
    conocimientos_produccion = request.form.get('conocimientos_produccion', '').strip()
    nivel_excel = request.form.get('nivel_excel', '')
    licencia_auto = 1 if request.form.get('licencia_auto') else 0
    tiene_movilidad_propia = 1 if request.form.get('tiene_movilidad_propia') else 0
    archivo = request.files.get('cv')
    foto_postulante = request.files.get('foto_postulante')
    calificacion = 0  # arranca en cero, despues el admin la cambia

    # Validación básica
    if not nombre or not apellido:
        flash('❌ Nombre y apellido son obligatorios.')
        return redirect(url_for('main.index'))
    if not archivo:
        flash('❌ Debes adjuntar un archivo.')
        return redirect(url_for('main.index'))
    if not allowed_file(archivo.filename):
        flash('❌ Formato de archivo no permitido.')
        return redirect(url_for('main.index'))
    if not foto_postulante:
        flash('❌ Debes adjuntar una foto.')
        return redirect(url_for('main.index'))

    # Sanitizar los nombres de archivos para evitar problemas con espacios o caracteres especiales
    filename_cv = secure_filename(f"{nombre}_{apellido}_{archivo.filename}")
    filepath_cv = os.path.join(app.config['UPLOAD_FOLDER'], filename_cv)
    filename_foto = secure_filename(f"{nombre}_{apellido}_{foto_postulante.filename}")
    filepath_foto = os.path.join(app.config['UPLOAD_FOLDER'], filename_foto)

    try:
        # Guardar archivos en la carpeta uploads
        archivo.save(filepath_cv)
        foto_postulante.save(filepath_foto)

        conn = get_db_connection()
        if conn is None:
            flash('❌ No se pudo conectar a la base de datos.')
            logging.error('No se pudo conectar a la base de datos.')
            return redirect(url_for('main.index'))

        cursor = conn.cursor()
        # Primero se mete el postulante
        cursor.execute(
            """
            INSERT INTO Postulantes (nombre, apellido, sexo, fecha_nacimiento, direccion, estado_civil, disponibilidad_horaria, curso_manipulacion_alimentos, calificacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (nombre, apellido, sexo, fecha_nacimiento, direccion, estado_civil, disponibilidad_horaria, curso_manipulacion_alimentos, calificacion)
        )
        id_postulante = cursor.lastrowid

        # Después se mete la formación
        cursor.execute(
            """
            INSERT INTO Formacion (id_postulante, tipo)
            VALUES (%s, %s)
            """,
            (id_postulante, tipo_formacion)
        )

        # Experiencia en panadería
        cursor.execute(
            """
            INSERT INTO ExperienciaPanaderia (id_postulante, experiencia_produccion, conocimientos_produccion)
            VALUES (%s, %s, %s)
            """,
            (id_postulante, experiencia_produccion, conocimientos_produccion)
        )

        # Experiencia general
        cursor.execute(
            """
            INSERT INTO Experiencia (id_postulante, atencion_publico, experiencia_administrativa, experiencia_reparto)
            VALUES (%s, %s, %s, %s)
            """,
            (id_postulante, atencion_publico, experiencia_administrativa, experiencia_reparto)
        )

        # Conocimientos de Excel
        cursor.execute(
            """
            INSERT INTO ConocimientosExcel (id_postulante, nivel)
            VALUES (%s, %s)
            """,
            (id_postulante, nivel_excel)
        )

        # Movilidad
        cursor.execute(
            """
            INSERT INTO Movilidad (id_postulante, licencia_auto, tiene_movilidad_propia)
            VALUES (%s, %s, %s)
            """,
            (id_postulante, licencia_auto, tiene_movilidad_propia)
        )

        # Documentos (rutas de archivos sanitizadas)
        cursor.execute(
            """
            INSERT INTO Documentos (id_postulante, ruta_cv, ruta_foto)
            VALUES (%s, %s, %s)
            """,
            (id_postulante, filename_cv, filename_foto)
        )

        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Postulante registrado: {nombre} {apellido}")
        flash('✅ Enviaste tu CV correctamente. Muchas gracias por postularte.')
        return redirect(url_for('main.index'))
    except Exception as err:
        logging.error(f'Error al registrar el postulante: {err}')
        flash(f'❌ Error al registrar el postulante: {err}')
        return redirect(url_for('main.index'))
    finally:
        pass
