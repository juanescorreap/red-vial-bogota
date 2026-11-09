"""Figuras de la presentación final con la estética de la presentación de avance.

Lee los resultados de data/salidas_locales/resultados/ (salidas de los notebooks 01 a 04).
Uso, desde la raíz del repo y con el .venv activado:
    python scripts/figuras_presentacion.py . data/salidas_locales/figuras
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

RAIZ = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(RAIZ / "src"))
import adaptador_gvial as ag
import metro_l1 as ml

ROJO, ROSA, GRIS, FONDO, REJILLA, TEXTO = "#8A0F12", "#E39A97", "#999999", "#F5F5F5", "#DDDDDD", "#444444"
plt.rcParams.update({"font.family": "Arial", "font.size": 22, "axes.edgecolor": REJILLA, "axes.labelcolor": TEXTO,
                     "xtick.color": TEXTO, "ytick.color": TEXTO, "axes.spines.top": False, "axes.spines.right": False})
RES = RAIZ / "data" / "salidas_locales" / "resultados"

# 1. Red vial en blanco (portada, contenido y referencias)
_, G = ag.cargar_gvial(RAIZ / "data" / "drive_snapshot" / "processed", "gvial_arterial", "Gvial arterial")
fig, ax = plt.subplots(figsize=(6, 9), dpi=200)
for u, v in G.edges():
    ax.plot([G.nodes[u]["x"], G.nodes[v]["x"]], [G.nodes[u]["y"], G.nodes[v]["y"]], color="#FFFFFF", lw=0.9, alpha=0.9)
ax.set_aspect("equal"); ax.axis("off")
fig.savefig(OUT / "red_vial_blanca.png", transparent=True, bbox_inches="tight", pad_inches=0)
plt.close(fig)

# 2. Fragilidad: Gvial y TransMilenio L, componente gigante contra fracción efectiva retirada
cv = pd.read_csv(RES / "gvial" / "curvas_resiliencia.csv")
ct = pd.read_csv(RES / "gtransporte" / "curvas_resiliencia.csv")
ct = ct[ct["espacio"] == "L"]
fig, axes = plt.subplots(1, 2, figsize=(16.6, 5.6), dpi=100, sharey=True)
fig.patch.set_facecolor(FONDO)
for ax, (titulo, c) in zip(axes, (("Red vial arterial", cv), ("TransMilenio (espacio L)", ct))):
    ax.set_facecolor(FONDO)
    azar = c[c["estrategia"] == "aleatorio"].groupby("f")[["f_efectiva", "S"]].mean()
    ad = c[c["estrategia"] == "eb_recalculada"]
    azar, ad = azar[azar["f_efectiva"] <= 0.2], ad[ad["f_efectiva"] <= 0.2]
    ax.plot(100 * azar["f_efectiva"], azar["S"], color=GRIS, lw=3, marker="o", ms=7, label="Azar (media de 5)")
    ax.plot(100 * ad["f_efectiva"], ad["S"], color=ROJO, lw=3, marker="o", ms=7, label="Adaptativo")
    ax.axhline(0.5, color=TEXTO, lw=1, ls="--")
    ax.set_title(titulo, color=TEXTO, fontsize=24, pad=14)
    ax.set_xlabel("% de tramos retirados (efectivo)", fontsize=20)
    ax.set_xlim(0, 20); ax.set_ylim(0, 1.03)
    ax.grid(axis="y", color=REJILLA); ax.set_axisbelow(True)
axes[0].set_ylabel("Componente gigante S", fontsize=20)
axes[0].text(0.3, 0.52, "mitad de la red", color=TEXTO, fontsize=17)
axes[0].legend(frameon=False, fontsize=19, loc="lower left")
fig.tight_layout()
fig.savefig(OUT / "fragilidad_comparada.png", facecolor=FONDO)
plt.close(fig)

# 3. Intervalos de confianza del cambio de R (10 réplicas pareadas)
rob = pd.read_csv(RES / "gvial" / "robustez_intervenciones.csv", index_col=0)
etiquetas = {"A": "A · Enlace 4,2 km", "B": "B · Cra. 68 y 50 a 50 km/h", "A+B": "A + B"}
fig, ax = plt.subplots(figsize=(10, 5.2), dpi=100)
fig.patch.set_facecolor(FONDO); ax.set_facecolor(FONDO)
for i, (k, fila) in enumerate(rob.loc[["A+B", "B", "A"]].iterrows()):
    color = ROJO if str(fila["concluyente"]) == "True" else GRIS
    ax.plot([fila["ic_inf_%"], fila["ic_sup_%"]], [i, i], color=color, lw=6, solid_capstyle="round")
    ax.plot(fila["dR_medio_%"], i, "o", color=color, ms=16, markeredgecolor=FONDO, markeredgewidth=2)
    ax.text(fila["ic_sup_%"] + 0.35, i, f"{fila['dR_medio_%']:+.1f} %".replace(".", ","), va="center", color=TEXTO, fontsize=22)
ax.axvline(0, color=TEXTO, lw=1.5)
ax.set_yticks(range(3)); ax.set_yticklabels([etiquetas[k] for k in ["A+B", "B", "A"]], fontsize=21)
ax.set_xlabel("Cambio de R frente a la red actual (%), IC 95 %", fontsize=19)
ax.set_xlim(-3, 8.5); ax.grid(axis="x", color=REJILLA); ax.set_axisbelow(True)
ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
fig.tight_layout()
fig.savefig(OUT / "robustez_intervalos.png", facecolor=FONDO)
plt.close(fig)

# 4. Mapa de TransMilenio L con la troncal 7 y la Línea 1 del metro
L = nx.read_graphml(RES / "gtransporte" / "Gtransporte_L.graphml")
xy = {n: (float(d["x"]), float(d["y"])) for n, d in L.nodes(data=True)}
est = ml.estaciones_osm(RAIZ / "data" / "raw" / "metro_l1" / "osm_metro_l1_2026-11-09.geojson", "Gibraltar")
fig, ax = plt.subplots(figsize=(6, 8.5), dpi=150)
fig.patch.set_facecolor(FONDO); ax.set_facecolor(FONDO)
for u, v, d in L.edges(data=True):
    t7 = d["name"] == "Troncal 7"
    ax.plot([xy[u][0], xy[v][0]], [xy[u][1], xy[v][1]], color=ROJO if t7 else GRIS, lw=4 if t7 else 2, zorder=2 if t7 else 1,
            solid_capstyle="round")
ax.plot(est["x"], est["y"], color=ROSA, lw=4, ls=(0, (2, 1.2)), zorder=3)
ax.scatter(est["x"], est["y"], s=28, color=ROSA, edgecolor=FONDO, linewidth=1, zorder=4)
ax.set_aspect("equal"); ax.axis("off")
fig.savefig(OUT / "mapa_transmilenio.png", facecolor=FONDO, bbox_inches="tight", pad_inches=0.05)
plt.close(fig)
print("figuras en", OUT)
