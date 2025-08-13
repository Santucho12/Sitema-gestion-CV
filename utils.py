import os
import psycopg2
from config import Config

UPLOAD_FOLDER = Config.UPLOAD_FOLDER

DB_CONFIG = {
    'host': Config.DB_HOST,
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dbname': Config.DB_NAME,
    'port': Config.DB_PORT
}

# Cuando eliminas un postulante, se borran sus datos de varias tablas y archivos asociados
def limpiar_archivos_huerfanos():
    # --- FUNCION DESHABILITADA ---
    pass

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'heic', 'heif', 'webp'}

def allowed_file(filename):
    # Chequeamos que el archivo tenga extensión permitida
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
