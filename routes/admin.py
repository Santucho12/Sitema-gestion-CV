import os
from flask import Blueprint, render_template, send_from_directory, current_app as app, abort, request, jsonify
from auth import auth
from db import get_db_connection
import logging
import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
logging.basicConfig(level=logging.INFO)

# Ruta para eliminar postulante
@admin_bp.route('/eliminar_postulante', methods=['POST'])
@auth.login_required
def eliminar_postulante():
    data = request.get_json()
    id_postulante = data.get('id')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Obtener rutas de archivos antes de eliminar
        cursor.execute("SELECT ruta_cv, ruta_foto FROM Documentos WHERE id_postulante = %s", (id_postulante,))
        doc = cursor.fetchone()
        # Eliminar registros relacionados en tablas hijas
        cursor.execute("DELETE FROM Formacion WHERE id_postulante = %s", (id_postulante,))
        cursor.execute("DELETE FROM ExperienciaPanaderia WHERE id_postulante = %s", (id_postulante,))
        cursor.execute("DELETE FROM Experiencia WHERE id_postulante = %s", (id_postulante,))
        cursor.execute("DELETE FROM ConocimientosExcel WHERE id_postulante = %s", (id_postulante,))
        cursor.execute("DELETE FROM Movilidad WHERE id_postulante = %s", (id_postulante,))
        cursor.execute("DELETE FROM Documentos WHERE id_postulante = %s", (id_postulante,))
        # Finalmente, eliminar el postulante principal
        cursor.execute("DELETE FROM Postulantes WHERE id = %s", (id_postulante,))
        conn.commit()
        cursor.close()
        conn.close()
        # Eliminar archivos del sistema
        import os
        from config import Config
        if doc:
            if doc.get('ruta_cv'):
                cv_path = os.path.join(Config.UPLOAD_FOLDER, doc['ruta_cv'])
                if os.path.isfile(cv_path):
                    try:
                        os.remove(cv_path)
                    except Exception as err:
                        logging.error(f"No se pudo eliminar el archivo CV: {cv_path} - {err}")
            if doc.get('ruta_foto'):
                foto_path = os.path.join(Config.UPLOAD_FOLDER, doc['ruta_foto'])
                if os.path.isfile(foto_path):
                    try:
                        os.remove(foto_path)
                    except Exception as err:
                        logging.error(f"No se pudo eliminar la foto: {foto_path} - {err}")
        # Limpiar archivos huérfanos después de eliminar
        from utils import limpiar_archivos_huerfanos
        limpiar_archivos_huerfanos()
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error al eliminar postulante: {e}")
        return jsonify({'success': False, 'error': str(e)})

# Ruta para actualizar calificación
@admin_bp.route('/calificar', methods=['POST'])
@auth.login_required
def calificar():
    data = request.get_json()
    id_postulante = data.get('id_postulante')
    calificacion = data.get('calificacion')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Postulantes SET calificacion = %s WHERE id = %s", (calificacion, id_postulante))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error al actualizar calificación: {e}")
        return jsonify({'success': False, 'error': str(e)})

# Ruta protegida por login
@admin_bp.route('/')
@auth.login_required
def admin():
    conn = get_db_connection()
    if conn is None:
        logging.error('No se pudo conectar a la base de datos en /admin.')
        abort(500)
    cursor = conn.cursor(dictionary=True)
    # Consulta con JOINs para traer todos los datos relevantes
    cursor.execute('''
        SELECT
            p.id AS id_postulante, p.nombre, p.apellido, p.sexo, p.fecha_nacimiento, p.direccion, p.estado_civil, p.disponibilidad_horaria, p.curso_manipulacion_alimentos, p.calificacion,
            f.tipo AS tipo_formacion,
            ep.experiencia_produccion, ep.conocimientos_produccion,
            e.atencion_publico, e.experiencia_administrativa, e.experiencia_reparto,
            ce.nivel AS nivel_excel,
            m.licencia_auto, m.tiene_movilidad_propia,
            d.ruta_cv, d.ruta_foto
        FROM Postulantes p
        LEFT JOIN Formacion f ON p.id = f.id_postulante
        LEFT JOIN ExperienciaPanaderia ep ON p.id = ep.id_postulante
        LEFT JOIN Experiencia e ON p.id = e.id_postulante
        LEFT JOIN ConocimientosExcel ce ON p.id = ce.id_postulante
        LEFT JOIN Movilidad m ON p.id = m.id_postulante
        LEFT JOIN Documentos d ON p.id = d.id_postulante
        ORDER BY p.id DESC
    ''')
    postulantes = cursor.fetchall()
    cursor.close()
    conn.close()
    logging.info('Acceso a panel admin.')
    return render_template('admin.html', postulantes=postulantes, today=datetime.date.today())

# Ruta protegida para ver archivos subidos
@admin_bp.route('/uploads/<nombre_archivo>')
@auth.login_required
def ver_cv(nombre_archivo):
    # Validar que el archivo exista en la carpeta
    folder = app.config['UPLOAD_FOLDER']
    file_path = os.path.join(folder, nombre_archivo)
    if not os.path.isfile(file_path):
        logging.warning(f"Intento de acceso a archivo inexistente: {nombre_archivo}")
        abort(404)
    logging.info(f"Descarga de archivo: {nombre_archivo}")
    return send_from_directory(folder, nombre_archivo)
