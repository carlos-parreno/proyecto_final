# routes/grafos_routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from grafos import calcular_ruta_optima, get_all_cities_from_db
from flask_login import login_required

# 1. Creamos el Blueprint
# El primer argumento 'grafos' es el nombre del Blueprint.
grafos_bp = Blueprint('grafos', __name__, template_folder='templates')

# 2. Movemos las rutas de app.py aquí y cambiamos @app.route por @grafos_bp.route
@grafos_bp.route('/')
@login_required
def index():
    return redirect(url_for('grafos.ruta_grafos')) # Nótese que ahora es 'grafos.ruta_grafos'

@grafos_bp.route('/grafos')
@login_required
def ruta_grafos():
    origen = request.args.get('origen')
    destino = request.args.get('destino')

    datos_para_plantilla = {}
    ciudades = get_all_cities_from_db()

    if origen and destino:
        if origen == destino:
            datos_para_plantilla = {"error": "La ciudad de origen y destino no pueden ser la misma."}
        else:
            datos_para_plantilla = calcular_ruta_optima(origen, destino)
        
        datos_para_plantilla['origen_seleccionado'] = origen
        datos_para_plantilla['destino_seleccionado'] = destino
    
    datos_para_plantilla['ciudades'] = ciudades
    return render_template('grafos.html', **datos_para_plantilla)