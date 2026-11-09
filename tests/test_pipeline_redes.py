"""Pruebas del núcleo con grafos sintéticos pequeños y resultados conocidos."""

import networkx as nx
import pandas as pd
import pytest

import src.pipeline_redes as pr


def grafo_valido() -> nx.DiGraph:
    """Ciclo de 4 nodos en ambos sentidos, con un tramo de nombre compuesto."""
    G = nx.DiGraph(red="prueba", crs="EPSG:9377", fuente="sintética", fecha_snapshot="2026-11-09")
    for i in range(4):
        G.add_node(i, x=float(i), y=0.0)
    nombres = ["Av A", "Av A", "Av A / Av B", pr.SIN_NOMBRE]
    for i in range(4):
        j = (i + 1) % 4
        for u, v in ((i, j), (j, i)):
            G.add_edge(u, v, length=1000.0, travel_time=60.0, name=nombres[i])
    return G


# --- normalizar_nombre ---

@pytest.mark.parametrize("entrada, esperado", [
    (["Av B", "Av A", "Av B"], "Av A / Av B"),
    ("  Calle 1 ", "Calle 1"),
    (None, pr.SIN_NOMBRE),
    ("", pr.SIN_NOMBRE),
    ([], pr.SIN_NOMBRE),
    (float("nan"), pr.SIN_NOMBRE),
])
def test_normalizar_nombre(entrada, esperado):
    assert pr.normalizar_nombre(entrada) == esperado


# --- validar_contrato ---

def test_contrato_valido_no_falla():
    pr.validar_contrato(grafo_valido())


def test_contrato_rechaza_multigrafo():
    with pytest.raises(ValueError, match="sin aristas paralelas"):
        pr.validar_contrato(nx.MultiDiGraph(grafo_valido()))


def test_contrato_rechaza_no_conexo():
    G = grafo_valido()
    G.add_node(99, x=0.0, y=0.0)
    with pytest.raises(ValueError, match="fuertemente conexo"):
        pr.validar_contrato(G)


def test_contrato_rechaza_tiempo_no_positivo():
    G = grafo_valido()
    G.edges[0, 1]["travel_time"] = 0
    with pytest.raises(ValueError, match="travel_time"):
        pr.validar_contrato(G)


def test_contrato_rechaza_nombre_lista():
    G = grafo_valido()
    G.edges[0, 1]["name"] = ["Av A"]
    with pytest.raises(ValueError, match="name"):
        pr.validar_contrato(G)


def test_contrato_rechaza_atributos_de_grafo_faltantes():
    G = grafo_valido()
    del G.graph["fuente"]
    with pytest.raises(ValueError, match="fuente"):
        pr.validar_contrato(G)


# --- estructura ---

def test_estructura_ciclo():
    r = pr.estructura(grafo_valido(), n_fuentes=10, seed=0)
    assert (r["N"], r["M"]) == (4, 8)
    assert r["grado_medio"] == 2.0
    assert r["clustering"] == 0.0
    # En un ciclo de 4 con 1 min por tramo: distancias 1, 2 y 1 min desde cada nodo
    assert r["tiempo_medio_min"] == pytest.approx(4 / 3)


def test_muestra_reproducible_igual_a_random_global():
    """Con la misma semilla reproduce random.seed + random.sample del notebook histórico."""
    import random
    G = nx.path_graph(50, create_using=nx.DiGraph)
    random.seed(42)
    esperado = random.sample(list(G.nodes), 10)
    assert pr.muestrear_nodos(G, 10, 42) == esperado


# --- concentración ---

def test_concentracion_igualdad_y_desigualdad():
    assert pr.concentracion([1.0] * 200)["gini"] == pytest.approx(0.0)
    r = pr.concentracion([0.0] * 199 + [1.0])
    assert r["gini"] == pytest.approx(199 / 200)
    assert r["top1"] == pytest.approx(1.0)   # 1% de 200 = 2 tramos, contienen todo


# --- corredores ---

def tramos_ejemplo() -> pd.DataFrame:
    return pd.DataFrame({
        "nombre": ["Av A", "Av A", "Av A / Av B", pr.SIN_NOMBRE],
        "length_m": [1000.0, 3000.0, 2000.0, 500.0],
        "eb": [0.1, 0.3, 0.2, 0.9],
        "eb_len": [0.2, 0.2, 0.4, 0.9],
    })


def test_corredores_promedio_ponderado_por_longitud():
    c = pr.corredores(tramos_ejemplo(), {"carga_t": "eb", "carga_l": "eb_len"}, min_km=0)
    assert set(c.index) == {"Av A", "Av A / Av B"}             # sin nombre excluido
    assert c.loc["Av A", "km"] == pytest.approx(4.0)
    assert c.loc["Av A", "carga_t"] == pytest.approx((0.1 * 1000 + 0.3 * 3000) / 4000)
    assert c.loc["Av A", "eb_max"] == pytest.approx(0.3)


def test_corredores_filtra_fragmentos():
    c = pr.corredores(tramos_ejemplo(), {"carga": "eb"}, min_km=3)
    assert list(c.index) == ["Av A"]


def test_corredores_divide_compuestos():
    c = pr.corredores(tramos_ejemplo(), {"carga": "eb"}, min_km=0, dividir_compuestos=True)
    assert set(c.index) == {"Av A", "Av B"}
    assert c.loc["Av A", "km"] == pytest.approx(6.0)
    assert c.loc["Av B", "carga"] == pytest.approx(0.2)


def test_tramos_excluidos():
    assert pr.tramos_excluidos(tramos_ejemplo()) == {"tramos": 1, "km": 0.5}


def test_dependencia_velocidad_cortes_a6():
    corr = pd.DataFrame({"t": [0.5, 1.0, 3.0], "l": [1.0, 1.0, 1.0]}, index=["x", "y", "z"])
    r = pr.dependencia_velocidad(corr, "t", "l", [0.6, 2],
                                 ["subutilizados", "estructurales", "atraen por velocidad"])
    assert list(r["tipo"]) == ["subutilizados", "estructurales", "atraen por velocidad"]


def test_dependencia_velocidad_valida_etiquetas():
    with pytest.raises(ValueError):
        pr.dependencia_velocidad(pd.DataFrame({"t": [1.0], "l": [1.0]}), "t", "l", [1], ["a"])


# --- comparaciones ---

def test_jaccard_y_comparacion():
    a = pd.Series({"p": 3, "q": 2, "r": 1})
    b = pd.Series({"p": 30, "q": 1, "s": 20})
    assert pr.jaccard_top(a, b, n=2) == pytest.approx(1 / 3)
    r = pr.comparar_corredores(a, b, n=2)
    assert r["comunes"] == 2
    assert r["top_en_ambos"] == {"p"}
    assert r["solo_en_b"] == {"s"}
