import mysql.connector
from config import Config
import logging

logging.basicConfig(level=logging.INFO)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        logging.info("Conexión a la base de datos exitosa.")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Error de conexión a la base de datos: {err}")
        return None
