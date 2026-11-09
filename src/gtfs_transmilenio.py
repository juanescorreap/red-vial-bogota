"""Adaptador de Gtransporte: del GTFS de TransMilenio al contrato del núcleo.

Construye la red troncal en espacio L (infraestructura) y en espacio P
(viajes directos) según docs/specs/gtransporte.md. Los grafos resultantes
cumplen `pipeline_redes.validar_contrato`.
"""

from __future__ import annotations

import hashlib
import logging
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
from pyproj import Transformer
from shapely.geometry import LineString, Point

log = logging.getLogger(__name__)

CRS = "EPSG:9377"
OPERADORES = ("Transmilenio-Troncal", "Transmilenio-Dual")
DIAS_HABILES = ("monday", "tuesday", "wednesday", "thursday", "friday")
FIN_DE_SEMANA = ("saturday", "sunday")


# ---------------------------------------------------------------------------
# Fuente
# ---------------------------------------------------------------------------

def sha256(ruta: Path) -> str:
    """Huella SHA-256 de un archivo."""
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def obtener_gtfs(url: str, destino: Path, huella: str) -> Path:
    """Descarga el GTFS si no está en `destino` y verifica que sea exactamente la copia esperada."""
    destino = Path(destino)
    if not destino.exists():
        destino.parent.mkdir(parents=True, exist_ok=True)
        log.info("Descargando %s", url)
        urllib.request.urlretrieve(url, destino)
    obtenida = sha256(destino)
    if obtenida != huella:
        raise ValueError(f"El GTFS en {destino} no es la copia esperada: SHA-256 {obtenida}")
    return destino


def segundos(hora: str) -> int:
    """Convierte HH:MM:SS a segundos; el GTFS admite horas mayores a 24."""
    h, m, s = map(int, hora.split(":"))
    return h * 3600 + m * 60 + s


def leer_feed(ruta_zip: Path) -> dict[str, pd.DataFrame]:
    """Tablas del GTFS restringidas a viajes troncales y duales de día hábil."""
    z = zipfile.ZipFile(ruta_zip)
    leer = lambda n, **k: pd.read_csv(z.open(n), dtype=str, encoding="utf-8-sig", **k)
    agency, routes, trips = leer("agency.txt"), leer("routes.txt"), leer("trips.txt")
    stops, calendar = leer("stops.txt"), leer("calendar.txt")

    habil = calendar[(calendar[list(DIAS_HABILES)] == "1").all(axis=1)
                     & (calendar[list(FIN_DE_SEMANA)] == "0").all(axis=1)]
    agencias = set(agency.loc[agency["agency_name"].isin(OPERADORES), "agency_id"])
    routes = routes[routes["agency_id"].isin(agencias)]
    trips = trips[trips["route_id"].isin(routes["route_id"]) & trips["service_id"].isin(habil["service_id"])]

    ids = set(trips["trip_id"])
    partes = [b[b["trip_id"].isin(ids)] for b in leer(
        "stop_times.txt", usecols=["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"],
        chunksize=2_000_000)]
    stop_times = pd.concat(partes, ignore_index=True)
    shapes = leer("shapes.txt")
    shapes = shapes[shapes["shape_id"].isin(set(trips["shape_id"].dropna()))]
    log.info("Feed: %d rutas, %d viajes de día hábil, %d paradas programadas",
             len(routes), len(trips), len(stop_times))
    return {"routes": routes, "trips": trips, "stops": stops, "stop_times": stop_times, "shapes": shapes}


# ---------------------------------------------------------------------------
# Estaciones
# ---------------------------------------------------------------------------

def estaciones(feed: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict[str, str]]:
    """Estaciones troncales atendidas y asignación de cada parada a su estación.

    Las estaciones con el mismo nombre se fusionan: el nodo toma el menor
    `stop_id` y el punto medio de las coordenadas. Devuelve la tabla de
    estaciones originales (con su nodo) y el mapa parada -> nodo.
    """
    stops = feed["stops"].set_index("stop_id")
    padre = feed["stop_times"]["stop_id"].map(stops["parent_station"])
    atendidas = stops.loc[sorted(set(padre.dropna()))].copy()
    atendidas["nombre"] = atendidas["stop_name"].str.strip()
    tr = Transformer.from_crs(4326, CRS, always_xy=True)
    atendidas["x"], atendidas["y"] = tr.transform(atendidas["stop_lon"].astype(float).values,
                                                  atendidas["stop_lat"].astype(float).values)
    atendidas["nodo"] = atendidas.groupby("nombre")["nombre"].transform(lambda s: min(s.index))
    fusionadas = atendidas["nodo"].ne(atendidas.index).sum()
    if fusionadas:
        log.info("Estaciones fusionadas por nombre: %s",
                 sorted(atendidas.loc[atendidas["nodo"] != atendidas.index, "nombre"]))
    parada_a_nodo = stops["parent_station"].dropna().map(atendidas["nodo"]).dropna().to_dict()
    return atendidas, parada_a_nodo


def _agregar_nodos(G: nx.DiGraph, est: pd.DataFrame) -> None:
    for nodo, g in est.groupby("nodo"):
        G.add_node(nodo, x=float(g["x"].mean()), y=float(g["y"].mean()), nombre=g["nombre"].iloc[0],
                   troncal=nodo[:-3])


def _tiempos(feed: dict[str, pd.DataFrame], parada_a_nodo: dict[str, str]) -> pd.DataFrame:
    """Paradas programadas con su nodo, en orden, con tiempos en segundos."""
    st = feed["stop_times"].merge(feed["trips"][["trip_id", "route_id", "shape_id"]], on="trip_id")
    st["nodo"] = st["stop_id"].map(parada_a_nodo)
    st["seq"] = st["stop_sequence"].astype(int)
    st["llegada"] = st["arrival_time"].map(segundos)
    st["salida"] = st["departure_time"].map(segundos)
    return st.sort_values(["trip_id", "seq"]).reset_index(drop=True)


def _atributos_grafo(G: nx.DiGraph, red: str, fuente: str, fecha: str) -> None:
    G.graph.update(red=red, crs=CRS, fuente=fuente, fecha_snapshot=fecha)


# ---------------------------------------------------------------------------
# Espacio L
# ---------------------------------------------------------------------------

def construir_L(feed: dict[str, pd.DataFrame], tolerancia_m: float = 80, max_m: float = 4000,
                fuente: str = "GTFS TransMilenio", fecha: str = "") -> nx.DiGraph:
    """Red troncal en espacio L: estaciones consecutivas sobre el trazado de cada ruta.

    Cada trazado ordena las estaciones a `tolerancia_m` o menos de su línea.
    `length` es la mediana de la distancia sobre los trazados; se descartan
    aristas de más de `max_m`. `travel_time` es la mediana del tiempo programado
    entre salidas consecutivas; sin viajes que paren en ambas, se usa la
    velocidad comercial mediana. `name` es la troncal (prefijo del
    identificador de estación) o la conexión entre dos troncales.
    """
    est, parada_a_nodo = estaciones(feed)
    tr = Transformer.from_crs(4326, CRS, always_xy=True)
    puntos = {sid: (Point(r.x, r.y), r.nodo) for sid, r in est.iterrows()}

    largos = defaultdict(list)
    for _, g in feed["shapes"].groupby("shape_id"):
        g = g.sort_values("shape_pt_sequence", key=lambda s: s.astype(int))
        xs, ys = tr.transform(g["shape_pt_lon"].astype(float).values, g["shape_pt_lat"].astype(float).values)
        linea = LineString(zip(xs, ys))
        cerca = sorted((linea.project(p), nodo) for p, nodo in puntos.values()
                       if linea.distance(p) <= tolerancia_m)
        for (sa, a), (sb, b) in zip(cerca, cerca[1:]):
            if a != b:
                largos[(a, b)].append(sb - sa)

    st = _tiempos(feed, parada_a_nodo)
    sig = st.groupby("trip_id")[["nodo", "salida"]].shift(-1)
    consecutivos = st.assign(b=sig["nodo"], dt=sig["salida"] - st["salida"])
    consecutivos = consecutivos[consecutivos["nodo"].notna() & consecutivos["b"].notna()
                                & (consecutivos["nodo"] != consecutivos["b"])]
    tiempo = consecutivos.groupby(["nodo", "b"])["dt"].median().to_dict()

    G = nx.DiGraph()
    _agregar_nodos(G, est)
    descartadas = 0
    for (a, b), ls in largos.items():
        largo = float(np.median(ls))
        if largo > max_m:
            descartadas += 1
            continue
        ta, tb = G.nodes[a]["troncal"], G.nodes[b]["troncal"]
        nombre = f"Troncal {ta}" if ta == tb else f"Conexión {min(ta, tb)}-{max(ta, tb)}"
        G.add_edge(a, b, length=largo, travel_time=tiempo.get((a, b)), name=nombre)
    log.info("Espacio L: %d aristas, %d descartadas por superar %d m", G.number_of_edges(), descartadas, max_m)

    con_tiempo = [d["length"] / d["travel_time"] for _, _, d in G.edges(data=True)
                  if d["travel_time"] and d["travel_time"] > 0]
    v_mediana = float(np.median(con_tiempo))
    sin_tiempo = 0
    for _, _, d in G.edges(data=True):
        if not d["travel_time"] or d["travel_time"] <= 0:
            d["travel_time"] = d["length"] / v_mediana
            sin_tiempo += 1
        d["travel_time"] = float(d["travel_time"])
        d["speed_kph"] = d["length"] / d["travel_time"] * 3.6
    log.info("Aristas sin viaje que pare en ambas estaciones (tiempo por velocidad mediana %.1f km/h): %d",
             v_mediana * 3.6, sin_tiempo)
    G.graph["aristas_sin_tiempo_programado"] = sin_tiempo
    G.graph["aristas_descartadas_por_longitud"] = descartadas
    _atributos_grafo(G, "Gtransporte L", fuente, fecha)
    return G


# ---------------------------------------------------------------------------
# Espacio P
# ---------------------------------------------------------------------------

def construir_P(feed: dict[str, pd.DataFrame], G_L: nx.DiGraph, franja_pico: tuple[int, int] = (6, 9),
                fuente: str = "GTFS TransMilenio", fecha: str = "") -> nx.DiGraph:
    """Red troncal en espacio P: estaciones unidas si un viaje para en ambas en ese orden.

    `travel_time` es la mediana del tiempo a bordo (salida de a, llegada a b);
    `frecuencia`, los buses por hora que salen de a en la franja pico y paran
    después en b; `length`, el camino más corto por longitud en el espacio L;
    `name`, los códigos de las rutas que unen a con b.
    """
    est, parada_a_nodo = estaciones(feed)
    st = _tiempos(feed, parada_a_nodo)
    st = st[st["nodo"].notna()]
    nombres_ruta = feed["routes"].set_index("route_id")["route_short_name"]
    ini, fin = franja_pico[0] * 3600, franja_pico[1] * 3600
    horas = franja_pico[1] - franja_pico[0]

    tiempos, conteo_pico, rutas = defaultdict(list), defaultdict(int), defaultdict(set)
    for _, g in st.groupby("trip_id", sort=False):
        nodos, sal, lle = g["nodo"].to_numpy(), g["salida"].to_numpy(), g["llegada"].to_numpy()
        ruta = nombres_ruta[g["route_id"].iloc[0]]
        for i in range(len(nodos) - 1):
            en_pico = ini <= sal[i] < fin
            vistos = set()
            for j in range(i + 1, len(nodos)):
                a, b = nodos[i], nodos[j]
                if a == b or b in vistos:
                    continue
                vistos.add(b)
                tiempos[(a, b)].append(lle[j] - sal[i])
                rutas[(a, b)].add(ruta)
                if en_pico:
                    conteo_pico[(a, b)] += 1

    largo_L = dict(nx.all_pairs_dijkstra_path_length(G_L, weight="length"))
    G = nx.DiGraph()
    _agregar_nodos(G, est)
    for (a, b), ts in tiempos.items():
        if b not in largo_L.get(a, {}):
            continue
        G.add_edge(a, b, travel_time=float(max(np.median(ts), 1.0)), length=float(largo_L[a][b]),
                   frecuencia=conteo_pico[(a, b)] / horas, name=" / ".join(sorted(rutas[(a, b)])))
    log.info("Espacio P: %d aristas", G.number_of_edges())
    _atributos_grafo(G, "Gtransporte P", fuente, fecha)
    return G


def resumen_troncales(G: nx.DiGraph) -> pd.DataFrame:
    """Estaciones por troncal (prefijo del identificador), con ejemplos de nombres."""
    filas = defaultdict(list)
    for _, d in G.nodes(data=True):
        filas[d["troncal"]].append(d["nombre"])
    return pd.DataFrame([{"troncal": t, "estaciones": len(n), "ejemplos": "; ".join(sorted(n)[:4])}
                         for t, n in sorted(filas.items(), key=lambda x: int(x[0]))])
