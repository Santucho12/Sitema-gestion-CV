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
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Pedimos todos los nombres de archivos que están en la base, tanto CV como foto
        cursor.execute("SELECT cv, foto_postulante FROM Documentos")
        archivos_db = set()
        for cv, foto in cursor.fetchall():
            if cv:  # si hay cv, lo guardamos
                archivos_db.add(cv)
            if foto:  # si hay foto, lo guardamos
                archivos_db.add(foto)

        # Ahora miramos todos los archivos que hay en la carpeta uploads
        uploads = os.listdir(UPLOAD_FOLDER)
        eliminados = []
        for archivo in uploads:
            # Si el archivo no está en la base, se borra
            if archivo not in archivos_db:
                ruta = os.path.join(UPLOAD_FOLDER, archivo)
                try:
                    os.remove(ruta)  # lo borramos del disco
                    eliminados.append(archivo)
                except Exception as e:
                    print(f"No se pudo eliminar {archivo}: {e}")

        # Mostramos por consola los que se borraron
        print(f"Archivos huérfanos eliminados: {eliminados}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al limpiar archivos huérfanos: {e}")

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'heic', 'heif', 'webp'}

def allowed_file(filename):
    # Chequeamos que el archivo tenga extensión permitida
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
