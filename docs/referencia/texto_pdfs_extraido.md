# Texto extraído de los PDF de referencia

Extracción automática con pypdf (2026-10-31) de los dos PDF de esta carpeta, para poder consultarlos sin abrirlos. Es texto plano: se pierden gráficos, tablas y orden visual. Los guiones largos y medios se cambiaron por guion simple. Ante una duda, manda el PDF.

- Presentacion_avance_redes_Bogota_rojo.pptx.pdf: presentación de avance (octubre 2026), 14 páginas.
- Nodos = estaciones TransMilenio.pdf: propuesta original del proyecto, 17 páginas.

```text
===== docs/referencia/Presentacion_avance_redes_Bogota_rojo.pptx.pdf 14
--- p1
Redes y Movilidad
en Bogotá
Caos y
ComplejidadPresentación de avance
Estructura de Redes y
Movilidad en Bogotá
Dónde y cómo es frágil la red vial
Andrés Pimienta  ·  Adriana Correa
Sebastián García  ·  Juan Esteban Correa
UTADEO  ·  Octubre 2026
--- p2
Redes y Movilidad
en Bogotá
Caos y
Complejidad
Contenido
De la pregunta a la intervención
Resumen
Estado del arte
Metodología
Resultados
Conclusiones
Referencias
ESTRUCTURA
 FLUJO
 FRAGILIDAD
 INTERVENCIÓN
--- p3
Redes y Movilidad
en Bogotá
Caos y
ComplejidadResumen
La NQS concentra; la cascada fractura
Red tras el ataque adaptativo: 3 macrozonas
¿Qué tramos concentran el flujo de Bogotá de forma que su falla degrada la conectividad, y qué
intervención reduce más esa concentración por kilómetro?
Modelamos Bogotá como un grafo dirigido ponderado por tiempo (3.203
intersecciones arteriales; 59.198 en la red completa). Medimos estructura y
betweenness, simulamos fallas y probamos dos intervenciones. La NQS
concentra el flujo, pero la red se fractura por cascada: un ataque adaptativo
necesita el 6,5 % de los tramos; el azar, el 14 %.
#1 NQS
corredor crítico en 4 de 4 pruebas
6,5 % vs 14 %
tramos para fracturar la red: ataque vs azar
3
--- p4
Redes y Movilidad
en Bogotá
Caos y
ComplejidadEstado del arte
LU & SHI (2007)
 YANG & AN (2021)
Espacio L
Espacio P
L: paradas consecutivas · P: misma ruta
En espacio P: mundo pequeño (σ > 1)
→ Lo usamos para modelar TransMilenio
falla
sobrecarga
El flujo se redirige al fallar un enlace
La alternativa se sobrecarga: cascada
→ Por eso nuestro ataque recalcula
Transporte: mundo pequeño y
cascadas

--- p5
Redes y Movilidad
en Bogotá
Caos y
ComplejidadEstado del arte
Red reproducible,
antecedente local
BOEING (2017)
OSMnx: redes viales desde OpenStreetMap
Descarga, corrige topología y analiza
→ Construye nuestro Gvial
DUARTE, BECERRA & NIÑO (2008)
Asignación de buses en TransMilenio
Dijkstra, colas y algoritmos genéticos
→ Antecedente con grafos en Bogotá
--- p6
Redes y Movilidad
en Bogotá
Caos y
ComplejidadMetodología
1. Construir
OSMnx · 2 niveles
peso = tiempo
2. Medir
Betweenness
ponderada por tramo
3. Atacar
Azar vs
adaptativo
4. Intervenir
Enlace nuevo
vs velocidad
5. Validar
Sensibilidad
y réplicas
↺  6 ajustes metodológicos
Validar → Medir, antes de escalar
Siguiente fase: Gtransporte
TransMilenio · espacios L y P
CUELLO DE BOTELLA
Tramo con alta betweenness: fracción de las rutas
más rápidas que lo cruzan
b(e) = Σ σst(e) / σst
Validamos el método en
Gvial primero
Python · NetworkX · OSMnx · GeoPandas · Colab
--- p7
Redes y Movilidad
en Bogotá
Caos y
ComplejidadResultados · Estructura
Bogotá es una red sin hubs
Distribución de grado (% de intersecciones; grados 1, 5 y 6 < 1 %)
1.0 2.0 3.0
0
20
40
60
80
8.0
73.0
18.0
73 % de las intersecciones tiene grado 3
Clustering casi nulo: red espacial planar
El riesgo está en tramos, no nodos
GRADO MEDIO  3,1
CLUSTERING  0,07
VIAJE MEDIO  17,9 MIN
3.203 INTERSECCIONES
59.198 EN RED COMPLETA
7
--- p8
Redes y Movilidad
en Bogotá
Caos y
ComplejidadResultados · Flujo
La NQS concentra el flujo urbano
Betweenness de arista ponderada por tiempo (escala log)
NQS · Cra. 30
1 % → 13,5 %
de los tramos concentra de toda la intermediación  ·  Gini 0,69
NQS: PRIMERA EN 4 DE 4 PRUEBAS
Por tiempo
 Por distancia
Red arterial
 Red completa
ρ de Spearman: 0,77 entre redes · 0,68 entre pesos
8
--- p9
Redes y Movilidad
en Bogotá
Caos y
ComplejidadResultados · Flujo
Tres tipos de corredor, tres remedios
Atraen por velocidad
NQS 2,8× · Transv. 35 9,4×
→ Gestionar la demanda
Estructurales
Ciudad de Cali 0,9× · Boyacá 0,8×
→ Añadir redundancia
Subutilizados
Cra. 68 (37 km/h) · Cra. 50 (34 km/h)
→ Mejorar velocidad: escenario B
9
--- p10
Redes y Movilidad
en Bogotá
Caos y
ComplejidadResultados · Fragilidad
Con 6,5 % de tramos, la red se fractura
Conectividad: componente gigante S(f)
Azar (media de 5) Ranking fijo Adaptativo
% de tramos retirados
1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0 11.0 12.0 13.0 14.0 15.0 16.0
0
0.2
0.4
0.6
0.8
1.0
Eficiencia global E(f)/E ₀
Azar (media de 5) Ranking fijo Adaptativo
% de tramos retirados
1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0 11.0 12.0 13.0 14.0 15.0 16.0
0
0.2
0.4
0.6
0.8
1.0
Transición abrupta entre 5 % y 7 %
6,5 %
colapso con ataque adaptativo
≈14 %
colapso con fallas al azar
−28 %
eficiencia con 5 % retirado, aún unida
10
--- p11
Redes y Movilidad
en Bogotá
Caos y
ComplejidadResultados · Fragilidad
La cascada corta costuras, no la NQS
1  NQS
2  Av. Boyacá
3  Autopista Norte · Cra. 68
4  Cra. 24 · Calle 19
5  Av. Ciudad de Cali
6  Corte: Cra. 86 · Cra. 7 · Calle 80
Flujo ≠ conectividad
El 97 % sigue físicamente unido; entre zonas solo quedan vías de un
sentido.
NORORIENTE · 825
CENTRO-OCC. · 957
SUR · 718
11
--- p12
Redes y Movilidad
en Bogotá
Caos y
ComplejidadResultados · Intervención
Gestionar rinde más que construir
A · Enlace nuevo 4,2 km B · Cra. 68 y 50 a 50 km/h
1.0 2.0 3.0
0
-5
-10
-15
0
5
-0.2
-15.1
-0.8
-3.8
4.8 4.2
*R: media de 3 réplicas pareadas, no concluyente. Modelo a flujo libre, sin congestión.
−15 %
carga de la NQS sin construir vías nuevas
A · Enlace B · Velocidad
Km nuevos 4,2 0
Carga NQS por km −0,05 % −0,41 %
Tiempo entre zonas −0,8 % −3,8 %
Eficiencia global +0,04 % +1,5 %
Siguiente fase
 GTRANSPORTE · ESPACIOS L/P
 METRO L1
 10 RÉPLICAS DE R
12
--- p13
Redes y Movilidad
en Bogotá
Caos y
ComplejidadConclusiones
Cuatro hallazgos, una respuesta
Tramos críticos: la NQS (flujo) y la Av. Ciudad de Cali y la Cra. 7 (costuras). Mejor intervención por
km: gestionar la velocidad de corredores subutilizados.
3,1
Red sin hubs: la fragilidad
está en tramos
1 % → 13,5 %
El flujo se concentra; la
NQS lidera
6,5 % vs 14 %
La cascada fractura con
la mitad de cierres
−15 %
Acelerar Cra. 68 y 50
descarga la NQS
13
--- p14
Redes y Movilidad
en Bogotá
Caos y
ComplejidadReferencias
Fuentes que sostienen el análisis
OSMNX
Boeing, G. (2017). OSMnx: New methods for acquiring, constructing, analyzing, and
visualizing complex street networks. Computers, Environment and Urban Systems, 65, 126-
139.
ANTECEDENTE
Duarte, Becerra & Niño (2008). Un modelo de asignación de recursos a rutas en el sistema
de transporte masivo TransMilenio.
MOVILIDAD
Hernández-Torres, E., Maldonado-Hinarejos, A., & Busdeker, S. (2020). Metodología de
análisis de sistemas de movilidad urbana basada en estructuras complejas. Transporte y
Territorio, (23), 1-24.
E GLOBAL
Latora, V., & Marchiori, M. (2001). Efficient behavior of small-world networks. Physical
Review Letters, 87(19), 198701.
ESPACIOS L/P
Lu, H., & Shi, Y. (2007). Complexity of public transport networks. Tsinghua Science and
Technology, 12(2), 204-213.
ÍNDICE R
Schneider, C. M., Moreira, A. A., Andrade, J. S., Havlin, S., & Herrmann, H. J. (2011).
Mitigation of malicious attacks on networks. PNAS, 108(10), 3838-3841.
CASCADA
Yang, H., & An, S. (2021). Robustness evaluation for multi-subnet composited complex
network of urban public transport. Alexandria Engineering Journal, 60(2), 2065-2074.
===== docs/referencia/Nodos = estaciones TransMilenio.pdf 17
--- p1
Estructura de
Redes y Movilidad
en Bogotá
Diagnóstico de Cuellos de Botella y Optimización
de Corredores Mediante Teoría de Grafos
Andrés Pimienta
Adriana Correa
Sebastián García
Juan Esteban Correa

--- p2
Introducción y
Justificación
Movilidad en Bogotá: retos y
congestión creciente
La ciencia de redes permite
analizar sistemas complejos
Diagnóstico y optimización para
mejorar la movilidad urbana
COMPARATIVA DE ESTRUCTURAS DE MOVILIDAD
MALLA VIAL FÍSICA
Geometría planar
VS
SISTEMA DE TRANSPORTE MASIVO
Estructura jerárquica
con concentradores

--- p3
Casos de
estudio
--- p4
Marco Teorico
TEORÍA DE GRAFOS
REDES ESPACIALES
GRAFOS PONDERADOS
--- p5
RED DE
TRANSFERENCIAS
RED DE RUTAS
 RED DE ESTACIONES
Estado del arte
COMPLEXITY OF PUBLIC TRANSPORT NETWORKS (2007)
Propone un enfoque metodológico basado en la teoría de redes complejas para clasificar y modelar los
sistemas de transporte público urbano en tres ciudades de China, Langfang, Jining y Dalian. Modelaron cada
red de tres formas distintas:
Alto coeficiente de
agrupamiento
Caminos promedio cortos
entre nodos
COMPORTAMIENTO CON CARACTERISTICAS DE RED DE MUNDO PEQUEÑO
Grado
Distribucion de grado
Longitud de camino promedio
Coeficiente de agrupamiento
RESULTADOSPARAMETROS DE ESTUDIO
--- p6
Estado del arte
Propone un marco metodológico avanzado integrando redes de transporte heterogéneas mediante la
combinación de redes de autobús y metro con reglas de transferencia espacial (<200m).
LA COMBINACIÓN DE GRAFOS Y TEORÍA DE COLAS CON ALGORITMOS GENÉTICOS PERMITE ENCONTRAR CONFIGURACIONES
DE FLOTA CASI ÓPTIMAS, ADAPTÁNDOSE A LA DEMANDA DINÁMICA DE LOS USUARIOS.
Integra algoritmos genéticos para
optimizar la asignación de buses y
frecuencias de salida
Aplica el algoritmo de Dijkstra en
grafos como preprocesamiento para
rutas óptimas. 
VARIABLES CLAVEMETODOLOGÍA Y MODELO EVALUACIÓN
Simulación experimental sobre 400
buses, 7 rutas y 100.000 usuarios 
Reducción de tiempos promedio de
viaje de 1432 a 689 minutos a nivel
global
Flujo e interacción: Distribución de
Poisson para la llegada de buses a
estaciones. 
Tiempos de espera: Distribución
Erlang basada en cupo y saturación
Función objetivo: Minimización del
tiempo total del usuario (tviaje 
+tespera espera).
DUARTE, BECERRA Y NIÑO (2008) UN MODELO DE ASIGNACIÓN DE RECURSOS A
RUTAS EN EL SISTEMA DE TRANSPORTE MASIVO TRANSMILENIO.
--- p7
Estado del arte
Habla sobre el desarrollo de un modelo de optimización para la asignación de buses y frecuencias en la
troncal de Américas del sistema de Transmilenio.
Coeficiente de tolerancia y
capacidad de enlaces (β).
Fuerza de acoplamiento
nodal y en aristas (ϑ1, ϑ2).
Perturbación externa por
clima extremo (edv).
HALLAZGO PRINCIPAL: LAS REDES DE TRANSPORTE MUESTRAN UN COMPORTAMIENTO LIBRE DE ESCALA (SCALE-FREE), DONDE
FALLAS LOCALES PROVOCADAS POR CONDICIONES EXTREMAS SE AMPLIFICAN Y PUEDEN DESENCADENAR UN COLAPSO SISTÉMICO
TOTAL.
Integra red de autobuses y metro en
una red compleja compuesta
multired.
Establece reglas de transferencia
espacial basadas en umbrales de
distancia (<200m).
Considera la heterogeneidad real en
capacidad y flujos operativos.
VARIABLES CLAVEMODELO MSCCN
 EVALUACIÓN
Simulación de fallas en cascada
impulsada por redirección de flujos.
Operador sintético de robustez (R)
combinando tamaño, eficiencia y
tráfico.
Aplicación práctica en el sistema de
transporte de Qingdao.
MULTI-SUBNET COMPOSITED COMPLEX NETWORK (MSCCN) - YANG & AN (2021)
--- p8
Estado del arte
NEW METHODS FOR ACQUIRING, CONSTRUCTING, ANALYZING, AND VISUALIZING
COMPLEX STREET NETWORKS
Examina las limitaciones metodológicas e instrumentales en el estudio urbano basado en grafos y presenta OSMnx, una
librería de Python para descargar, construir, corregir topológicamente y analizar redes viales complejas a partir de
OpenStreetMap de forma sencilla, consistente y automatizada
1.Diagnóstico: Muestras pequeñas, simplficación excesiva, dificultad de replicación, falta de herramientas integradas
2.Adquisición de datos: Descarga multiproposito, Tipos de redes especificas y flexibilidad de consulta
3.Correción topológica: Simplificación de redes, topológia no planar real
4.Análisis avanzado y visualización: Métricas urbanas, ruteo y topologia, exportación versátil 
--- p9
Objetivos
Analizar la estructura de redes viales y de
transporte público en Bogotá para
diagnosticar cuellos de botella y proponer
optimizaciones basadas en teoría de grafos.
Construcción
de Grafos
Gvial y Gtransporte
Métricas de
Conectividad
Simulación
de Resiliencia
Propuesta de
Optimización
--- p10
Alcance y Modelamiento
Red Vial
Física (Gvial)
Nodos = intersecciones
Aristas = tramos viales
Datos obtenidos
con OSMnx
Pesos asignados
por distancia y tiempo
Red de Transporte
Público
(Gtransporte)
Nodos = estaciones
TransMilenio
Datos GTFS
Pesos por tiempo
y frecuencia
Aristas = rutas
--- p11
Metodología -
Fases 1 y 2
1
Preprocesamiento
y construcción de
grafos
Filtrado y limpieza de datos
Generación de matrices
de adyacencia
2
Métricas topológicas
y centralidad
Diámetro, ruta promedio,
eficiencia global
Distribución de grado,
strength, betweeness,
closeness
--- p12
Metodología
Fases 3 y 4
03
Simulación
de Resiliencia
Remoción de nodos:
fallos aleatorios vs
ataques dirigidos a
cuellos de botella
04
Escenarios de
Optimización
Inserción de nuevo
corredor vial y de
transporte público
HERRAMIENTAS UTILIZADAS
Python con librerías NetworkX, OSMnx,
GeoPandas y SciPy
--- p13
TIEMPO TOTAL
10
SEMANA 1-2
 SEMANA 3-5
 SEMANA 6-8
 SEMANA 9-10
01
Descarga y
Preprocesamiento
02
Análisis Topológico
y Centralidad
03
Simulación de
Resiliencia y
Optimización
04
Redacción e
Informe Final
SEMANAS
Cronograma
de Trabajo
--- p14
Cronograma de Trabajo
--- p15
Referencias Bibliográficas
Cardillo, O., Gómez, J. E., & Montoya-Torres, J. R. (2006).
Traffic modularity and robustness under failures, attacks and
strategies. Physica A: Statistical Mechanics and Its
Applications, 363(2), 593-606.
Hernández-Torres, E., Maldonado-Hinarejos, A., & Busdeker, S. (2020).
Metodología de análisis de sistemas de movilidad urbana basada
en estructuras complejas. Caso de estudio: Celaya, Guanajuato.
Trans. Rev. Transp. Territ., (23), 1-24.
--- p16
Referencias Bibliográficas
Lu, H., & Shi, Y. (2007).
Complexity of public transport networks. Tsinghua Science
and Technology, 12(2), 204-213.
Yang, H., & An, S. (2021).
Robustness evaluation for multi-subnet composited complex
network of urban public transport. Alexandria Engineering
Journal, 60(2), 2065-2074.
--- p17
Referencias Bibliográficas
Boeing, G. (2017).
OSMnx: New methods for acquiring, constructing, analyzing,
and visualizing complex street networks. Computers,
environment and urban systems, 65, 126-139.
```
