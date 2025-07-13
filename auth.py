# este archivo es para manejar la autenticacion, o sea, quien puede entrar al panel admin
# aca usamos flask_httpauth que te salva la vida para pedir usuario y contrasena

from flask_httpauth import HTTPBasicAuth
from config import Config

# aca creamos la instancia de autenticacion, bien simple
auth = HTTPBasicAuth()

# aca armamos el diccionario de usuarios, solo uno en este caso
users = {
    Config.AUTH_USERNAME: Config.AUTH_PASSWORD
}

# esta funcion verifica si el usuario y la contrasena son correctos
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username