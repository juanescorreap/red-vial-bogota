# Plan

Estado: [ ] pendiente, [~] en curso, [x] hecho, [!] bloqueado

Responsables: nadie ha sido asignado. La tarea 1 lo resuelve. Hasta entonces todas dicen "Por definir".

Los números de tarea son estables: las tareas añadidas el 2026-11-09 (20 a 24) llevan números nuevos y no alteran la numeración existente.

## Alcance fijo y gestión del tiempo

El alcance es fijo, sin recortes (decisión de Juan Esteban Correa, 2026-11-09): Gvial, Gtransporte en espacio L y en espacio P, intervención Metro L1 y 10 réplicas pareadas del índice R. Sin recortes, el riesgo de tiempo se gestiona así:

1. Calendario hacia atrás desde la fecha de entrega (tarea 2), con un hito de cierre por fase.
2. Punto de control al cerrar la línea base (tarea 4): se estima el esfuerzo del resto con datos reales de esa corrida y se compara con las semanas disponibles.
3. Escalamiento al equipo y al profesor en cuanto un hito se atrase, sin esperar al final. Quién escala: por definir (tarea 1).

No se conoce la fecha de inicio ni la de entrega final. El plan usa fases con semanas relativas hasta que la tarea 2 fije el calendario.

Referencia de hitos: el cronograma de la propuesta original dura 10 semanas (semanas 1 y 2 descarga y preprocesamiento, 3 a 5 análisis topológico y centralidad, 6 a 8 simulación de resiliencia y optimización, 9 y 10 redacción e informe final). No es la fecha de entrega. La asignación de tareas a esas bandas es propuesta del pm y se ajusta con la tarea 2.

| Hito (banda de la propuesta) | Fase del plan | Tareas que deben estar cerradas |
|---|---|---|
| Semanas 1 y 2: descarga y preprocesamiento | 0. Arranque; inicio de 1 y 2 | 1 a 5, 10, 11 |
| Semanas 3 a 5: análisis topológico y centralidad | 1. Gvial reproducible; grafos de Gtransporte | 6, 7, 12, 13, 20 |
| Semanas 6 a 8: simulación de resiliencia y optimización | 2. Gtransporte y robustez | 8, 9, 14, 15, 21, 22, 23, 24 |
| Semanas 9 y 10: redacción e informe final | 3. Cierre | 16, 17, 18, 19 |

| Fase | Semanas relativas | Contenido |
|---|---|---|
| 0. Arranque | 1 | Responsables, fecha y criterios, inventario, línea base, decisiones de Gvial |
| 1. Gvial reproducible | 2 a 3 | Módulo y `01_gvial` verificados contra la línea base |
| 2. Gtransporte y robustez | 3 a 5 (en paralelo con la fase 1 donde la dependencia lo permita) | Regla de construcción, grafos L y P, métricas, ataques y cascada; Metro L1; 10 réplicas de R. Duración por reestimar en el punto de control de la tarea 4 |
| 3. Cierre | 5 a 6 | Comparación, entorno de entrega, informe y revisión cruzada. Duración por reestimar en el punto de control de la tarea 4 |

## Contingencias de forma (no reducen alcance)

Solo cambian cómo se presenta el trabajo, no qué se entrega. Aceptadas como contingencias de forma por Juan Esteban Correa el 2026-11-09.

| Contingencia | Se aplica si |
|---|---|
| `03_comparacion.ipynb` pasa a ser la sección final de `02_gtransporte.ipynb` | menos de 3 semanas |
| Notebook único parametrizado en lugar del módulo (plan B, ver `docs/decisiones.md`). Con L, P y Metro L1 exige ramas por espacio e intervención, por lo que es poco recomendable | 3 semanas o menos al cerrar la línea base |

No se modifica en ningún caso: tareas 1 a 5, snapshot de grafos, `validar_contrato`, cifras calculadas en la corrida, celdas de texto por sección, el alcance de Gtransporte (L, P, Metro L1, con estructura, intermediación, concentración, resiliencia y cascada) ni las 10 réplicas pareadas de R.

## Arranque

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 1 | Asignar un responsable a cada tarea para que el trabajo de los cuatro integrantes quede repartido | Por definir (equipo) | | Columna Responsable completa en este archivo; persona que escala atrasos definida | [ ] |
| 2 | Confirmar con el profesor la fecha de entrega, el formato y los criterios de evaluación para fijar el calendario del alcance fijo | Por definir | | Fecha y criterios registrados en `docs/proyecto.md`; calendario hacia atrás con un hito por fase registrado en este archivo | [ ] |
| 3 | Inventariar los `.graphml` y las salidas del avance en Drive para saber si son los que produjeron las cifras presentadas | Por definir | | Lista con ruta, fecha de modificación y versiones de OSMnx y NetworkX usadas, o declaración de que no se conocen | [ ] |
| 4 | Registrar la línea base de cifras corriendo una copia del notebook histórico sobre los `.graphml`, para tener contra qué verificar cada paso del refactor y estimar con datos reales el esfuerzo restante | Por definir | 3 | `resultados/referencia_avance.csv` con `valor_presentado` y `valor_linea_base`; N y M contrastados con 3.203 y 5.175; grado medio 3,1, clustering 0,07, viaje medio 17,9 min, eficiencia -28% con 5% de nodos retirados y macrozonas de 825, 957 y 718 nodos contrastados; cifras de las intervenciones A y B de la presentación contrastadas; cada diferencia explicada por escrito; punto de control: estimación del esfuerzo del resto comparada con las semanas disponibles y compartida con el equipo y el profesor | [ ] |
| 5 | Cerrar las definiciones de Gvial (A3 a A7 y A9 de `docs/decisiones.md`; A8 ya está cerrada) para que cada cifra del informe tenga una sola definición | Por definir | 4 | Decisiones A3 a A7 y A9 con persona confirmante en `docs/decisiones.md` | [ ] |

## OE1. Gvial reproducible en Colab

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 6 | Obtener el módulo con contrato del grafo, estructura, intermediación, concentración y dependencia de velocidad, y `01_gvial` hasta esa etapa, para regenerar esas cifras sin estado global | Por definir | 4, 5 | N, M, grado medio (3,1), clustering (0,07), viaje medio (17,9 min), Gini, 1% superior, Spearman y top 10 de corredores idénticos a la línea base | [ ] |
| 7 | Incorporar resiliencia y cascada con f_c calculado y fracción efectiva registrada, para sostener 6,5%, 14%, el -28% de eficiencia con 5% retirado, las macrozonas (825, 957 y 718 nodos) y el 97% con código | Por definir | 6, 5 | Curvas y componentes idénticos a la línea base; f_c, eficiencia con 5% retirado, tamaño de macrozonas y 97% calculados; diferencia con las cifras escritas a mano documentada; diferencia entre los 2.500 nodos de las macrozonas y los 3.203 de la red explicada | [ ] |
| 8 | Incorporar las intervenciones A y B con todas las réplicas calculadas en la corrida, para eliminar los valores de corridas anteriores | Por definir | 7 | A: carga NQS -0,2% (-0,05% por km), tiempo entre zonas -0,8%, eficiencia +0,04%. B: carga NQS -15,1% (-0,41% por km), tiempo -3,8%, eficiencia +1,5%. Todos idénticos a la línea base; base del "por km" de B documentada; ningún valor numérico de resultado escrito a mano en el código | [ ] |
| 9 | Completar `01_gvial` con texto por sección y figuras generadas desde CSV, para que el profesor lo ejecute de arriba abajo en Colab | Por definir | 8 | Ejecución limpia en entorno nuevo por un integrante distinto al autor; celda 40 sin error | [ ] |

## OE2. Gtransporte con el mismo pipeline

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 10 | Definir cómo se modela Gtransporte en espacio L y en espacio P (fuente GTFS y respaldos, aristas, pesos por tiempo y frecuencia, `travel_time`, transbordos, aplicación del contrato) para que sea comparable con Gvial | Por definir | 2 | Decisión A11 con persona confirmante y reglas de ambos espacios escritas en `docs/specs/` | [ ] |
| 11 | Verificar la vigencia y la licencia de la fuente, y que traiga rutas, viajes y frecuencias, y congelarla en `data/raw/gtransporte/` para poder reconstruir los grafos | Por definir | 10 | Fuente elegida con fecha en el nombre, nota de licencia y verificación de rutas y frecuencias; si falla, respaldo o supuesto de A11 aplicado y documentado | [ ] |
| 12 | Construir el grafo de TransMilenio en espacio L que cumpla el contrato, para ejecutar el pipeline sin cambios en el núcleo | Por definir | 6, 11 | `validar_contrato` pasa; conteo de nodos y aristas verificado contra la fuente; grafo en Drive | [ ] |
| 13 | Calcular estructura, intermediación exacta, concentración, resiliencia y cascada de Gtransporte en espacio L para medir su fragilidad | Por definir | 7, 12 | CSV en `resultados/gtransporte/` (espacio L), curvas de ataque aleatorio y adaptativo y `02_gtransporte` con texto por sección | [ ] |
| 20 | Construir el grafo de TransMilenio en espacio P (estaciones unidas si comparten ruta, pesos por tiempo y frecuencia) para modelar su estructura por rutas | Por definir | 10, 12 | Grafo en Drive; validación acorde con la regla de la tarea 10 aprobada; nodos coincidentes con los del espacio L o diferencia explicada; aristas verificadas contra las rutas de la fuente | [ ] |
| 21 | Calcular las mismas métricas de la tarea 13 en espacio P para contrastar la fragilidad de la red por rutas | Por definir | 13, 20 | CSV en `resultados/gtransporte/` (espacio P) con las mismas columnas que el espacio L y sección de `02_gtransporte` con texto | [ ] |
| 22 | Modelar Metro Línea 1 como variante del grafo de Gtransporte en espacio L para poder evaluarlo como intervención | Por definir | 10, 12 | Decisión A12 registrada; variante del grafo con estaciones y conexiones nuevas que pasa `validar_contrato`; fuente o supuesto del trazado documentado con fecha; supuestos de tiempo de viaje escritos | [ ] |

## OE3. Robustez de las intervenciones

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 14 | Medir el tiempo de 10 réplicas pareadas del índice R en Colab para confirmar que caben en una sesión y fijar el esquema de semillas pareadas y de guardado por réplica | Por definir | 8 | Tiempo medido en Colab; esquema de semillas escrito; decisión A10 (añadir o no la intermediación exacta) registrada | [ ] |
| 15 | Establecer si la mejora de R de las intervenciones A y B es real con 10 réplicas pareadas (sustituye las 3 réplicas del avance) | Por definir | 14 | R por réplica y escenario en CSV; media y dispersión de las diferencias pareadas; unidad de R (porcentaje o puntos) confirmada; si no hay conclusión, declaración de no concluyente con su fundamento | [ ] |
| 23 | Evaluar Metro L1 sobre Gtransporte con las métricas de intervención aplicables y R con 10 réplicas pareadas, igual que A y B, para medir cuánto cambia la fragilidad | Por definir | 14, 22, 13 | CSV de resultados antes y después en `resultados/gtransporte/`; R con 10 réplicas pareadas; resultado concluyente o declarado no concluyente con fundamento | [ ] |

## OE4. Comparación entre redes

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 16 | Contrastar Gvial y Gtransporte (espacio L) con métricas relativas, incluidas las intervenciones comparables (A y B frente a Metro L1), para responder cuál es más frágil y por qué | Por definir | 9, 13, 15, 23, 24 | Tabla en `resultados/comparacion/`; cada cifra apunta a un CSV y a la celda que lo generó; párrafo interpretativo | [ ] |
| 24 | Contrastar el espacio L y el espacio P de Gtransporte para mostrar qué conclusiones dependen de cómo se modela la red | Por definir | 13, 21 | Tabla en `resultados/comparacion/` con las mismas métricas en ambos espacios; párrafo que indica qué cambia y qué no | [ ] |

## OE5. Informe final

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 17 | Dejar Drive y repo listos para que el profesor reproduzca el análisis | Por definir | 9, 13, 21, 23 | Instrucciones de acceso a la carpeta en la primera celda de cada notebook; la carpeta abre desde una cuenta distinta a las del equipo | [ ] |
| 18 | Redactar el informe con la estructura exigida para que el profesor evalúe la metodología | Por definir | 2, 16, 24 | Todas las secciones completas; cada cifra trazable a un CSV y a una celda | [ ] |
| 19 | Revisar el informe de punta a punta para garantizar coherencia y reproducibilidad | Por definir | 17, 18 | Revisión cruzada por un integrante distinto al redactor; cero cifras sin origen en una ejecución | [ ] |

## Dependencias de terceros

| Tercero | Qué se espera | Tarea | Último contacto |
|---|---|---|---|
| Profesor | Fecha de entrega, formato y criterios | 2 | Sin contacto registrado |
| Profesor | Validación del modelo de Gtransporte si cambia la pregunta | 10 | Sin contacto registrado |
| Profesor | Aviso de atrasos de hitos y resultado del punto de control de la línea base | 4 | Sin contacto registrado |
