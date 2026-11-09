# Gtransporte: red troncal de TransMilenio

Gtransporte representa la red troncal de TransMilenio en dos espacios: el espacio L, que describe la infraestructura física y es comparable con Gvial, y el espacio P, que describe la oferta de viajes directos sin transbordo. Ambos grafos cumplen el mismo contrato del núcleo (`validar_contrato` en `src/pipeline_redes.py`) y se analizan con las mismas funciones que Gvial.

## 1. Fuente

| Elemento | Valor |
|---|---|
| Datos | GTFS estático publicado por Transmilenio S.A. |
| Origen | Mobility Database, feed mdb-3358 (https://mobilitydatabase.org/feeds/gtfs/mdb-3358) |
| Copia | 2026-07-13, congelada en Drive como `data/raw/gtransporte/gtfs_transmilenio_2026-07-13.zip` |
| Vigencia del servicio | 2026-01-01 a 2026-12-31 (`feed_info.txt`) |
| Día de referencia | Día hábil: `service_id` activo de lunes a viernes e inactivo sábado y domingo |
| Archivos usados | `agency`, `routes`, `trips`, `stop_times`, `stops`, `shapes`, `calendar` |

## 2. Servicios y nodos

**Servicios incluidos.** Rutas de los operadores `Transmilenio-Troncal` y `Transmilenio-Dual` en el día de referencia. Quedan fuera los alimentadores, el SITP zonal, TransMiCable y las paradas de calle de las rutas duales (paradas sin `parent_station`).

**Nodos.** Cada nodo es una estación troncal: una parada de tipo estación (`location_type = 1`) que es `parent_station` de alguna parada atendida por los servicios incluidos. Las paradas hijas (vagones y accesos) se asignan a su estación.

| Atributo | Regla |
|---|---|
| Identificador | `stop_id` de la estación |
| `x`, `y` | Coordenadas de la estación proyectadas a EPSG:9377, en metros |
| Nombre | `stop_name` sin espacios sobrantes |

**Estaciones con el mismo nombre.** Las estaciones de igual nombre se fusionan en un solo nodo. El nodo fusionado toma el menor `stop_id`, las coordenadas del punto medio y todas las aristas de las estaciones originales; las aristas entre ellas se eliminan. En la copia de la fuente ninguna pareja de estaciones atendidas comparte nombre: Ricaurte figura dos veces entre las 152 estaciones del GTFS, pero los servicios incluidos solo atienden una. El tiempo de transbordo a pie entre estaciones no se modela.

**Troncal.** Cada estación pertenece a la troncal que indica su identificador sin los tres últimos dígitos (por ejemplo, las estaciones 2000 a 2016 forman la troncal 2). La equivalencia entre ese prefijo y el nombre comercial de la troncal se deduce de los nombres de sus estaciones y se presenta aparte.

## 3. Espacio L

**Regla de adyacencia.** Dos estaciones son adyacentes si son consecutivas sobre el trazado de alguna ruta, sin importar en qué estaciones para cada servicio. Para cada trazado (`shape_id`) usado por los viajes incluidos:

1. El trazado se proyecta a EPSG:9377.
2. Se toman todas las estaciones del grafo a 80 m o menos de la línea del trazado.
3. Las estaciones se ordenan por su posición a lo largo de la línea.
4. Cada par de estaciones distintas consecutivas genera una arista dirigida en el sentido del trazado.

La regla evita que los servicios expresos, que omiten estaciones intermedias, creen enlaces que no existen en la infraestructura.

**Descarte de artefactos.** Se eliminan las aristas cuya longitud sobre el trazado supera 4.000 m. Corresponden a trazados que hacen bucle en una terminal o recorren tramos sin estaciones troncales, por ejemplo Museo Nacional con Las Nieves a 25 km sobre el trazado.

**Atributos de arista.**

| Atributo | Regla |
|---|---|
| `length` | Mediana, entre trazados, de la distancia a lo largo de la línea entre las dos estaciones, en metros |
| `travel_time` | Mediana del tiempo programado entre la salida de la estación de origen y la salida de la de destino, en los viajes del día de referencia que paran en ambas de forma consecutiva, en segundos. Si ningún viaje para en ambas de forma consecutiva: `length` dividida por la velocidad comercial mediana de las aristas que sí tienen tiempo |
| `speed_kph` | `length / travel_time * 3,6` |
| `name` | "Troncal" seguido del prefijo, si ambas estaciones pertenecen a la misma troncal; "Conexión" seguido de los dos prefijos ordenados, si pertenecen a troncales distintas |

**Valores de control.** Con la copia del 2026-07-13 la regla produce 141 estaciones y 328 aristas dirigidas en una sola componente fuertemente conexa, con grado medio no dirigido de 2,4 y longitud mediana de arista de 789 m. Se descartan 6 aristas de más de 4.000 m. En 33 aristas ningún viaje para en ambas estaciones de forma consecutiva; su tiempo usa la velocidad comercial mediana, 18,6 km/h. El espacio P resultante tiene 6.995 aristas dirigidas.

## 4. Espacio P

**Regla de adyacencia.** Hay una arista dirigida de la estación a a la estación b si algún viaje incluido para en a y después en b. En el espacio P dos estaciones adyacentes se conectan sin transbordo.

**Atributos de arista.**

| Atributo | Regla |
|---|---|
| `travel_time` | Mediana del tiempo a bordo entre la salida de a y la llegada a b, en los viajes del día de referencia que paran en ambas en ese orden, en segundos |
| `length` | Longitud del camino más corto entre a y b en el espacio L, en metros |
| `frecuencia` | Buses por hora entre 6:00 y 9:00 del día de referencia: viajes que salen de a en esa franja y paran después en b, divididos entre 3 |
| `name` | Códigos de las rutas que conectan a con b, ordenados y unidos con " / " |

**Uso.** El espacio P se analiza con estructura, intermediación, concentración, resiliencia y cascada. El análisis por corredor no se aplica, porque sus aristas no corresponden a tramos físicos.

## 5. Diferencias con Gvial que el análisis declara

| Aspecto | Gvial | Gtransporte |
|---|---|---|
| Tiempo de viaje | Longitud a la velocidad máxima imputada por OSMnx (flujo libre) | Tiempo programado del GTFS, que incluye la operación del servicio |
| Transbordos | No aplica | No se modela el tiempo de transbordo ni el de espera |
| Fecha de los datos | OpenStreetMap, 2026-10-05 | GTFS, copia del 2026-07-13 |

## 6. Controles de construcción

- El grafo de cada espacio pasa `validar_contrato`.
- El número de estaciones coincide con el de estaciones atendidas por los servicios incluidos, menos las fusionadas.
- Toda arista del espacio L tiene `length` de 4.000 m o menos.
