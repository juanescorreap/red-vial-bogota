"""Núcleo del análisis de redes de movilidad de Bogotá.

Las funciones reciben el grafo y sus parámetros como argumentos y no leen
variables globales, para que el mismo código sirva para Gvial y Gtransporte.
Todo grafo debe cumplir el contrato de `validar_contrato` antes de entrar.

No importa OSMnx: la conversión de cada fuente al contrato vive en el
adaptador de cada red (notebooks 01_gvial y 02_gtransporte).
"""

from __future__ import annotations

import logging
import random
from collections.abc import Mapping, Sequence

import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

log = logging.getLogger(__name__)

SIN_NOMBRE = "sin nombre"
SEPARADOR_NOMBRES = " / "
ATRIBUTOS_GRAFO = ("red", "crs", "fuente", "fecha_snapshot")


# ---------------------------------------------------------------------------
# Contrato del grafo
# ---------------------------------------------------------------------------

def normalizar_nombre(nombre: object) -> str:
    """Convierte el nombre de un tramo a texto.

    OSM puede traer una lista de nombres cuando un tramo une vías; se ordenan y
    se unen con " / ". Un nombre ausente o vacío queda como "sin nombre".
    """
    if isinstance(nombre, (list, tuple, set)):
        nombres = sorted({str(n) for n in nombre if str(n).strip()})
        return SEPARADOR_NOMBRES.join(nombres) if nombres else SIN_NOMBRE
    if nombre is None or (isinstance(nombre, float) and np.isnan(nombre)):
        return SIN_NOMBRE
    texto = str(nombre).strip()
    return texto if texto else SIN_NOMBRE


def validar_contrato(G: nx.DiGraph) -> None:
    """Verifica que el grafo tenga la forma que espera el núcleo.

    Falla con ValueError y la lista de incumplimientos. Reglas:
    DiGraph sin aristas paralelas, una sola componente fuertemente conexa,
    nodos con `x` e `y`, aristas con `length` y `travel_time` positivos y
    `name` de texto no vacío, y atributos de grafo `red`, `crs`, `fuente` y
    `fecha_snapshot`.
    """
    errores: list[str] = []

    if not isinstance(G, nx.DiGraph) or G.is_multigraph():
        errores.append(f"debe ser nx.DiGraph sin aristas paralelas, es {type(G).__name__}")
    if G.number_of_nodes() == 0:
        raise ValueError("Contrato incumplido: el grafo no tiene nodos")
    if not nx.is_strongly_connected(G):
        n_comp = nx.number_strongly_connected_components(G)
        errores.append(f"debe ser fuertemente conexo, tiene {n_comp} componentes")

    faltan_graf = [a for a in ATRIBUTOS_GRAFO if a not in G.graph]
    if faltan_graf:
        errores.append(f"faltan atributos del grafo: {faltan_graf}")

    nodos_sin_xy = sum(1 for _, d in G.nodes(data=True) if "x" not in d or "y" not in d)
    if nodos_sin_xy:
        errores.append(f"{nodos_sin_xy} nodos sin x o y")

    for attr in ("length", "travel_time"):
        malas = sum(
            1 for _, _, d in G.edges(data=True)
            if not isinstance(d.get(attr), (int, float)) or not d[attr] > 0
        )
        if malas:
            errores.append(f"{malas} aristas con {attr} ausente, no numérico o no positivo")

    nombres_malos = sum(
        1 for _, _, d in G.edges(data=True)
        if not isinstance(d.get("name"), str) or not d["name"].strip()
    )
    if nombres_malos:
        errores.append(f"{nombres_malos} aristas con name ausente o que no es texto")

    if errores:
        raise ValueError("Contrato incumplido:\n- " + "\n- ".join(errores))
    log.info("Contrato OK: %s, N=%d, M=%d", G.graph["red"], G.number_of_nodes(), G.number_of_edges())


# ---------------------------------------------------------------------------
# Estructura
# ---------------------------------------------------------------------------

def muestrear_nodos(G: nx.DiGraph, n: int, seed: int) -> list:
    """Muestra reproducible de hasta `n` nodos, en el orden de G.nodes."""
    return random.Random(seed).sample(list(G.nodes), min(n, G.number_of_nodes()))


def estructura(G: nx.DiGraph, n_fuentes: int = 500, seed: int = 42) -> dict:
    """Métricas estructurales de la red.

    Grado medio y clustering se calculan sobre la versión no dirigida. El
    tiempo medio de viaje es el promedio de los caminos más cortos por
    `travel_time` (segundos) desde `n_fuentes` nodos muestreados, en minutos.
    """
    U = G.to_undirected()
    N = G.number_of_nodes()
    fuentes = muestrear_nodos(G, n_fuentes, seed)
    tiempos = [
        t for s in fuentes
        for v, t in nx.single_source_dijkstra_path_length(G, s, weight="travel_time").items()
        if v != s
    ]
    return {
        "N": N,
        "M": G.number_of_edges(),
        "grado_medio": 2 * U.number_of_edges() / N,
        "clustering": nx.average_clustering(U),
        "tiempo_medio_min": sum(tiempos) / len(tiempos) / 60,
    }


# ---------------------------------------------------------------------------
# Intermediación y concentración
# ---------------------------------------------------------------------------

def intermediacion(G: nx.DiGraph, peso: str, k: int | None = None, seed: int = 42) -> dict:
    """Intermediación de aristas: exacta si k es None, muestreada con k fuentes si no."""
    if k is not None:
        k = min(k, G.number_of_nodes())
    return nx.edge_betweenness_centrality(G, k=k, weight=peso, seed=seed)


def tabla_tramos(G: nx.DiGraph, intermediaciones: Mapping[str, Mapping]) -> pd.DataFrame:
    """Una fila por arista con su nombre, longitud e intermediaciones.

    `intermediaciones` asocia el nombre de cada columna de salida con un
    diccionario {(u, v): valor}, por ejemplo {"eb": eb_t, "eb_len": eb_l}.
    """
    filas = []
    for u, v, d in G.edges(data=True):
        fila = {"u": u, "v": v, "nombre": d["name"], "length_m": d["length"]}
        for col, valores in intermediaciones.items():
            fila[col] = valores[(u, v)]
        filas.append(fila)
    return pd.DataFrame(filas)


def concentracion(valores: Sequence[float]) -> dict:
    """Gini de los valores y fracción del total que acumula el 1% superior."""
    x = np.sort(np.asarray(valores, dtype=float))
    n = len(x)
    gini = (2 * np.sum(np.arange(1, n + 1) * x) / (n * x.sum())) - (n + 1) / n
    top1 = x[-max(1, n // 100):].sum() / x.sum()
    return {"gini": gini, "top1": top1}


# ---------------------------------------------------------------------------
# Corredores
# ---------------------------------------------------------------------------

def tramos_por_corredor(tramos: pd.DataFrame, dividir_compuestos: bool = False) -> pd.DataFrame:
    """Tramos con nombre, listos para agrupar por corredor.

    Excluye los tramos sin nombre. Con `dividir_compuestos=True` (decisión
    A13), un tramo con nombre compuesto ("Av. X / Av. Y") cuenta una vez para
    cada corredor que nombra.
    """
    t = tramos[tramos["nombre"] != SIN_NOMBRE].copy()
    if dividir_compuestos:
        t["nombre"] = t["nombre"].str.split(SEPARADOR_NOMBRES, regex=False)
        t = t.explode("nombre", ignore_index=True)
    return t


def tramos_excluidos(tramos: pd.DataFrame) -> dict:
    """Cuántos tramos y kilómetros quedan fuera del análisis por no tener nombre."""
    sin = tramos[tramos["nombre"] == SIN_NOMBRE]
    return {"tramos": len(sin), "km": sin["length_m"].sum() / 1000}


def corredores(
    tramos: pd.DataFrame,
    cargas: Mapping[str, str],
    min_km: float = 2.0,
    dividir_compuestos: bool = False,
) -> pd.DataFrame:
    """Carga de cada corredor: intermediación media ponderada por longitud.

    `cargas` asocia el nombre de la columna de salida con la columna de
    intermediación de `tramos`, por ejemplo {"carga_t": "eb", "carga_l": "eb_len"}.
    `eb_max` es el máximo de la primera columna de `cargas`. Se excluyen los
    corredores de menos de `min_km` kilómetros (fragmentos).
    """
    t = tramos_por_corredor(tramos, dividir_compuestos)
    agregados = {"km": ("length_m", lambda s: s.sum() / 1000),
                 "eb_max": (next(iter(cargas.values())), "max")}
    for salida, col in cargas.items():
        t[f"_{salida}"] = t[col] * t["length_m"]
        agregados[salida] = (f"_{salida}", "sum")
    c = t.groupby("nombre").agg(**agregados)
    for salida in cargas:
        c[salida] /= c["km"] * 1000
    return c[c["km"] >= min_km]


def dependencia_velocidad(
    corr: pd.DataFrame,
    col_tiempo: str,
    col_distancia: str,
    cortes: Sequence[float],
    etiquetas: Sequence[str],
) -> pd.DataFrame:
    """Índice de dependencia de velocidad y tipo de corredor.

    El índice es la carga por tiempo dividida por la carga por distancia.
    `cortes` son los límites internos entre tipos (A6: 0,6 y 2) y `etiquetas`
    los nombres de cada tramo, de menor a mayor índice.
    """
    if len(etiquetas) != len(cortes) + 1:
        raise ValueError("Debe haber una etiqueta más que cortes")
    out = corr.copy()
    out["dep_vel"] = out[col_tiempo] / out[col_distancia]
    out["tipo"] = pd.cut(out["dep_vel"], [0, *cortes, np.inf], labels=list(etiquetas))
    return out


# ---------------------------------------------------------------------------
# Comparaciones
# ---------------------------------------------------------------------------

def jaccard_top(a: pd.Series, b: pd.Series, n: int = 10) -> float:
    """Similitud de Jaccard entre los n índices con mayor valor de a y de b."""
    top_a, top_b = set(a.nlargest(n).index), set(b.nlargest(n).index)
    return len(top_a & top_b) / len(top_a | top_b)


def spearman(a: Sequence[float], b: Sequence[float]) -> float:
    """Correlación de rangos de Spearman."""
    return float(spearmanr(a, b)[0])


def comparar_corredores(a: pd.Series, b: pd.Series, n: int = 10) -> dict:
    """Compara la carga de los corredores comunes entre dos redes o pesos."""
    comunes = a.index.intersection(b.index)
    top_a, top_b = set(a.nlargest(n).index), set(b.nlargest(n).index)
    return {
        "comunes": len(comunes),
        "spearman": spearman(a.loc[comunes], b.loc[comunes]),
        "top_en_ambos": top_a & top_b,
        "solo_en_b": top_b - top_a,
    }
