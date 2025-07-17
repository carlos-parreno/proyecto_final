# app.py

from flask import Flask
from flask_login import LoginManager # <-- Importa LoginManager
from database import db
from routes import register_blueprints
from models import User # <-- Importa el modelo User

app = Flask(__name__)
app.secret_key = 'tu-clave-secreta-aqui' # <-- Flask-Login necesita esto

# --- CONFIGURACIÓN ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/grafos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- INICIALIZACIÓN DE EXTENSIONES ---
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # <-- Redirige a esta ruta si no está logueado

@login_manager.user_loader
def load_user(user_id):
    """Función que Flask-Login usa para cargar un usuario por su ID."""
    return User.query.get(int(user_id))

# Registramos todos nuestros blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)