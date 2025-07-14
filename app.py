# este archivo es el que arranca todo, es como el motor del sistema
# aca se arma la app flask y se conectan todos puzzle

import os
from flask import Flask
from config import Config
from auth import auth  # importas la instancia ya creada
from routes.main import main_bp
from routes.admin import admin_bp

# funcion para crear la app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  #la config que armamos antes

    app.register_blueprint(main_bp)  # conectamos las rutas principales
    app.register_blueprint(admin_bp)  # conectamos las rutas del admin

    # si no existe la carpeta uploads, la creamos para guardar los archivos
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    return app  # devolvemos la app lista para usar

 #se arranca el servidor
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)  # esto lo pone en modo debug,para ver todo lo que pasa