# Plan

Estado: [ ] pendiente, [~] en curso, [x] hecho, [!] bloqueado

Responsable de todas las tareas: Juan Esteban Correa (2026-11-09).

Los números de tarea son estables: las tareas añadidas el 2026-11-09 (20 a 24) llevan números nuevos y no alteran la numeración existente.

## Alcance fijo y forma de avance

El alcance es fijo, sin recortes (decisión de Juan Esteban Correa, 2026-11-09): Gvial, Gtransporte en espacio L y en espacio P, intervención Metro L1 y 10 réplicas pareadas del índice R.

No hay fecha de entrega (decisión de Juan Esteban Correa, 2026-11-09): se avanza lo más posible, sin calendario. Juan Esteban Correa es responsable de todas las tareas. Con un solo responsable y sin fecha, el orden de trabajo lo fija el camino crítico:

1. Arranque: 3 (inventario) y 4 (línea base). La tarea 4 es la base de todo lo que sigue.
2. Mientras la línea base no esté, avanzar lo que no depende de ella: 10 y 11 (fuente de Gtransporte) y la definición de Metro L1 (A12).
3. Gvial reproducible (5 a 9), que entrega el módulo que usan las redes siguientes.
4. Gtransporte L y P (12, 13, 20, 21), Metro L1 (22, 23) y robustez (14, 15).
5. Comparaciones (16, 24) e informe (17, 18, 19).

Referencia: el cronograma de la propuesta original duraba 10 semanas (semanas 1 y 2 descarga y preprocesamiento, 3 a 5 análisis topológico y centralidad, 6 a 8 simulación de resiliencia y optimización, 9 y 10 redacción e informe final). Se conserva solo como referencia del orden de las fases.

## Contingencias de forma (no reducen alcance)

Solo cambian cómo se presenta el trabajo, no qué se entrega. Aceptadas como contingencias de forma por Juan Esteban Correa el 2026-11-09.

| Contingencia | Se aplica si |
|---|---|
| `03_comparacion.ipynb` pasa a ser la sección final de `02_gtransporte.ipynb` | el notebook propio no aporta frente a una sección |
| Notebook único parametrizado en lugar del módulo (plan B, ver `docs/decisiones.md`). Con L, P y Metro L1 exige ramas por espacio e intervención, por lo que es poco recomendable | el módulo frena el avance más que lo que ahorra |

No se modifica en ningún caso: tareas 1 a 5, snapshot de grafos, `validar_contrato`, cifras calculadas en la corrida, celdas de texto por sección, el alcance de Gtransporte (L, P, Metro L1, con estructura, intermediación, concentración, resiliencia y cascada) ni las 10 réplicas pareadas de R.

## Arranque

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 1 | Asignar un responsable a cada tarea para que el trabajo quede repartido | Juan Esteban Correa | | Columna Responsable completa en este archivo | [x] |
| 2 | Definir criterios propios de evaluación del proyecto (no hay criterios del profesor ni fecha de entrega), para saber cuándo cada objetivo está cumplido | Juan Esteban Correa | | Criterios por objetivo (OE1 a OE5) registrados en `docs/proyecto.md` | [ ] |
| 3 | Inventariar los `.graphml` y las salidas del avance en Drive para saber si son los que produjeron las cifras presentadas | Juan Esteban Correa | | Lista con ruta, fecha de modificación y versiones de OSMnx y NetworkX usadas, o declaración de que no se conocen. Hecho: `docs/referencia/inventario_drive.md` | [x] |
| 4 | Registrar la línea base de cifras corriendo una copia del notebook histórico sobre los `.graphml`, para tener contra qué verificar cada paso del refactor | Juan Esteban Correa | 3 | `resultados/referencia_avance.csv` con `valor_presentado` y `valor_linea_base`; N y M contrastados con 3.203 y 5.175; grado medio 3,1, clustering 0,07, viaje medio 17,9 min, eficiencia -28% con 5% de nodos retirados y macrozonas de 825, 957 y 718 nodos contrastados; cifras de las intervenciones A y B de la presentación contrastadas; cada diferencia explicada por escrito Avance 2026-11-09: corrida local completa sobre el snapshot (`data/linea_base/`); 48 cifras en `referencia_avance.csv`, todas las presentadas coinciden o tienen la diferencia explicada en la columna `nota`. La celda 40 falla (hallazgo B1). La NQS como primera por carga por distancia quedó verificada con `01_gvial` (4 de 4 pruebas). Falta: subir el CSV a Drive en `resultados/` | [~] |
| 5 | Cerrar las definiciones de Gvial (A3 a A7 y A9 de `docs/decisiones.md`; A8 ya está cerrada) para que cada cifra del informe tenga una sola definición | Juan Esteban Correa | 4 | Decisiones A3 a A7 y A9 con persona confirmante en `docs/decisiones.md`. Hecho 2026-11-09, más A13 (asignación de tramos a corredores) | [x] |

## OE1. Gvial reproducible en Colab

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 6 | Obtener el módulo con contrato del grafo, estructura, intermediación, concentración y dependencia de velocidad, y `01_gvial` hasta esa etapa, para regenerar esas cifras sin estado global | Juan Esteban Correa | 4, 5 | N, M, grado medio (3,1), clustering (0,07), viaje medio (17,9 min), Gini, 1% superior, Spearman y top 10 de corredores idénticos a la línea base. Después, en un paso aparte, se aplican A6 (cortes 0,6 y 2) y A13 (nombres compuestos) y cada cifra que cambie queda en `resultados/gvial/cambios_definiciones.csv` (`valor_refactor` conserva la versión equivalente al avance). Avance 2026-11-09: `src/pipeline_redes.py`, `tests/test_pipeline_redes.py` y `notebooks/01_gvial.ipynb` reproducen las 23 cifras comparables de la línea base sin diferencias. Sección 9 corrida: con A6 y A13 hay 209 corredores (antes 135), el top 3 no cambia y entra Avenida Calle 57R Sur al top 10, el Spearman entre redes baja de 0,77 a 0,72 y los tipos coinciden con la presentación (`cambios_definiciones.csv`) | [x] |
| 7 | Incorporar resiliencia y cascada con f_c calculado y fracción efectiva registrada, para sostener f_c (definición de A5, presentado como 6,5% y 14%), el -28% de eficiencia con 5% retirado, las macrozonas (825, 957 y 718 nodos) y el 97% con código | Juan Esteban Correa | 6, 5 | Curvas y componentes idénticos a la línea base; f_c, eficiencia con 5% retirado, tamaño de macrozonas y 97% calculados; diferencia con las cifras escritas a mano documentada; f_c según A5 y curvas también contra la fracción efectiva (A9). Hecho 2026-11-09: curvas, cierres y registro del ataque idénticos fila por fila a los CSV del avance; E0, -28,5%, macrozonas y 97,3% coinciden. f_c calculado (A5): 6,3% adaptativo y 13,9% azar con pasos de 1%; con la definición del informe (pasos de 0,5%, fracción efectiva) 6,3% y 13,6% (`fc_informe.csv`) | [x] |
| 8 | Incorporar las intervenciones A y B con todas las réplicas calculadas en la corrida, para eliminar los valores de corridas anteriores | Juan Esteban Correa | 7 | A: carga NQS -0,2% (-0,05% por km), tiempo entre zonas -0,8%, eficiencia +0,04%. B: carga NQS -15,1% (-0,41% por km), tiempo -3,8%, eficiencia +1,5%. Todos idénticos a la línea base; base del "por km" de B documentada; ningún valor numérico de resultado escrito a mano en el código. Avance 2026-11-09: funciones de intervención y robustez en el módulo (34 pruebas) y sección 11 en `01_gvial`; candidatos de enlace verificados idénticos al avance; Hecho: 41 cifras coinciden; escenarios_robustez.csv idéntico; en escenarios_final.csv solo cambia el tercer decimal del cambio de R (4,777 frente a 4,775 en A y 4,226 frente a 4,224 en B) porque la primera réplica ya no se toma redondeada de otra corrida; las cifras presentadas (4,8 y 4,2) se mantienen | [x] |
| 9 | Completar `01_gvial` con texto por sección y figuras generadas desde CSV, para que el profesor lo ejecute de arriba abajo en Colab | Juan Esteban Correa | 8 | Ejecución limpia en un entorno de Colab nuevo, desde una cuenta de Google distinta a la del autor; celda 40 sin error | [ ] |

## OE2. Gtransporte con el mismo pipeline

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 10 | Definir cómo se modela Gtransporte en espacio L y en espacio P (fuente GTFS y respaldos, aristas, pesos por tiempo y frecuencia, `travel_time`, transbordos, aplicación del contrato) para que sea comparable con Gvial | Juan Esteban Correa | 2 | Decisión A11 con persona confirmante y reglas de ambos espacios escritas en `docs/specs/`. Hecho 2026-11-09: `docs/specs/gtransporte.md`; queda por verificar la correspondencia letra de ruta y troncal | [x] |
| 11 | Verificar la vigencia y la licencia de la fuente, y que traiga rutas, viajes y frecuencias, y congelarla en `data/raw/gtransporte/` para poder reconstruir los grafos | Juan Esteban Correa | 10 | Fuente elegida con fecha en el nombre, nota de licencia y verificación de rutas y frecuencias; si falla, respaldo o supuesto de A11 aplicado y documentado. Avance 2026-11-09: fuente elegida y verificada (A11: feed mdb-3358 de Mobility Database, copia del 2026-07-13, vigencia 2026, rutas y `stop_times` presentes). Falta: confirmar la licencia en http://www.simur.gov.co/gtfs y subir el ZIP a Drive como `data/raw/gtransporte/gtfs_transmilenio_2026-07-13.zip` Cerrada 2026-11-09: el notebook descarga la copia fija de Mobility Database y verifica su SHA-256 (bc1f00f2a4e36417655b95a4f4835e76457e7a26a140179f04f10adfc2a458e1); la copia en Drive queda como respaldo opcional; la licencia no se revisa (decisión de Juan Esteban Correa) | [x] |
| 12 | Construir el grafo de TransMilenio en espacio L que cumpla el contrato, para ejecutar el pipeline sin cambios en el núcleo | Juan Esteban Correa | 6, 11 | `validar_contrato` pasa; conteo de nodos y aristas verificado contra la fuente; grafo en Drive Hecho 2026-11-09: `src/gtfs_transmilenio.py`; L con 141 estaciones y 328 aristas, contrato OK; grafos guardados en `resultados/gtransporte/` (local; en Drive al correr en Colab) | [x] |
| 13 | Calcular estructura, intermediación exacta, concentración, resiliencia y cascada de Gtransporte en espacio L para medir su fragilidad | Juan Esteban Correa | 7, 12 | CSV en `resultados/gtransporte/` (espacio L), curvas de ataque aleatorio y adaptativo y `02_gtransporte` con texto por sección Hecho 2026-11-09: `notebooks/02_gtransporte.ipynb` ejecutado completo; f_c adaptativo 4,1% y azar 15,4% (efectiva); R = 0,444 | [x] |
| 20 | Construir el grafo de TransMilenio en espacio P (estaciones unidas si comparten ruta, pesos por tiempo y frecuencia) para modelar su estructura por rutas | Juan Esteban Correa | 10, 12 | Grafo en Drive; validación acorde con la regla de la tarea 10 aprobada; nodos coincidentes con los del espacio L o diferencia explicada; aristas verificadas contra las rutas de la fuente Hecho 2026-11-09: P con 141 estaciones y 6.995 aristas, contrato OK | [x] |
| 21 | Calcular las mismas métricas de la tarea 13 en espacio P para contrastar la fragilidad de la red por rutas | Juan Esteban Correa | 13, 20 | CSV en `resultados/gtransporte/` (espacio P) con las mismas columnas que el espacio L y sección de `02_gtransporte` con texto Hecho 2026-11-09: métricas de P en `02_gtransporte`; P no se fragmenta con 40% retirado (f_c no alcanzado) | [x] |
| 22 | Modelar Metro Línea 1 como variante del grafo de Gtransporte en espacio L para poder evaluarlo como intervención | Juan Esteban Correa | 10, 12 | Decisión A12 registrada; variante del grafo con estaciones y conexiones nuevas que pasa `validar_contrato`; fuente o supuesto del trazado documentado con fecha; supuestos de tiempo de viaje escritos Hecho 2026-11-09: `src/metro_l1.py`; 16 estaciones de OSM (extracción del 2026-11-09), 21,9 km de vía, 27 min de recorrido, 7 transbordos a 400 m o menos de 5 min; contrato OK | [x] |

## OE3. Robustez de las intervenciones

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 14 | Medir el tiempo de 10 réplicas pareadas del índice R en Colab para confirmar que caben en una sesión y fijar el esquema de semillas pareadas y de guardado por réplica | Juan Esteban Correa | 8 | Tiempo medido en Colab; esquema de semillas escrito; decisión A10 (añadir o no la intermediación exacta) registrada Hecho 2026-11-09 (medido en local; Colab no disponible): intermediación k=300 8,9 s y exacta 94,6 s por paso en la red arterial; R con 10 pasos 1,5 min frente a 16 min. Se aplica A10: 10 réplicas con k=300 y exacta solo si no es concluyente | [x] |
| 15 | Establecer si la mejora de R de las intervenciones A y B es real con 10 réplicas pareadas (sustituye las 3 réplicas del avance) | Juan Esteban Correa | 14 | R por réplica y escenario en CSV; media y dispersión de las diferencias pareadas; unidad de R (porcentaje o puntos) confirmada; si no hay conclusión, declaración de no concluyente con su fundamento Hecho 2026-11-09 (`03_robustez_gvial`): con 10 réplicas pareadas A da +1,9% (IC 95% -1,6 a 5,4) y B +2,4% (IC -0,6 a 5,4), no concluyentes; A+B +3,8% (IC 1,6 a 5,9), concluyente. Las 3 primeras réplicas reproducen exactamente las de `01_gvial`; el +4,8% y +4,2% de 3 réplicas eran ruido de muestreo | [x] |
| 23 | Evaluar Metro L1 sobre Gtransporte con las métricas de intervención aplicables y R con 10 réplicas pareadas, igual que A y B, para medir cuánto cambia la fragilidad | Juan Esteban Correa | 14, 22, 13 | CSV de resultados antes y después en `resultados/gtransporte/`; R con 10 réplicas pareadas; resultado concluyente o declarado no concluyente con fundamento Hecho 2026-11-09 (sección 9 de `02_gtransporte`): R +6,8% (10 réplicas idénticas: intermediación exacta), f_c adaptativo 4,1% a 5,0%, carga de la troncal 7 -36%, eficiencia entre estaciones TM +1,0%. La mejora de R no es monótona con el tiempo de transbordo (+23% con 3 min, +7% con 5, +25% con 10): el signo es estable, la magnitud no | [x] |

## OE4. Comparación entre redes

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 16 | Contrastar Gvial y Gtransporte (espacio L) con métricas relativas, incluidas las intervenciones comparables (A y B frente a Metro L1), para responder cuál es más frágil y por qué | Juan Esteban Correa | 9, 13, 15, 23, 24 | Tabla en `resultados/comparacion/`; cada cifra apunta a un CSV y a la celda que lo generó; párrafo interpretativo Avance 2026-11-09: `notebooks/04_comparacion.ipynb` con tablas en `resultados/comparacion/` (estructura, fragilidad, corredor crítico, intervenciones), cada una con su archivo de origen; 10 réplicas incorporadas e interpretación escrita en la sección 7 | [x] |
| 24 | Contrastar el espacio L y el espacio P de Gtransporte para mostrar qué conclusiones dependen de cómo se modela la red | Juan Esteban Correa | 13, 21 | Tabla en `resultados/comparacion/` con las mismas métricas en ambos espacios; párrafo que indica qué cambia y qué no Avance 2026-11-09: tabla `L_vs_P.csv` en `04_comparacion`; 10 réplicas incorporadas e interpretación escrita en la sección 7 | [x] |

## OE5. Informe final

| # | Tarea | Responsable | Depende de | Criterio de terminado | Estado |
|---|---|---|---|---|---|
| 17 | Dejar Drive y repo listos para que el profesor reproduzca el análisis | Juan Esteban Correa | 9, 13, 21, 23 | Instrucciones de acceso a la carpeta en la primera celda de cada notebook; la carpeta abre desde una cuenta distinta a las del equipo | [ ] |
| 18 | Redactar el informe con la estructura de la sección 10 de `docs/proyecto.md` para que el profesor evalúe la metodología | Juan Esteban Correa | 2, 16, 24 | Todas las secciones completas; cada cifra trazable a un CSV y a una celda | [ ] |
| 19 | Revisar el informe de punta a punta para garantizar coherencia y reproducibilidad | Juan Esteban Correa | 17, 18 | Revisión de punta a punta con la lista de criterios de la sección 10 de `docs/proyecto.md`, en una sesión distinta a la de redacción; cero cifras sin origen en una ejecución | [ ] |

## Dependencias de terceros

| Tercero | Qué se espera | Tarea | Último contacto |
|---|---|---|---|
| Profesor | Validación del modelo de Gtransporte si cambia la pregunta | 10 | Sin contacto registrado |
