"""Adaptador de Gvial: del .graphml de OSMnx al contrato del núcleo."""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import osmnx as ox

import pipeline_redes as pr


def cargar_gvial(carpeta: Path, nombre_archivo: str, red: str) -> tuple[nx.MultiDiGraph, nx.DiGraph]:
    """Carga un .graphml del snapshot y devuelve el grafo original y el grafo del contrato.

    El grafo del contrato es dirigido sin aristas paralelas (conserva la de
    menor tiempo), con nombres de texto y los atributos de origen.
    """
    rutas = sorted(Path(carpeta).glob(f"{nombre_archivo}.graphml*"))
    if len(rutas) != 1:
        raise FileNotFoundError(f"Se esperaba un {nombre_archivo}.graphml en {carpeta}, hay {len(rutas)}")
    G_osm = ox.load_graphml(rutas[0])
    G = ox.convert.to_digraph(G_osm, weight="travel_time")
    for _, _, d in G.edges(data=True):
        d["name"] = pr.normalizar_nombre(d.get("name"))
    G.graph.update(
        red=red,
        crs=str(G_osm.graph.get("crs")),
        fuente=f"OpenStreetMap vía {G_osm.graph.get('created_with')}",
        fecha_snapshot=G_osm.graph.get("created_date"),
    )
    pr.validar_contrato(G)
    return G_osm, G
