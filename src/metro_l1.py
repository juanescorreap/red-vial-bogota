"""Intervención Metro Línea 1 sobre el espacio L de Gtransporte.

Las estaciones salen de OpenStreetMap (red "Metro de Bogotá"). La línea se
agrega como nodos nuevos unidos en secuencia, con enlaces de transbordo a
las estaciones de TransMilenio cercanas.
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd

RED_METRO = "Metro de Bogotá"


def estaciones_osm(ruta_geojson: Path, inicio: str, crs: str = "EPSG:9377") -> pd.DataFrame:
    """Estaciones de la Línea 1 en orden de recorrido desde la estación `inicio`.

    El orden se obtiene encadenando cada estación con la más cercana aún no
    visitada. Devuelve nombre, x, y y la distancia en línea recta a la
    siguiente estación.
    """
    g = gpd.read_file(ruta_geojson).to_crs(crs)
    cols = [c for c in g.columns if c != "geometry"]
    texto = g[cols].apply(lambda r: " ".join(str(v) for v in r if pd.notna(v)), axis=1)
    est = g[(g["railway"] == "station") & texto.str.contains(RED_METRO)]
    xy = {n: np.array([p.x, p.y]) for n, p in zip(est["name"], est.geometry.centroid)}
    if inicio not in xy:
        raise ValueError(f"No hay una estación llamada {inicio}")
    orden, resto = [inicio], set(xy) - {inicio}
    while resto:
        sig = min(resto, key=lambda n: np.linalg.norm(xy[orden[-1]] - xy[n]))
        orden.append(sig)
        resto.remove(sig)
    tabla = pd.DataFrame({"nombre": orden, "x": [xy[n][0] for n in orden], "y": [xy[n][1] for n in orden]})
    tabla["dist_sig_m"] = np.hypot(tabla["x"].diff(-1), tabla["y"].diff(-1))
    return tabla


def factor_trazado(ruta_geojson: Path, estaciones: pd.DataFrame, nombre_linea: str = "Línea 1",
                   crs: str = "EPSG:9377") -> float:
    """Razón entre la longitud de la vía (mitad del trazado de doble vía) y la suma de distancias rectas entre estaciones."""
    g = gpd.read_file(ruta_geojson).to_crs(crs)
    via = g[(g["name"] == nombre_linea) & (g["railway"] == "construction")].length.sum() / 2
    return float(via / estaciones["dist_sig_m"].sum())


def agregar_metro(G: nx.DiGraph, estaciones: pd.DataFrame, minutos_recorrido: float, factor: float,
                  radio_transbordo_m: float, segundos_transbordo: float) -> tuple[nx.DiGraph, pd.DataFrame]:
    """Copia del espacio L con la Línea 1 y sus transbordos.

    Cada tramo entre estaciones consecutivas tiene longitud igual a la
    distancia recta por `factor`, y un tiempo proporcional a su longitud de
    modo que el recorrido completo dure `minutos_recorrido`. Cada estación de
    metro se une en ambos sentidos con las estaciones de TransMilenio a
    `radio_transbordo_m` o menos, con tiempo `segundos_transbordo`.
    Devuelve el grafo y la tabla de transbordos.
    """
    H = G.copy()
    ids = [f"M{i:02d}" for i in range(1, len(estaciones) + 1)]
    for nodo, fila in zip(ids, estaciones.itertuples()):
        H.add_node(nodo, x=float(fila.x), y=float(fila.y), nombre=fila.nombre, troncal="Metro")

    largos = (estaciones["dist_sig_m"].iloc[:-1] * factor).to_numpy()
    seg_por_m = minutos_recorrido * 60 / largos.sum()
    for (a, b), largo in zip(zip(ids, ids[1:]), largos):
        for u, v in ((a, b), (b, a)):
            H.add_edge(u, v, length=float(largo), travel_time=float(largo * seg_por_m),
                       speed_kph=float(3.6 / seg_por_m), name="Metro L1")

    tm = [(n, d) for n, d in G.nodes(data=True)]
    transbordos = []
    for nodo in ids:
        xm, ym = H.nodes[nodo]["x"], H.nodes[nodo]["y"]
        for n, d in tm:
            dist = float(np.hypot(float(d["x"]) - xm, float(d["y"]) - ym))
            if dist <= radio_transbordo_m:
                transbordos.append({"metro": H.nodes[nodo]["nombre"], "transmilenio": d.get("nombre", n),
                                    "nodo_metro": nodo, "nodo_tm": n, "distancia_m": dist})
                for u, v in ((nodo, n), (n, nodo)):
                    H.add_edge(u, v, length=max(dist, 1.0), travel_time=float(segundos_transbordo),
                               speed_kph=max(dist, 1.0) / segundos_transbordo * 3.6, name="Transbordo Metro")
    H.graph["red"] = f"{G.graph.get('red', 'Gtransporte L')} con Metro L1"
    return H, pd.DataFrame(transbordos)
