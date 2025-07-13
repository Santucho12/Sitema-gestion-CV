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
#cuando eliminas un postulante, se borran sus datos de varias tablas y archivos asociados
def limpiar_archivos_huerfanos():
    # bueno aca conectamos a la db
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # pedimos todos los nombres de archivos que estan en la base, tanto cv como foto
        cursor.execute("SELECT cv, foto_postulante FROM Documentos")
        archivos_db = set()
        # aca vamos sumando los nombres que aparecen en la base, si hay alguno lo metemos en el set
        for cv, foto in cursor.fetchall():
            if cv:  # si hay cv, lo guardamos
                archivos_db.add(cv)
            if foto:  # si hay foto, lo guardamos
                archivos_db.add(foto)

        # ahora miramos todos los archivos que hay en la carpeta uploads
        uploads = os.listdir(UPLOAD_FOLDER)
        eliminados = []
        # revisamos uno por uno los archivos
        for archivo in uploads:
            # si el archivo no esta en la base, se borra
            if archivo not in archivos_db:
                ruta = os.path.join(UPLOAD_FOLDER, archivo)
                try:
                    os.remove(ruta)  # lo borramos del disco
                    eliminados.append(archivo)  # lo anotamos en la lista de los que se fueron
                except Exception as e:
                    print(f"no se pudo eliminar {archivo}: {e}")  # si no se puede borrar, avisamos
        # mostramos por consola los que se borraron
        print(f"archivos huerfanos eliminados: {eliminados}")
        cursor.close()
        conn.close()
    except Exception as e:
        # si algo explota, lo mostramos por consola
        print(f"error al limpiar archivos huerfanos: {e}")
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}


def allowed_file(filename):
    # aca chequeamos que el archivo tenga extension permitida
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
