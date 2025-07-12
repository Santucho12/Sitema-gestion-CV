import os
import mysql.connector
from config import Config

UPLOAD_FOLDER = Config.UPLOAD_FOLDER
DB_CONFIG = {
    'host': Config.DB_HOST,
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'database': Config.DB_NAME
}

def limpiar_archivos_huerfanos():
    """
    Elimina archivos en la carpeta uploads que no estén asociados a ningún postulante en la base de datos.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT cv, foto_postulante FROM Documentos")
        archivos_db = set()
        for cv, foto in cursor.fetchall():
            if cv:
                archivos_db.add(cv)
            if foto:
                archivos_db.add(foto)
        uploads = os.listdir(UPLOAD_FOLDER)
        eliminados = []
        for archivo in uploads:
            if archivo not in archivos_db:
                ruta = os.path.join(UPLOAD_FOLDER, archivo)
                try:
                    os.remove(ruta)
                    eliminados.append(archivo)
                except Exception as e:
                    print(f"No se pudo eliminar {archivo}: {e}")
        print(f"Archivos huérfanos eliminados: {eliminados}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al limpiar archivos huérfanos: {e}")
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

"""
Utilidades para validación de archivos y otras funciones auxiliares.
Mantén este archivo para funciones reutilizables.
"""
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    """Valida si el archivo tiene una extensión permitida."""
