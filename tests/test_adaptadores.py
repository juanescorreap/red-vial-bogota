"""Pruebas de los adaptadores de TransMilenio y de la Línea 1 con datos sintéticos."""

import zipfile

import geopandas as gpd
import networkx as nx
import pandas as pd
import pytest
from pyproj import Transformer
from shapely.geometry import LineString, Point

import gtfs_transmilenio as gt
import metro_l1 as ml
import pipeline_redes as pr

LAT = "4.6"
LONS = ["-74.100", "-74.090", "-74.080"]          # tres estaciones a unos 1,1 km entre sí
EST = ["10001", "10002", "10003"]                 # troncal 10


def feed_sintetico() -> dict[str, pd.DataFrame]:
    """Tres estaciones en línea; la ruta 1 para en todas y la E1 es un expreso de la primera a la tercera."""
    stops = pd.DataFrame(
        [{"stop_id": e, "stop_name": f"Estación {i + 1}", "stop_lat": LAT, "stop_lon": lon,
          "location_type": "1", "parent_station": None} for i, (e, lon) in enumerate(zip(EST, LONS))]
        + [{"stop_id": f"S{i + 1}", "stop_name": f"Vagón {i + 1}", "stop_lat": LAT, "stop_lon": lon,
            "location_type": "0", "parent_station": e} for i, (e, lon) in enumerate(zip(EST, LONS))])
    shapes = pd.DataFrame(
        [{"shape_id": "IDA", "shape_pt_sequence": str(k), "shape_pt_lat": LAT, "shape_pt_lon": lon}
         for k, lon in enumerate(LONS, 1)]
        + [{"shape_id": "VUELTA", "shape_pt_sequence": str(k), "shape_pt_lat": LAT, "shape_pt_lon": lon}
           for k, lon in enumerate(reversed(LONS), 1)])
    trips = pd.DataFrame([
        {"trip_id": "T1", "route_id": "R1", "service_id": "1", "shape_id": "IDA"},
        {"trip_id": "T2", "route_id": "R1", "service_id": "1", "shape_id": "VUELTA"},
        {"trip_id": "T3", "route_id": "R2", "service_id": "1", "shape_id": "IDA"},
        {"trip_id": "T4", "route_id": "R2", "service_id": "1", "shape_id": "VUELTA"},
    ])
    paradas = [("T1", "S1", "08:00:00"), ("T1", "S2", "08:03:00"), ("T1", "S3", "08:06:00"),
               ("T2", "S3", "08:00:00"), ("T2", "S2", "08:03:00"), ("T2", "S1", "08:06:00"),
               ("T3", "S1", "07:00:00"), ("T3", "S3", "07:04:00"),
               ("T4", "S3", "07:00:00"), ("T4", "S1", "07:04:00")]
    stop_times = pd.DataFrame([{"trip_id": t, "stop_id": s, "arrival_time": h, "departure_time": h,
                                "stop_sequence": str(k)}
                               for k, (t, s, h) in enumerate(paradas)])
    routes = pd.DataFrame([{"route_id": "R1", "agency_id": "1", "route_short_name": "1"},
                           {"route_id": "R2", "agency_id": "1", "route_short_name": "E1"}])
    return {"routes": routes, "trips": trips, "stops": stops, "stop_times": stop_times, "shapes": shapes}


# --- GTFS: utilidades ---

def test_segundos_admite_horas_mayores_a_24():
    assert gt.segundos("25:10:00") == 25 * 3600 + 600


def test_obtener_gtfs_rechaza_copia_distinta(tmp_path):
    archivo = tmp_path / "gtfs.zip"
    archivo.write_bytes(b"no es la copia")
    with pytest.raises(ValueError, match="SHA-256"):
        gt.obtener_gtfs("https://no.se.descarga", archivo, "0" * 64)


def test_leer_feed_filtra_operador_y_dia_habil(tmp_path):
    f = feed_sintetico()
    agency = pd.DataFrame([{"agency_id": "1", "agency_name": "Transmilenio-Troncal"},
                           {"agency_id": "2", "agency_name": "Zonal-Urbano"}])
    dias = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    calendar = pd.DataFrame([{"service_id": "1", **{d: "1" if d not in ("saturday", "sunday") else "0" for d in dias}},
                             {"service_id": "2", **{d: "1" if d == "saturday" else "0" for d in dias}}])
    routes = pd.concat([f["routes"], pd.DataFrame([{"route_id": "R9", "agency_id": "2", "route_short_name": "Z"}])])
    trips = pd.concat([f["trips"], pd.DataFrame([
        {"trip_id": "T5", "route_id": "R1", "service_id": "2", "shape_id": "IDA"},
        {"trip_id": "T6", "route_id": "R9", "service_id": "1", "shape_id": "IDA"}])])
    ruta = tmp_path / "feed.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        for nombre, df in {"agency": agency, "calendar": calendar, "routes": routes, "trips": trips,
                           "stops": f["stops"], "stop_times": f["stop_times"], "shapes": f["shapes"]}.items():
            z.writestr(f"{nombre}.txt", df.to_csv(index=False))
    feed = gt.leer_feed(ruta)
    assert set(feed["trips"]["trip_id"]) == {"T1", "T2", "T3", "T4"}
    assert set(feed["routes"]["route_id"]) == {"R1", "R2"}


# --- Espacio L ---

def test_espacio_L_el_expreso_no_crea_tramo_fisico():
    G = gt.construir_L(feed_sintetico(), fecha="2026-01-01")
    pr.validar_contrato(G)
    assert set(G.edges()) == {("10001", "10002"), ("10002", "10003"), ("10003", "10002"), ("10002", "10001")}
    assert not G.has_edge("10001", "10003")


def test_espacio_L_tiempo_programado_longitud_y_nombre():
    G = gt.construir_L(feed_sintetico(), fecha="2026-01-01")
    d = G.edges["10001", "10002"]
    assert d["travel_time"] == pytest.approx(180)
    assert 1000 < d["length"] < 1200                 # unos 1,1 km sobre el trazado
    assert d["name"] == "Troncal 10"
    assert G.graph["aristas_sin_tiempo_programado"] == 0


def test_espacio_L_descarta_aristas_largas():
    G = gt.construir_L(feed_sintetico(), max_m=500, fecha="2026-01-01")
    assert G.number_of_edges() == 0 and G.graph["aristas_descartadas_por_longitud"] == 4


# --- Espacio P ---

def test_espacio_P_une_estaciones_de_una_misma_ruta():
    f = feed_sintetico()
    G_L = gt.construir_L(f, fecha="2026-01-01")
    G_P = gt.construir_P(f, G_L, fecha="2026-01-01")
    pr.validar_contrato(G_P)
    assert G_P.number_of_edges() == 6 and G_P.has_edge("10001", "10003")
    d = G_P.edges["10001", "10003"]
    assert d["travel_time"] == pytest.approx(300)    # mediana de 360 s (ruta 1) y 240 s (expreso)
    assert d["name"] == "1 / E1"
    assert d["frecuencia"] == pytest.approx(2 / 3)   # 2 viajes entre 6:00 y 9:00
    assert d["length"] == pytest.approx(G_L.edges["10001", "10002"]["length"] + G_L.edges["10002", "10003"]["length"])


# --- Línea 1 del metro ---

def metro_geojson(ruta):
    """Tres estaciones de metro desordenadas, una de RegioTram y la vía de doble carril."""
    filas = [
        {"name": "E2", "railway": "station", "network": "Metro de Bogotá", "geometry": Point(-74.09, 4.6)},
        {"name": "E3", "railway": "station", "network": "Metro de Bogotá", "geometry": Point(-74.08, 4.6)},
        {"name": "E1", "railway": "station", "network": "Metro de Bogotá", "geometry": Point(-74.10, 4.6)},
        {"name": "Otra", "railway": "station", "network": "RegioTram", "geometry": Point(-74.05, 4.6)},
        {"name": "Línea 1", "railway": "construction", "network": "Metro de Bogotá",
         "geometry": LineString([(-74.10, 4.6), (-74.08, 4.6)])},
        {"name": "Línea 1", "railway": "construction", "network": "Metro de Bogotá",
         "geometry": LineString([(-74.08, 4.6), (-74.10, 4.6)])},
    ]
    gpd.GeoDataFrame(filas, crs=4326).to_file(ruta, driver="GeoJSON")
    return ruta


def test_estaciones_osm_ordena_y_excluye_otras_redes(tmp_path):
    est = ml.estaciones_osm(metro_geojson(tmp_path / "metro.geojson"), "E1")
    assert list(est["nombre"]) == ["E1", "E2", "E3"]
    assert est["dist_sig_m"].iloc[0] == pytest.approx(1110, rel=0.02)


def test_factor_trazado_de_via_recta_es_uno(tmp_path):
    ruta = metro_geojson(tmp_path / "metro.geojson")
    est = ml.estaciones_osm(ruta, "E1")
    assert ml.factor_trazado(ruta, est) == pytest.approx(1.0, rel=0.01)


def test_agregar_metro_tramos_tiempos_y_transbordos(tmp_path):
    est = ml.estaciones_osm(metro_geojson(tmp_path / "metro.geojson"), "E1")
    x3, y3 = Transformer.from_crs(4326, 9377, always_xy=True).transform(-74.08, 4.6)
    G = nx.DiGraph(red="TM", crs="EPSG:9377", fuente="sintética", fecha_snapshot="2026-01-01")
    G.add_node("TM1", x=x3 + 100, y=y3, nombre="Cerca")
    G.add_node("TM2", x=x3 + 5000, y=y3, nombre="Lejos")
    for u, v in (("TM1", "TM2"), ("TM2", "TM1")):
        G.add_edge(u, v, length=4900.0, travel_time=600.0, name="Troncal 1")
    H, transbordos = ml.agregar_metro(G, est, minutos_recorrido=10, factor=1.0,
                                      radio_transbordo_m=400, segundos_transbordo=300)
    pr.validar_contrato(H)
    assert list(transbordos["transmilenio"]) == ["Cerca"]
    tiempo_total = H.edges["M01", "M02"]["travel_time"] + H.edges["M02", "M03"]["travel_time"]
    assert tiempo_total == pytest.approx(600)
    assert H.edges["M03", "TM1"]["travel_time"] == 300 and H.has_edge("TM1", "M03")
    assert not G.has_node("M01")                     # el grafo original no cambia
