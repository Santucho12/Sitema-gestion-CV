from flask_httpauth import HTTPBasicAuth
from config import Config

auth = HTTPBasicAuth()

users = {
    Config.AUTH_USERNAME: Config.AUTH_PASSWORD
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
