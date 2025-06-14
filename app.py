import os
from flask import Flask
from config import Config
from auth import auth  # importás la instancia ya creada
from routes.main import main_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # NO hace falta auth.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
