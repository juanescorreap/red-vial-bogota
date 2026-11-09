# Inventario de Drive (tarea 3)

Fecha del inventario: 2026-11-09. Carpeta: `MyDrive/proyecto-redes-bogota/data/processed/`, descargada a `data/drive_snapshot/` (fuera de git). Grafos leídos con NetworkX 3.7 en el entorno local.

## Grafos

| Archivo en Drive | Tamaño | Nodos | Aristas | Dirigido | Construido (`created_date`) | Versión de OSMnx |
|---|---|---|---|---|---|---|
| `gvial_arterial.graphml` | 5,00 MB | 3.203 | 5.199 | Sí | 2026-10-05 19:22:30 | 2.1.1 |
| `gvial_drive.graphml` | 79,05 MB | 59.198 | 148.019 | Sí | 2026-10-05 19:23:54 | 2.1.1 |

La descarga agregó `.xml` al nombre de ambos archivos; el contenido no cambia.

## Otras salidas del avance

`cierre_corredores.csv`, `curvas_resiliencia.csv`, `eb_drive_k1000.pkl`, `escenarios_final.csv`, `escenarios_robustez.csv`, `log_ataque_recalculado.csv`. Están todas las que guarda el notebook histórico en `data/processed/`.

## Contraste con las cifras presentadas

- Nodos: 3.203 y 59.198 coinciden con la presentación de avance (diapositivas 3 y 7).
- Aristas de la red completa: 148.019 coincide con el documento de contexto.
- Aristas de la red arterial: el grafo tiene 5.199 y el documento de contexto dice 5.175 (diferencia de 24). No es el conteo no dirigido de una red de doble sentido, que daría cerca de la mitad. Hipótesis por verificar en la tarea 4: 5.175 se contó después de convertir el grafo (por ejemplo con `ox.convert.to_digraph`, que une aristas paralelas, o al pasarlo a no dirigido).

## Lo que no se sabe

- Versión de NetworkX usada en el avance: el `.graphml` no la registra.
- Fecha exacta de la presentación de avance (solo "octubre 2026"). Inferencia: los grafos del 5 de octubre son los que produjeron las cifras, porque N coincide en ambas redes y la versión de OSMnx es la que el notebook espera (2.x). Se confirma en la tarea 4 si la línea base reproduce las cifras.
- Fechas de modificación de los CSV en Drive: no se registraron.
