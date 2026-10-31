# [Nombre del proyecto]

## Contexto
- Problema y objetivo: ver docs/proyecto.md
- Plan y responsables: ver PLAN.md
- Arquitectura: ver docs/arquitectura/

## Flujo de trabajo
1. Proyecto nuevo o cambio de fondo: pm encuadra en docs/proyecto.md.
2. arquitecto propone el diseño en docs/arquitectura/.
3. pm filtra las propuestas según el alcance y registra la decisión.
4. Espera mi aprobación del encuadre y del diseño.
5. pm escribe la spec de cada frente y actualiza PLAN.md.
6. Implementa en una rama por frente: feat/<tema>.
7. qa valida código y datos antes de cada commit.
8. insights interpreta los resultados validados, si es un análisis.
9. docs cierra: decisiones, documentación final, README.
10. Nunca hagas commit ni push sin que yo lo pida.

## Señal de fricción
Si la misma query o función se corrige más de dos veces, o crece la lógica de negocio en el SQL, detente y consulta al arquitecto antes del siguiente intento.

## Datos
- data/ y outputs/ nunca se versionan.
- Puedes leer data/ con scripts para analizar; en la conversación muestra solo agregados e ids de ejemplo.
- tests/ usa casos sintéticos, no datos reales.
