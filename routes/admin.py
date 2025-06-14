from flask import Blueprint, render_template, send_from_directory, current_app as app
from auth import auth
from db import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@auth.login_required
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM postulantes")
    postulantes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', postulantes=postulantes)

@admin_bp.route('/uploads/<nombre_archivo>')
@auth.login_required
def ver_cv(nombre_archivo):
    return send_from_directory(app.config['UPLOAD_FOLDER'], nombre_archivo)
