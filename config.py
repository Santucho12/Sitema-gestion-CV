# este archivo es el corazon de la config, aca esta lo importante asi no te volves loco buscando datos
import os
from dotenv import load_dotenv  # esto sirve para cargar las variables del archivo .env

load_dotenv()  # aca cargamos las variables de entorno, tipo claves y contras

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # aca sacamos la ruta base del proyecto

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')  # clave secreta para flask, para que no te hackeen
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')  # aca van los archivos que suben los usuarios
    AUTH_USERNAME = os.getenv('AUTH_USERNAME')  # usuario para entrar al panel admin
    AUTH_PASSWORD = os.getenv('AUTH_PASSWORD')  # contrasena para el panel admin

    DB_HOST = os.getenv('DB_HOST')  # host de la base de datos
    DB_USER = os.getenv('DB_USER')  # usuario de la base
    DB_PASSWORD = os.getenv('DB_PASSWORD')  # contrasena de la base
    DB_NAME = os.getenv('DB_NAME')  # nombre de la base
    DB_PORT = int(os.getenv('DB_PORT', 5432))  # puerto, 5432 por defecto para PostgreSQL

    # URI para SQLAlchemy usando PostgreSQL
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # esto es para que no te tire warnings al usar sqlalchemy
