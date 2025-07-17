# models/user.py
from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# UserMixin nos da funcionalidades por defecto de Flask-Login
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # Aumentado a 256 por hashes largos

    def set_password(self, password):
        """Crea un hash de la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica el hash de la contraseña."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'