# Contexto: Caos y Complejidad

Universidad Jorge Tadeo Lozano, Ciencia de Datos, semestre 2026-2.

## Contenido del curso visto hasta ahora

Texto de referencia: *Network Science*, Albert-László Barabási (networksciencebook.com), capítulo 2 (secciones 2.1 a 2.10), más material complementario sobre BFS y Dijkstra.

- Origen de la teoría de grafos (puentes de Königsberg) y caminos eulerianos por paridad de grados.
- Formalismo de redes: nodos, enlaces, grado, grado promedio, matriz de adyacencia, listas de enlaces, redes dirigidas y no dirigidas.
- Redes dispersas y redes ponderadas.
- Redes bipartitas y sus proyecciones.
- Caminos, distancias, diámetro, conectividad y componentes.
- Coeficiente de clustering local y promedio.
- Conteo de caminatas con potencias de la matriz de adyacencia.
- Algoritmos: BFS (cola, complejidad) y Dijkstra (grafos ponderados, cola de prioridad, formulación como programación lineal).
- Teoría de la información de Shannon (información como −log p) también aparece en el curso.

## Proyecto del curso

**Título presentado:** "Estructura de Redes y Movilidad en Bogotá" (propuesta inicial: "Del Trazado a la Fragilidad: Análisis Morfológico y de Vulnerabilidad de la Red Vial Urbana mediante Teoría de Redes Complejas").

**Equipo:** Andrés Pimienta, Adriana Correa, Sebastián García y Juan Esteban Correa. Duración: 10 semanas.

**Pregunta central:** qué segmentos viales concentran el flujo de Bogotá de forma que su falla degrada la conectividad de manera desproporcionada, y qué intervención reduce mejor esa concentración por kilómetro.

**Alcance:**
- Bogotá urbana completa, sin Sumapaz.
- Dos grafos construidos con OSMnx: red arterial (3.203 nodos, 5.175 enlaces; de autopistas a vías secundarias), usada para los cálculos repetidos, y red "drive" completa (59.198 nodos, 148.019 enlaces), usada para validar que el filtro no sesga los resultados.
- Escenario de referencia: día hábil, hora pico AM. Acceso a datos de la Secretaría de Movilidad aún por verificar.
- Herramientas: Python, OSMnx, NetworkX, GeoPandas, en Google Colab con resultados en Google Drive.

**Decisión metodológica:** validar toda la metodología primero con el grafo vial (Gvial) en la presentación de avance, y después ejecutar el mismo pipeline con TransMilenio (Gtransporte) antes de la entrega final.

**Resultados de la presentación de avance:**
- La red vial no tiene estructura de hubs (no es libre de escala; grado medio 3,1).
- La Av. Carrera 30 (NQS) es el corredor más crítico en cuatro pruebas independientes (ponderado por tiempo, por distancia, red arterial y red completa; correlación de Spearman 0,77 entre redes).
- La intermediación de enlaces está muy concentrada: el 1% superior de segmentos acumula el 13,5% del total (Gini 0,69).
- Índice de dependencia de velocidad (carga por tiempo dividida por carga por distancia), propuesto por el equipo, que distingue tres tipos de corredores: los que atraen tráfico por velocidad (NQS, Transversal 35), los estructurales críticos con cualquier ponderación (Av. Boyacá, Av. Ciudad de Cali) y los subutilizados (Carrera 68 a 37 km/h y Carrera 50 a 34 km/h).
- Resiliencia: un ataque adaptativo (recalculando intermediación después de cada remoción) fragmenta la red con solo el 6,5% de los enlaces removidos, frente a cerca del 14% con fallas aleatorias. Mecanismo de cascada: al cerrar la NQS el tráfico pasa a la Av. Boyacá y luego a otros corredores, hasta partir la ciudad en tres macrozonas por corredores "costura" (Av. Ciudad de Cali, Carrera 7). La fragmentación es direccional: el 97% sigue conectado en sentido débil.
- Intervenciones: subir a 50 km/h la Carrera 68 y la Carrera 50 reduce 15% la carga de la NQS, mejora 1,5% la eficiencia y reduce 3,8% el tiempo de viaje entre zonas; un enlace nuevo de 4,2 km entre Fontibón y Kennedy logra solo 0,2% y 0,04%. Las mejoras de robustez de ambos escenarios (cerca de 4 a 5%) no son concluyentes con solo 3 réplicas.

**Estructura exigida por el profesor para la presentación de avance:** título, tabla de contenido, resumen de un párrafo, estado del arte, metodología, resultados y avance (la sección de mayor peso), conclusiones y referencias.

**Referencias metodológicas adicionales:** Boeing (artículo de OSMnx), Strano et al. (robustez y centralidad), Kirkley et al. 2025 (modelos universales de redes de calles), un artículo sobre embebimiento espacial y robustez de redes planares, y un caso de robustez de la red vial de Messina.

## Cómo prefiero trabajar en esta materia

- En el proyecto, yo ejecuto todos los pasos técnicos; Claude guía y explica, y solo ejecuta cuando se lo pido explícitamente.
- Resúmenes del libro para el cuaderno: en español, con los mismos títulos de las secciones del texto.
- Los datos de OpenStreetMap no se pueden descargar desde el entorno de Claude; los descargo yo (OSMnx en Colab u Overpass Turbo). Exportar en un formato que conserve la topología de nodos y enlaces, no GeoJSON simple.

## Pendientes

- Ejecutar el pipeline con TransMilenio (Gtransporte).
- Aumentar réplicas en las pruebas de robustez de los escenarios de intervención.
- Confirmar acceso a datos de la Secretaría de Movilidad.
- Preparar la entrega final.

## Por confirmar

- Nombre del profesor, fecha de la entrega final y criterios de evaluación (subir el programa y el enunciado del proyecto como archivos).
