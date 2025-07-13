# este archivo es para manejar la autenticacion, quien puede entrar al panel admin
# aca usamos flask_httpauth para pedir usuario y contrasena

from flask_httpauth import HTTPBasicAuth
from config import Config

# instancia de autenticacion
auth = HTTPBasicAuth()

#armamos el diccionario de usuarios, solo uno en este caso
users = {
    Config.AUTH_USERNAME: Config.AUTH_PASSWORD
}

# esta funcion verifica si el usuario y la contrasena son correctos
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username