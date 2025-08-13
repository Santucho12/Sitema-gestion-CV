import psycopg2
from psycopg2 import OperationalError
from config import Config
import logging

logging.basicConfig(level=logging.INFO)

def get_db_connection():
    """Intenta conectar con la base de datos PostgreSQL y devuelve la conexión"""
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            dbname=Config.DB_NAME,
            port=Config.DB_PORT
        )
        logging.info("Conexión a la base de datos exitosa")
        return conn
    except OperationalError as err:
        logging.error(f"Error de conexión a la base de datos: {err}")
        return None
