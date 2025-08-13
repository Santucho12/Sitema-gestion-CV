import os
from flask import Flask
from config import Config
from auth import auth  # importas la instancia ya creada
from routes.main import main_bp
from routes.admin import admin_bp
#f
# funcion para crear la app
def create_app():
    # Creamos la app con static_url_path para que sirva estáticos desde /postularse/static
    app = Flask(__name__, static_url_path='/postularse/static')
    app.config.from_object(Config)  # la config que armamos antes

    # Registramos los blueprints sin prefijo para rutas directas
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # si no existe la carpeta uploads, la creamos para guardar los archivos
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    return app  # devolvemos la app lista para usar

# Creamos la instancia de la aplicación a nivel global para que Passenger la encuentre
app = create_app()

# se arranca el servidor (solo para desarrollo local)
if __name__ == '__main__':
    app.run(debug=True)
