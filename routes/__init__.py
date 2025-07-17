# routes/__init__.py

from .grafos_routes import grafos_bp
from .ciudades_routes import ciudades_bp
from .auth_routes import auth_bp # <-- Importa el nuevo blueprint

def register_blueprints(app):
    """Registra todos los blueprints en la aplicación Flask."""
    app.register_blueprint(grafos_bp)
    app.register_blueprint(ciudades_bp)
    app.register_blueprint(auth_bp) # <-- Registra el nuevo blueprint