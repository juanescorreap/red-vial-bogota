"""Descarga de OpenStreetMap las estaciones y el trazado de la Línea 1 del Metro de Bogotá.

Uso, desde la raíz del repo y con el .venv activado:
    python scripts/descargar_metro_osm.py data/raw/metro_l1

Guarda lo encontrado en un GeoJSON con la fecha en el nombre e imprime un resumen.
"""

import sys
from datetime import date
from pathlib import Path

import osmnx as ox
import pandas as pd

destino = Path(sys.argv[1])
destino.mkdir(parents=True, exist_ok=True)

# Etiquetas con que OSM suele marcar líneas y estaciones de metro, en servicio o en construcción
ETIQUETAS = {
    "railway": ["subway", "light_rail", "construction", "proposed", "station", "halt", "stop"],
    "construction:railway": True,
    "construction": ["subway", "light_rail", "rail", "station"],
    "station": ["subway", "light_rail"],
}

objetos = ox.features_from_place("Bogotá, Colombia", tags=ETIQUETAS)
columnas = [c for c in ["name", "railway", "construction", "construction:railway", "station",
                        "public_transport", "operator", "network", "line", "ref"] if c in objetos.columns]
objetos = objetos[columnas + ["geometry"]].copy()

# Solo lo que parece metro: descarta trenes de carga, tranvías antiguos y similares
texto = objetos[columnas].apply(lambda fila: " ".join(str(v) for v in fila if pd.notna(v)), axis=1).str.lower()
metro = objetos[texto.str.contains("metro|subway|línea 1|linea 1|light_rail")]

archivo = destino / f"osm_metro_l1_{date.today():%Y-%m-%d}.geojson"
salida = metro.reset_index()
for c in salida.columns:
    if c != "geometry":
        salida[c] = salida[c].astype(str)
salida.to_file(archivo, driver="GeoJSON")

pd.set_option("display.width", 200)
pd.set_option("display.max_rows", 200)
print(f"Objetos con etiquetas ferroviarias: {len(objetos)} | que parecen metro: {len(metro)}")
print(f"Guardado en {archivo}\n")
print("Por tipo de geometría y etiqueta railway:")
print(metro.assign(geom=metro.geometry.geom_type).groupby(["geom", "railway"], dropna=False).size().to_string(), "\n")
puntos = metro[metro.geometry.geom_type.isin(["Point", "Polygon", "MultiPolygon"])]
print(f"Posibles estaciones ({len(puntos)}):")
print(puntos[[c for c in columnas if c in puntos.columns]].to_string())
