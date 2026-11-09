# Estructura de Redes y Movilidad en Bogotá

Proyecto del curso Caos y Complejidad (Ciencia de Datos, UTADEO, 2026-2). Equipo: Andrés Pimienta, Adriana Correa, Sebastián García y Juan Esteban Correa. Duración según la propuesta: 10 semanas. Lector final: el profesor del curso.

## 1. Pregunta del proyecto

Qué segmentos viales concentran el flujo de Bogotá de forma que su falla degrada la conectividad de manera desproporcionada, y qué intervención reduce mejor esa concentración por kilómetro.

Título presentado: "Estructura de Redes y Movilidad en Bogotá". Propuesta inicial: "Del Trazado a la Fragilidad: Análisis Morfológico y de Vulnerabilidad de la Red Vial Urbana mediante Teoría de Redes Complejas".

Objetivo general: entregar un análisis reproducible de la estructura, la vulnerabilidad y las intervenciones de la red vial de Bogotá (Gvial), y replicar el mismo pipeline sobre TransMilenio (Gtransporte, modelado en espacio L y en espacio P, con una intervención de Metro Línea 1) para comparar ambas redes.

## 2. Estado actual (avance presentado)

Las cifras provienen de `docs/referencia/contexto_caos_y_complejidad.md` y se contrastaron con el texto extraído de la presentación de avance (`docs/referencia/texto_pdfs_extraido.md`, diapositivas 3 y 7 a 13). No aparecen en ese texto: los 5.175 enlaces (el `.graphml` arterial tiene 5.199 aristas dirigidas, ver `docs/referencia/inventario_drive.md`) y los 148.019 de la red completa (confirmados en el `.graphml`), el escenario "día hábil, hora pico AM" y el nombre "Fontibón a Kennedy" del enlace nuevo; esos datos solo constan en el documento de contexto. Ninguna cifra está verificada contra una ejecución: el notebook del avance no conserva salidas (ver 2.5 y la sección 8).

### 2.1 Decisión metodológica vigente

Validar toda la metodología con Gvial en la presentación de avance y después ejecutar el mismo pipeline con TransMilenio (Gtransporte) antes de la entrega final.

Alcance de la siguiente fase, anunciado al profesor en la presentación de avance (diapositiva 12) y en la propuesta (páginas 10 y 12), confirmado por Juan Esteban Correa el 2026-11-09 (el mismo día reemplazó la versión con recortes: "desarrollar y completar exitosamente el alcance planteado del proyecto sin recortar"):

1. Gtransporte en espacio L y en espacio P. Según la propuesta: nodos = estaciones, aristas = rutas, datos GTFS, pesos por tiempo y frecuencia. Fijo.
2. Intervenciones sobre Gtransporte: Metro Línea 1 (la propuesta habla de insertar un nuevo corredor de transporte público). Fijo.
3. Robustez con 10 réplicas pareadas del índice R (Schneider et al., 2011). Fijo.

El alcance no tiene elementos recortables. No hay fecha de entrega: se avanza lo más posible en el orden del camino crítico de `PLAN.md` (Juan Esteban Correa, 2026-11-09).

### 2.2 Grafos construidos con OSMnx

| Grafo | Nodos | Enlaces | Uso |
|---|---|---|---|
| Red arterial (autopistas a vías secundarias) | 3.203 | 5.175 | Cálculos repetidos |
| Red "drive" completa | 59.198 | 148.019 | Validar que el filtro no sesga los resultados |

Escenario de referencia: día hábil, hora pico AM.

### 2.3 Resultados presentados sobre Gvial

| Tema | Resultado |
|---|---|
| Estructura | Sin hubs: la red no es libre de escala. Grado medio 3,1; clustering 0,07 (casi nulo, red espacial planar); viaje medio 17,9 min. El 73% de las intersecciones tiene grado 3. |
| Corredor crítico | La Av. Carrera 30 (NQS) es el más crítico en cuatro pruebas independientes (ponderado por tiempo, por distancia, red arterial y red completa). Correlación de Spearman entre redes: 0,77. |
| Concentración | El 1% superior de segmentos acumula el 13,5% de la intermediación de enlaces (Gini 0,69). |
| Índice de dependencia de velocidad | Carga por tiempo dividida por carga por distancia, propuesto por el equipo. Distingue tres tipos: atraen tráfico por velocidad (NQS, Transversal 35), estructurales críticos con cualquier ponderación (Av. Boyacá, Av. Ciudad de Cali) y subutilizados (Carrera 68 a 37 km/h, Carrera 50 a 34 km/h). |
| Resiliencia | Un ataque adaptativo (intermediación recalculada tras cada remoción) fragmenta la red con 6,5% de los enlaces removidos, frente a cerca de 14% con fallas aleatorias. Con 5% de tramos retirados la red sigue unida, pero la eficiencia global cae 28%. |
| Cascada | Al cerrar la NQS, el tráfico pasa a la Av. Boyacá y luego a otros corredores, hasta partir la ciudad en tres macrozonas por corredores "costura" (Av. Ciudad de Cali, Carrera 7). Macrozonas: Nororiente 825 nodos, Centro-occidente 957 y Sur 718. La fragmentación es direccional: el 97% sigue conectado en sentido débil. |
| Intervención A: enlace nuevo de 4,2 km (Fontibón a Kennedy) | Carga de la NQS -0,2% (-0,05% por km), tiempo de viaje entre zonas -0,8%, eficiencia global +0,04%. |
| Intervención B: velocidad de la Carrera 68 y la Carrera 50 a 50 km/h | Carga de la NQS -15,1% (-0,41% por km), tiempo de viaje entre zonas -3,8%, eficiencia global +1,5%. |
| Robustez de las intervenciones | Índice R de 4,8 (A) y 4,2 (B), media de 3 réplicas pareadas, no concluyente. Modelo a flujo libre, sin congestión. Si 4,8 y 4,2 son porcentajes o puntos de R no está confirmado (ver sección 9). |

Las letras A y B de las intervenciones coinciden con el notebook y con la presentación de avance (diapositiva 12). El documento de contexto las tenía invertidas.

### 2.4 Estructura exigida por el profesor para el avance

Título, tabla de contenido, resumen de un párrafo, estado del arte, metodología, resultados y avance (la sección de mayor peso), conclusiones y referencias.

### 2.5 Estado del código

El notebook del avance existe en `notebooks/Proyecto_diagnóstico_cuellos_de_botella.ipynb`: 43 celdas de código, sin celdas de texto y sin salidas guardadas. Según la revisión de `docs/arquitectura/propuesta_pipeline.md`:

- No consta que los `.graphml` de Drive sean los que produjeron las cifras presentadas.
- La celda 40 falla por nombres no definidos.
- Varias cifras no se pueden regenerar desde el código (ver riesgos en la sección 8).
- `src/` aún no contiene código. El módulo común es una propuesta.

## 3. Alcance

### Dentro

- Bogotá urbana completa, sin Sumapaz.
- Gvial: consolidar y documentar el pipeline ya validado, de modo que se reproduzca en Colab y regenere las cifras del avance o explique las diferencias.
- Gtransporte (TransMilenio) en espacio L (estaciones unidas si son consecutivas en un corredor), con el mismo pipeline. Nodos = estaciones; fuente GTFS según la propuesta.
- Gtransporte en espacio P (estaciones unidas si comparten ruta), con pesos por tiempo y frecuencia.
- Intervención sobre Gtransporte: Metro Línea 1 (nuevo corredor de transporte público).
- Comparación Gvial frente a Gtransporte con las mismas métricas, y comparación del espacio L frente al espacio P.
- Robustez de las intervenciones con 10 réplicas pareadas del índice R. Fijo.
- Informe final con la estructura definida en la sección 10.

### Fuera

- Datos de aforo o velocidades reales de la Secretaría de Movilidad, mientras no se confirme el acceso. El escenario se mantiene con los datos de OSMnx.
- Otros modos de transporte distintos de TransMilenio y de la intervención Metro L1 (SITP zonal, bicicleta).
- Intervenciones nuevas más allá de A y B en Gvial y de Metro L1 en Gtransporte.
- Infraestructura que no aporte a claridad metodológica o reproducibilidad: servidores, bases de datos, orquestadores, tableros, empaquetado como librería, integración continua.
- Almacenar grafos o resultados en el repositorio (viven en Google Drive).

## 4. Objetivos de la entrega final

| # | Objetivo específico | Entregable verificable |
|---|---|---|
| OE1 | Gvial reproducible en Colab | Notebook(s) que corren sin cambios y regeneran las cifras de la sección 2.3 (o explican las diferencias) |
| OE2 | Gtransporte analizado con el mismo pipeline en espacio L y en espacio P | Grafos de TransMilenio en Drive (L y P) y resultados con las métricas de Gvial, y variante del grafo con Metro L1 |
| OE3 | Conclusiones de robustez firmes | 10 réplicas pareadas del índice R para las intervenciones A y B, y evaluación de Metro L1 con 10 réplicas pareadas, o declaración fundamentada de no concluyente |
| OE4 | Comparación entre redes | Tabla y texto que contrastan Gvial y Gtransporte (L), y L frente a P |
| OE5 | Informe final | Documento con la estructura de la sección 10, cifras trazables a ejecuciones |

## 5. Metodología

- Pipeline único aplicado a ambos grafos: construcción con OSMnx (Gvial) y desde GTFS (Gtransporte), métricas estructurales (grado, clustering, componentes), intermediación de enlaces y concentración (Gini), índice de dependencia de velocidad, ataques (aleatorio y adaptativo), cascada de redistribución e intervenciones.
- Robustez de intervenciones: índice R (Schneider et al., 2011) con 10 réplicas pareadas.
- Marco teórico del curso: *Network Science* de Barabási (capítulo 2), BFS y Dijkstra. Referencias adicionales: Boeing (OSMnx), Lu y Shi 2007 (espacios L y P), Yang y An 2021 (cascada), Latora y Marchiori 2001 (eficiencia global), Strano et al., Kirkley et al. 2025, embebimiento espacial y robustez de redes planares, robustez de la red vial de Messina.
- Reproducibilidad: cada notebook corre en Colab sin cambios, lee de Drive o descarga con OSMnx, fija semillas aleatorias y registra versiones de librerías.
- Toda cifra del informe proviene de una ejecución real.
- Datos de OSM exportados en un formato que conserve la topología de nodos y enlaces (no GeoJSON simple).
- Fases del plan: arranque, Gvial reproducible, Gtransporte y robustez, cierre. Detalle y orden de avance en `PLAN.md`; decisiones de diseño en `docs/decisiones.md` (pendientes de confirmación, salvo el alcance de Gtransporte, las 10 réplicas y la letra de las intervenciones, confirmados el 2026-11-09).
- Cronograma de la propuesta original (referencia de hitos, no es la fecha de entrega): 10 semanas. Semanas 1 y 2: descarga y preprocesamiento. Semanas 3 a 5: análisis topológico y centralidad. Semanas 6 a 8: simulación de resiliencia y optimización. Semanas 9 y 10: redacción e informe final.
- Cadencia de revisión del equipo: por definir.

## 6. Recursos y datos

- Herramientas: Python, OSMnx, NetworkX, GeoPandas, SciPy, Google Colab, Google Drive.
- Datos: OpenStreetMap vía OSMnx (descarga a cargo de un integrante, no desde el entorno de Claude). GTFS de TransMilenio según la propuesta (fuente y vigencia por verificar). Trazado de Metro L1: fuente por definir (candidata: información oficial de la Empresa Metro de Bogotá, por verificar). Secretaría de Movilidad: acceso por verificar.
- Almacenamiento: grafos y resultados en Drive; el repositorio contiene documentación y código.
- Equipo: cuatro integrantes. Responsable de todas las tareas del plan: Juan Esteban Correa (2026-11-09).
- Fuentes de referencia en el repositorio: `docs/referencia/contexto_caos_y_complejidad.md`, presentación de avance (PDF), "Nodos = estaciones TransMilenio.pdf" (propuesta original), `docs/referencia/texto_pdfs_extraido.md` (texto de ambos PDF; ante una duda manda el PDF) y `docs/arquitectura/propuesta_pipeline.md`.

## 7. Stakeholders

- Profesor del curso: evalúa y define fecha y criterios. Nombre por confirmar.
- Equipo de cuatro integrantes: ejecuta y decide lo metodológico.

## 8. Supuestos y riesgos

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Cifras del avance escritas a mano o copiadas de corridas anteriores en el notebook: f_c de 6,5% y 14% (líneas fijas en las celdas 29 y 42), `R_prev` (celda 36), réplicas de la celda 41 y los tiempos -0,8 y -3,8 | No se pueden regenerar ni defender ante el profesor; mezclan sesiones distintas | Registrar línea base, calcular cada cifra en la corrida y documentar las diferencias con lo presentado |
| Cifras sin celda de origen única: N y M (celda 4 o 5), Gini y 1% superior (muestreada o exacta), Spearman 0,77 (celda 15 o 20), 97% en sentido débil, 0,04% del enlace nuevo | Una cifra del informe puede no corresponder a lo que se presentó | Resolver en la decisión A7, verificar el origen del 0,04% en la línea base y dejar el origen en `referencia_avance.csv` |
| Los `.graphml` de Drive no son los del avance, o OSM cambió | Las cifras no coinciden con las presentadas | Inventario de Drive, snapshot fijo y diferencias documentadas |
| TransMilenio no se modela de forma comparable con Gvial | Comparación débil | Regla de construcción acordada y escrita antes de calcular |
| La fuente GTFS no trae rutas y frecuencias vigentes, o su licencia no lo permite | El espacio P no se puede construir y el peso por frecuencia queda sin fuente | Verificar la fuente antes de construir. Respaldos: GTFS de 2020 y 2021 declarando su fecha como limitación, relaciones de ruta de OSM (completitud sin verificar) o, si falta solo la frecuencia, un peso alternativo como supuesto documentado (A11). Si ninguna fuente trae rutas, no hay mitigación real para P: se escala al equipo y al profesor |
| Metro L1 sin fuente de trazado, estaciones y tiempos | No se puede modelar la intervención | Verificar la información oficial de la Empresa Metro de Bogotá. Respaldo: trazado y estaciones transcritos de esa información como supuesto documentado, con el tiempo de viaje como parámetro y análisis de sensibilidad (A12). Fuente alternativa de datos abiertos: por identificar |
| Las 10 réplicas pareadas de R no caben en una sesión de Colab | Corridas truncadas o no reproducibles | Cronometrar antes (tarea 14) y guardar resultados por réplica |
| El alcance fijo (L, P, Metro L1, 10 réplicas) supera el tiempo disponible | Entrega incompleta | Sin fecha de entrega ni recortes: avanzar en el orden del camino crítico de `PLAN.md`, empezando por la línea base, que es la base de todo lo demás |
| Sin acceso a datos de la Secretaría de Movilidad | Escenario basado solo en OSMnx | Declarar la limitación en el informe |
| Mejoras de intervención siguen sin ser concluyentes con 10 réplicas | Conclusión sobre intervenciones debilitada | Reportarlas como no concluyentes con fundamento; la intermediación exacta es una mejora opcional (decisión A10) |
| Sin criterios de evaluación del profesor | No hay forma externa de saber si un objetivo está cumplido | Definir criterios propios por objetivo (tarea 2) |
| Dispersión hacia infraestructura | Menos tiempo para análisis | Lista de exclusiones de la sección 3 |

## 9. Preguntas abiertas e inferencias

Las decisiones abiertas con su responsable y lo que bloquean están en `docs/decisiones.md`, sección 2. Preguntas adicionales:

1. Nombre del profesor y criterios de evaluación.
2. Asignación de responsables por tarea (las fuentes no la respaldan).
3. Acceso a datos de la Secretaría de Movilidad.
4. Fuente del trazado y de las estaciones de Metro L1.

Inferencias a confirmar:

- Confirmado (línea base del 2026-11-09, `referencia_avance.csv`): los 4,8 y 4,2 de la diapositiva 12 son el cambio porcentual del R medio de 3 réplicas frente a la base (4,77% para A y 4,22% para B, celda 36). Se expresan en porcentaje, no en puntos de R. El "4 a 5%" del documento de contexto se refiere a esas dos cifras.
- La propuesta indica "aristas = rutas" para Gtransporte. Se interpreta que en espacio P dos estaciones se unen si comparten ruta y en espacio L si son consecutivas (según la diapositiva 4 de la presentación). La regla exacta de construcción se define en la tarea 10.
- La presentación de avance lista "Metro L1" y "10 réplicas de R" como siguiente fase, sin precisar si las 10 réplicas aplican a A y B de Gvial, a Metro L1 o a ambas. Se aplican a las tres intervenciones (confirmado por Juan Esteban Correa el 2026-11-09).
- Confirmado (línea base del 2026-11-09, `referencia_avance.csv`): las tres macrozonas (957, 825 y 718 nodos) son las tres componentes grandes tras 7 pasos de ataque adaptativo; los 703 nodos restantes quedan en componentes pequeñas (la cuarta tiene 38).
- Confirmado (línea base del 2026-11-09, `referencia_avance.csv`): el "por km" de B usa los kilómetros de vía intervenida. -15,12% / 36,39 km (Carrera 68 con 20,08 km y Carrera 50 con 16,30 km) = -0,415% por km.
- La diapositiva 12 nombra la intervención B como "Cra. 68 y 50". Se escribe "Carrera 50", como en la presentación y en el documento de contexto.
- Se asume que Gtransporte se analiza con el mismo pipeline y las mismas métricas que Gvial, según la decisión metodológica registrada.

## 10. Criterios de éxito

- `01_gvial` y `02_gtransporte` corren de arriba abajo en un entorno de Colab nuevo, desde una cuenta de Google distinta a la del autor, sin cambios, y obtienen las cifras del informe.
- Cada cifra del informe se traza a un CSV y a la celda que lo generó.
- Las diferencias con las cifras del avance están explicadas por escrito.
- La comparación entre Gvial y Gtransporte usa las mismas métricas y responde cuál red es más frágil y por qué.
- La robustez de las intervenciones se reporta con 10 réplicas pareadas del índice R, con resultado concluyente o declarado no concluyente con fundamento.
- Gtransporte se entrega en espacio L y en espacio P, con la intervención Metro L1, tal como se anunció en la presentación de avance y en la propuesta.
- Los supuestos usados para cubrir fuentes faltantes (GTFS, trazado de Metro L1) están documentados y declarados como limitación.
- El informe cumple esta estructura: 1. Pregunta y motivación. 2. Marco teórico. 3. Datos y construcción de las redes (Gvial, Gtransporte en L y P). 4. Metodología (métricas, ataques, cascada, intervenciones, índice R). 5. Resultados de Gvial. 6. Resultados de Gtransporte. 7. Intervenciones y robustez (A, B, Metro L1). 8. Comparación entre redes y entre espacios. 9. Conclusiones. 10. Limitaciones y supuestos. Anexo: cómo reproducir el análisis.
- No hay criterios del profesor: estos criterios los definió el equipo (tarea 2).

Plan de tareas: `PLAN.md`.
