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


# --- eficiencia y cierres ---

def test_eficiencia_ciclo():
    # Desde cada nodo: distancias 60, 120 y 60 s -> (1/60 + 1/120 + 1/60) / 3
    G = grafo_valido()
    assert pr.eficiencia(G, list(G.nodes)) == pytest.approx((2 / 60 + 1 / 120) / 3)


def test_con_reverso_y_cerrar_tramos():
    G = grafo_valido()
    assert set(pr.con_reverso(G, [(0, 1)])) == {(0, 1), (1, 0)}
    H = pr.cerrar_tramos(G, [(0, 1)])
    assert H.number_of_edges() == 6 and G.number_of_edges() == 8   # no modifica el original


def test_cerrar_aleatorio_alcanza_km():
    G = grafo_valido()
    H = pr.cerrar_aleatorio(G, km_objetivo=1.5, seed=0)
    # Dos aristas de 1 km cada una alcanzan 1,5 km; con sus reversos se retiran 2 o 4
    assert G.number_of_edges() - H.number_of_edges() in (2, 4)


def test_tramos_de_corredor_incluye_compuestos():
    sel = pr.tramos_de_corredor(tramos_ejemplo(), "Av A")
    assert len(sel) == 3


# --- resiliencia ---

def test_ataque_aleatorio_registra_curva_y_retiros():
    G = grafo_valido()
    curva, registro = pr.ataque(G, "aleatorio", list(G.nodes), E0=pr.eficiencia(G, list(G.nodes)),
                                pasos=2, frac=0.25, seed=1)
    assert list(curva["f"]) == [0.0, 0.25, 0.5]
    assert curva["S"].iloc[0] == 1.0 and curva["S"].iloc[-1] < 1.0
    assert set(registro["paso"]) <= {1, 2}
    assert curva["f_efectiva"].iloc[-1] == pytest.approx(len(registro) / 8)


def test_ataque_valida_estrategia():
    G = grafo_valido()
    with pytest.raises(ValueError):
        pr.ataque(G, "otra", list(G.nodes), 1.0)
    with pytest.raises(ValueError):
        pr.ataque(G, "eb_inicial", list(G.nodes), 1.0)


def test_f_critica_interpola():
    assert pr.f_critica([0, 0.01, 0.02], [1.0, 0.6, 0.4]) == pytest.approx(0.015)
    assert pr.f_critica([0, 0.01], [1.0, 0.9]) != pr.f_critica([0, 0.01], [1.0, 0.9])   # NaN


def test_robustez_en_rango_y_reproducible():
    G = grafo_valido()
    R1, S1 = pr.robustez(G, pasos=3, frac=0.25, k=4)
    R2, _ = pr.robustez(G, pasos=3, frac=0.25, k=4)
    assert R1 == R2 and 0 < R1 <= 1 and len(S1) == 4 and S1[0] == 1.0


def test_componentes_tras_retiro():
    G = grafo_valido()
    registro = pd.DataFrame({"paso": [1, 1, 2, 2], "u": [0, 1, 2, 3], "v": [1, 0, 3, 2]})
    assert [len(c) for c in pr.componentes_tras_retiro(G, registro, 1)] == [4]
    assert sorted(len(c) for c in pr.componentes_tras_retiro(G, registro, 2)) == [2, 2]


# --- intervenciones ---

def test_agregar_enlace_doble_sentido():
    G = grafo_valido()
    H, km = pr.agregar_enlace(G, 0, 2, vel_kph=36, factor=1.0)
    assert km == pytest.approx(0.002)                 # nodos a 2 m en línea recta
    assert H.edges[0, 2]["travel_time"] == pytest.approx(0.2) and H.has_edge(2, 0)
    assert not G.has_edge(0, 2)


def test_acelerar_y_km_de_corredores():
    G = grafo_valido()
    H = pr.acelerar(G, {"Av A"}, vel_kph=36)          # 10 m/s
    assert H.edges[0, 1]["travel_time"] == pytest.approx(100.0)
    assert H.edges[2, 3]["travel_time"] == 60.0       # "Av A / Av B" no es nombre exacto
    assert pr.km_de_corredores(G, {"Av A"}) == pytest.approx(4.0)


def test_tiempo_entre_zonas():
    G = grafo_valido()
    assert pr.tiempo_entre_zonas(G, {0}, {2}, n=1) == pytest.approx(2.0)


# --- comparaciones ---

def test_jaccard_y_comparacion():
    a = pd.Series({"p": 3, "q": 2, "r": 1})
    b = pd.Series({"p": 30, "q": 1, "s": 20})
    assert pr.jaccard_top(a, b, n=2) == pytest.approx(1 / 3)
    r = pr.comparar_corredores(a, b, n=2)
    assert r["comunes"] == 2
    assert r["top_en_ambos"] == {"p"}
    assert r["solo_en_b"] == {"s"}
