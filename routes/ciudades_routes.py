# routes/ciudades_routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from grafos import get_all_cities_from_db, add_city_to_db, delete_city_from_db
from flask_login import login_required

# 1. Creamos el Blueprint
ciudades_bp = Blueprint('ciudades', __name__, template_folder='templates')

# 2. Movemos las rutas aquí
@ciudades_bp.route('/ciudades', methods=['GET', 'POST'])
@login_required
def gestionar_ciudades():
    if request.method == 'POST':
        nombre_nueva_ciudad = request.form.get('nombre_ciudad')
        conexiones_seleccionadas = request.form.getlist('conexiones_check')
        conexiones_con_distancia = {}
        for ciudad_a_conectar in conexiones_seleccionadas:
            distancia = request.form.get(f'distancia_{ciudad_a_conectar}')
            if distancia:
                conexiones_con_distancia[ciudad_a_conectar] = distancia
        
        if nombre_nueva_ciudad:
            add_city_to_db(nombre_nueva_ciudad, conexiones_con_distancia)
        
        return redirect(url_for('ciudades.gestionar_ciudades'))

    ciudades_existentes = get_all_cities_from_db()
    return render_template('gestionar_ciudades.html', ciudades_existentes=ciudades_existentes)

@ciudades_bp.route('/ciudades/eliminar/<string:nombre_ciudad>', methods=['POST'])
@login_required
def eliminar_ciudad(nombre_ciudad):
    delete_city_from_db(nombre_ciudad)
    return redirect(url_for('ciudades.gestionar_ciudades'))