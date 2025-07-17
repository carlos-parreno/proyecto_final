# grafos.py
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

from database import db
from models import City, Route

# --- FUNCIONES QUE INTERACTÚAN CON LA DB ---

def get_all_cities_from_db():
    """Obtiene todas las ciudades de la base de datos."""
    ciudades_obj = City.query.order_by(City.name).all()
    return [city.name for city in ciudades_obj]

def add_city_to_db(nombre_ciudad, conexiones):
    """Añade una ciudad y sus rutas a la base de datos."""
    if City.query.filter_by(name=nombre_ciudad).first():
        return

    nueva_ciudad = City(name=nombre_ciudad)
    db.session.add(nueva_ciudad)
    db.session.commit()

    for ciudad_existente_nombre, distancia in conexiones.items():
        try:
            peso = int(distancia)
            if peso > 0:
                ciudad_existente_obj = City.query.filter_by(name=ciudad_existente_nombre).one()
                ruta1 = Route(origin=nueva_ciudad, destination=ciudad_existente_obj, distance=peso)
                ruta2 = Route(origin=ciudad_existente_obj, destination=nueva_ciudad, distance=peso)
                db.session.add(ruta1)
                db.session.add(ruta2)
        except (ValueError, TypeError):
            continue
    db.session.commit()

def delete_city_from_db(nombre_ciudad):
    """Elimina una ciudad y todas sus rutas asociadas."""
    ciudad_a_borrar = City.query.filter_by(name=nombre_ciudad).first()
    if ciudad_a_borrar:
        Route.query.filter((Route.origin_id == ciudad_a_borrar.id) | (Route.destination_id == ciudad_a_borrar.id)).delete()
        db.session.delete(ciudad_a_borrar)
        db.session.commit()

def build_graph_from_db():
    """Construye un objeto grafo de NetworkX a partir de los datos de la DB."""
    G = nx.Graph()
    rutas = Route.query.all()
    for ruta in rutas:
        G.add_edge(ruta.origin.name, ruta.destination.name, weight=ruta.distance)
    return G

def calcular_ruta_optima(origen, destino):
    """Construye el grafo desde la DB y calcula la ruta."""
    G = build_graph_from_db()
    ciudades = sorted(list(G.nodes()))

    try:
        camino = nx.dijkstra_path(G, source=origen, target=destino)
        costo = nx.dijkstra_path_length(G, source=origen, target=destino)

        pos = nx.spring_layout(G, seed=42, k=0.9)
        plt.figure(figsize=(13, 9))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2200, font_size=10, font_weight='bold')
        path_edges = list(zip(camino, camino[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=camino, node_color='tomato', node_size=2300)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='tomato', width=3)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title(f"Ruta más corta de {origen} a {destino}", size=15)
        
        ruta_imagen = os.path.join('static', 'img', 'grafo_ruta.png')
        directorio_imagen = os.path.dirname(ruta_imagen)
        os.makedirs(directorio_imagen, exist_ok=True)
        plt.savefig(ruta_imagen)
        plt.close()

        costera = {'Manta', 'Portoviejo', 'Guayaquil'}
        interseccion = set(camino).intersection(costera)
        mensaje_costera = f"✅ El camino pasa por: {', '.join(interseccion)}" if interseccion else "❌ El camino NO pasa por ninguna ciudad costera."

        return {
            "ciudades": ciudades, "camino": camino, "costo": costo,
            "mensaje_costera": mensaje_costera, "ruta_imagen": "img/grafo_ruta.png", "error": None
        }
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return {"ciudades": ciudades, "error": f"No existe una ruta posible entre {origen} y {destino}."}