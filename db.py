import mysql.connector
from config import Config
import logging

logging.basicConfig(level=logging.INFO)

def get_db_connection():
    # aca intentamos conectar con la base, si sale todo bien avisamos
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        logging.info("conexion a la base de datos exitosa")
        return conn
    except mysql.connector.Error as err:
        # si explota algo, lo mostramos y devolvemos None
        logging.error(f"error de conexion a la base de datos: {err}")
        return None
