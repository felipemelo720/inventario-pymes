# Metodología de Desarrollo Ágil 2026-P — Proyecto Scrum "Inventario ligero para Pymes"

Ramo INACAP (sede Valdivia), docente **Omar Ignacio Cabrera Quiroga**. Referencia completa de teoría, requisitos y evidencias. Lo esencial para programar está en `../CLAUDE.md`.

Rutas relativas de este archivo (`Documentos INACAP/`, `Primera entrega/`, `Sprint 1/`) están bajo `~/inacap/metodologia-agil/`.

---

## Fuentes

| Ubicación | Contenido |
|---|---|
| `Documentos INACAP/` | PDFs del docente (vienen del zip de OneDrive del equipo) |
| `Primera entrega/` | Planillas de la primera entrega (backlog, sprint planning) |
| `Sprint 1/` | Plan, código, minutas, tablero, burndown del Sprint 1 |
| `Sprint 2/` (solo en el zip del 23-10, no copiado) | Plan "Que debe hacer cada uno", tablero, Sprint Planning, dailies, minutas, burndown del Sprint 2 |
| `~/inacap/api-inacap/descargas/Metodología de Desarrollo Ágil 2026_P/` | Todo lo bajado de la plataforma por el scraper (incluye material que no está aquí) |
| `~/inacap/api-inacap/resumen_ramos/metodología_de_desarrollo_ágil_2026_p.md` | Resumen autogenerado; de baja calidad (texto sin espacios). Este archivo lo reemplaza |

Origen: `C:\Users\fmelo\Downloads\OneDrive_1_16-10-2026.zip` (16-10-2026). El zip trae `Sprint 1/` duplicado en la raíz, idéntico byte a byte a `Metodología Ágil/Sprint 1/`; solo se copió una vez.

Zip más reciente: `C:\Users\fmelo\Downloads\OneDrive_2026-10-23.zip` (23-10-2026, carpeta compartida de la PO). Trae `Sprint 2/` y cambios en `Sprint 1/` que la copia local no tiene: Scrum Board movido a `Sprint 1/Documentos/Scrum Board/ScrumBoard_InventarioPymes.xlsx` (ya no existe `Sprint 1/Tablero/Tablero_InventarioPymes.xlsx`), Daily 1 llenada, `Codigo/ejemplo base datos/inventario_pymes.sql` y `Notas clase.txt` con contenido. `Sprint 2/Codigo/` es idéntico a `Sprint 1/Codigo/`: el código de verdad está en el repo. OneDrive es la fuente; para actualizar, bajar el zip de nuevo.

Material que solo está en `~/inacap/api-inacap/descargas/...`: `2.-Criterios de Aceptacion.pdf`, `3.-Mazo_Scrum_Poker.pdf`, `4.-Guía de Uso - Planning Poker en Scrum.pdf`, `Ejercicio.pdf`, `IntroducciondesaroolloAgil.pdf` (17 láminas escaneadas, sin capa de texto: hay que renderizarlas para leerlas), `Metodologia_Agil_Epicas_Historias_Requerimientos.pdf`, `Infografia.png`, `TablaAprobacion.jpeg`, `enlaces.md` (Scrum Poker online: https://www.scrumpoker-online.org/es/).

Material que solo está aquí: `4.-Metodo_MoSCoW.pdf`, `Esquema_Proyecto_Agil_Ejemplos.pdf`.

`2.-` y `5.-PresentaciónScrumSprintPlanning.pdf` son la misma presentación (solo cambian espacios).

Para extraer texto: `pdf-parse`, `mammoth` y `xlsx` están en `~/inacap/api-inacap/node_modules`. Varios PDFs salen con las palabras pegadas (sin espacios); leer con cuidado.

---

## Aprobación del ramo (`TablaAprobacion.jpeg`)

| Tipo | Modalidad | Nota aprobación | Eximición | Asistencia mínima |
|---|---|---|---|---|
| Lectiva | Presencial | 4,0 | 5,0 | 50% |
| Práctica | Presencial | 4,0 | No aplica examen final | 60% |
| Lectiva o práctica | Online | 4,0 | Sin eximición | No aplica |
| Lectiva / Práctica | Semipresencial | 4,0 | Sin eximición / no aplica examen | 70% horas presenciales |

Por confirmar qué tipo de asignatura es este ramo.

Trabajo Scrum (`3.-Trabajo_Scrum_Guia.pdf`): aprobación sugerida **≥ 60 pts**. **Bonus +5** por automatizar pruebas básicas o CI/CD simple.

---

## Teoría condensada

### Conceptos base (`IntroducciondesaroolloAgil.pdf`, `Infografia.png`)
- Proyecto: complicado, incierto, cambiante. Triángulo **Time / Cost / Scope** con **Quality** al centro.
- PMI: llevado por personas, recursos limitados, planificado + ejecutado + controlado.
- Scrum no define "proyecto": prioriza producto y entregar valor cada poco tiempo.
- **Manifiesto Ágil**: individuos e interacciones > procesos y herramientas; software que funciona > documentación exhaustiva; colaboración con el cliente > negociación de contratos; respuesta al cambio > seguir un plan.
- Principios: colaboración, entregas frecuentes, adaptación al cambio, mejora continua, valor para el cliente.
- Ciclo ágil: planificación, backlog, sprint, desarrollo, pruebas, entrega, retroalimentación, mejora continua.

### XP (eXtreme Programming)
- Valores: simplicidad, comunicación, realimentación, coraje, respeto.
- Prácticas: desarrollo iterativo e incremental, pruebas unitarias continuas, programación en pareja, sincronía con el cliente, corrección inmediata de errores, refactorización continua, propiedad compartida del código, simplicidad ("hacer solo lo que se pide").
- Roles: Customer (define funcionalidades y prioridad), Developer (desarrollo + pruebas unitarias), Coach (controla el método, interlocutor con el cliente), Tracker (mide avance y éxito de cada ciclo).

### Kanban
- Taiichi Ohno, 1953. *kan* = visual, *ban* = tarjeta.
- Reglas: visualizar el flujo (Pendiente / En curso / Hecho), **limitar el WIP** (caso simple: en "En curso" no más tareas que personas), medir **lead time** (Pendiente a Hecho) y cycle time.
- Kanban vs Scrum board: Kanban limita WIP por columna y es continuo; el Scrum board no limita WIP a priori y se limpia al terminar cada sprint.

### Scrum (`1.-Flujo de Trabajo SCRUM.pdf`)
- Control empírico: **transparencia, inspección, adaptación**. Equipos autogestionados y multifuncionales.
- Roles:
  - **Product Owner**: una sola persona, maximiza valor, ordena el Product Backlog, acepta o rechaza.
  - **Scrum Master**: asegura que se adopte Scrum; facilita, no dirige ni gestiona el desarrollo.
  - **Equipo de desarrollo**: sin jerarquías, todos "desarrollador", 3 a 9 personas.
- Sprint: máximo 1 mes, cada uno es un proyecto independiente que produce un incremento usable.
- Timeboxes (sprint de 1 mes; proporcional si es más corto):

| Evento | Sprint 1 mes | Sprint 2 semanas |
|---|---|---|
| Sprint Planning | 8 h | 4 h |
| Daily Scrum | 15 min, de pie | 15 min |
| Sprint Review | 4 h | 2 h |
| Retrospectiva | 3 h | 1,5 h |

- Daily: ¿qué hice?, ¿qué haré?, ¿qué impedimentos tengo?
- Artefactos: Product Backlog (ordenado por valor, riesgo, prioridad; nunca terminado), Sprint Backlog (lo modifica solo el equipo; requerimientos nuevos van al Product Backlog), Monitoreo de progreso (trabajo restante, burndown), Incremento (solo ítems terminados; lo incompleto vuelve al backlog con prioridad alta).
- Ciclo de vida: planeación, puesta en escena, desarrollo, entrega.

### Épicas e historias (`Metodologia_Agil_Epicas_Historias_Requerimientos.pdf`)
- Jerarquía: visión, épicas, historias, tareas técnicas. Flujo: problema, requerimiento, épica, historias, sprint.
- Épica: amplia, estratégica, contiene varias historias, se divide antes del sprint. Formato: nombre, objetivo, usuarios impactados, valor esperado, alcance, métrica de éxito.
- Historia: **Como [rol] quiero [necesidad] para [beneficio]**.
- **INVEST**: Independiente, Negociable, Valiosa, Estimable, Small, Testeable.
- Formato completo: ID, título, historia, criterios de aceptación, prioridad, estimación (story points), reglas de negocio, dependencias.
- Levantamiento: entrevistas, observación, workshop, prototipos. Documentos: acta de entrevista, mapa de proceso, matriz RF/RNF, glosario, reglas de negocio, prototipo + feedback.
- Matriz valor/esfuerzo: alto valor y bajo esfuerzo se hace primero; alto/alto se planifica; bajo/bajo se evalúa; bajo valor y alto esfuerzo se evita.

### Criterios de aceptación (`2.-Criterios de Aceptacion.pdf`)
- Claros, específicos (una condición cada uno), verificables, **binarios**, definidos al crear la historia, enfocados en el usuario. Funcionan como contrato con el PO.
- Formato **Dado / Cuando / Entonces**.
- Separar reglas de negocio de criterios de aceptación.

### Estimación: Planning Poker
- Mazo Fibonacci modificado: `0, ½, 1, 2, 3, 5, 8, 13, 20, 40, 100, ?, ∞`. Story points = esfuerzo relativo + complejidad + riesgo, **no horas**.
- 20 o más: conviene dividir. `?` = falta información. `∞` = refinar o dividir.
- Dinámica: el PO lee la historia, cada uno elige en secreto, se revela a la vez, los extremos argumentan, se vuelve a votar hasta llegar a consenso. Ejemplo del curso: push notifications, votos 3 y 13, consenso en 8.
- No "negociar puntos". Si hay alta incertidumbre: **Spike** (investigación con timebox).

### Priorización MoSCoW (`4.-Metodo_MoSCoW.pdf`)
- **Must** (sin esto la entrega no es viable), **Should** (impacto alto, hay alternativa temporal), **Could** (deseable, primero en salir si falta capacidad), **Won't this time** (fuera de esta entrega por acuerdo).
- Prueba del Must: "¿detendríamos la entrega sin esta historia?".
- DSDM: Must ≤ ~60% del **esfuerzo** (no de la cantidad de historias), Should ~20%, Could ~20%.
- En Scrum MoSCoW complementa: clasificar, luego ordenar dentro de cada categoría (valor, riesgo, dependencias), luego planificar según capacidad. El orden del backlog lo decide el PO.
- Alertas: todo es Must, historias que mezclan necesidades, nadie explica el impacto de aplazar.

### Sprint Planning (`2.-/5.-PresentaciónScrumSprintPlanning.pdf`, `Clase_Sprint_Planning_Extendido.xlsx`)
- Inputs (24-48 h antes): backlog priorizado con INVEST, borrador de Sprint Goal, velocidad histórica, capacidad, calendario, DoR/DoD.
- Capacidad:
  ```
  Capacidad_horas = Σ(miembros) × horas_efectivas_día × días_sprint − horas_ceremonias − horas_ausencias
  Rango_puntos ≈ Velocidad_histórica ± (10–20%)
  ```
  Ejemplo de clase: 5 × 6 × 10 = 300 − 20 − 20 = 260 h; velocidad 28, buffer 10%, rango 25,2 a 30,8.
- Pasos con timebox (sprint de 2 semanas, ≈ 4 h): apertura 10 min, capacidad 20, selección 30, aclaraciones + estimación 90, desglose en tareas de 4-8 h 60, riesgos/orden 20, cierre y compromiso 10.
- Salida: Sprint Goal aprobado, Sprint Backlog (historias + tareas + dueños), tablero To Do / In Progress / Review / Done.
- **DoR**: entendida, CA claros, datos/UX disponibles, sin bloqueos críticos, estimada.
- **DoD**: código + pruebas pasan, code review, integrado/deployable, documentado, aceptado por el PO.
- Antipatrones: comprometer puntos por presión, saltarse la DoR, diseñar todo el sistema en el planning, olvidar QA/datos/devops, esconder trabajo no planificado.

### Esquema de proyecto ágil (`Esquema_Proyecto_Agil_Ejemplos.pdf`)
Kick-off (visión, Product Vision Statement), levantamiento (HU + backlog), Sprint Planning, sprints (1-4 semanas + daily), Review (feedback del cliente), Retro (lo bueno / lo malo / propuesta de mejora), cierre (lecciones aprendidas).

### Casos de clase
- **GreenMarket** (Sprint Planning): pago seguro (1), carrito en tiempo real (2), seguimiento de pedido (3), registro con redes (4), notificaciones (5).
- **Taller automotriz** (épicas/HU): 2 épicas, 6 HU, 3 CA por historia crítica, backlog con puntos, mini Sprint 1. `Product Backlog.xlsx` de descargas tiene HU-INV-001 "Registro de Repuestos" como ejemplo.
- **Reserva de laboratorios** (`Ejercicio.pdf`): prototipo con pantallas de inicio, consulta de salas, fecha, horario y confirmación; 3 avances incrementales; líder y cronograma.

---

## Trabajo del curso: requisitos (`3.-Trabajo_Scrum_Guia.pdf`)

- Duración: 2 sprints de 2 semanas **o** 3 sprints de 1 semana. Casos posibles: e-commerce, reservas de salas, **inventario para Pymes** (elegido: altas/bajas, alerta de stock bajo, exportar a CSV). Tecnología libre; se evalúa el proceso ágil y un incremento demostrable.
- Hitos: semana 1 (backlog, DoR/DoD, estimación, Planning S1, tablero activo), semana 2 (dailies, Review + Retro S1), semanas 3-4 (S2, demo final, documentación).
- **Entregables**:
  - Product Backlog con **≥ 10 HU** (formato Como/quiero/para) y CA.
  - DoR y DoD como checklists.
  - Estimación (Planning Poker / story points) y capacidad por sprint.
  - Sprint Goal + Sprint Backlog.
  - Tablero To Do / In Progress / Review / Done **con historial real de movimiento**.
  - Burndown por sprint y velocidad.
  - Minutas de Review y Retro con acciones de mejora.
  - Incremento: demo en video de 3-5 min + repositorio o ZIP + Release Notes.
  - Informe final de 12 a 15 páginas: contexto, backlog, diseño ligero, planificación, métricas, aprendizajes, conclusiones.
- **Estructura de entrega**:
  ```
  /doc        informe PDF + DoR/DoD + minutas Review/Retro
  /boards     capturas del tablero por sprint
  /metrics    burndown(s) + resumen de velocidad
  /increment  binarios/ZIP o link al repo + video demo
  README.md   instrucciones de ejecución
  ```
- Reglas: el portavoz rota en las Reviews; el SM facilita y no dirige; los cambios de alcance se registran en el backlog; respetar los timeboxes; autoría propia y citar fuentes.

---

## Proyecto del equipo: Inventario ligero para Pymes

### Equipo
| Rol | Integrante |
|---|---|
| Product Owner | Anastasia Fuentes |
| Scrum Master | José Oporto (no programa; tablero, dailies, burndown, minutas, velocidad) |
| Dev | Antonella Pezzopane (HU-01, HU-05; S2: T-03, HU-02, HU-03) |
| Dev | Benjamín Ceballos (T-01 BD + conexión, HU-04; S2: T-03, HU-08, HU-10) |
| Dev | **Felipe Melo**, programador en jefe (HU-06; S2: HU-04, HU-06, T-02 pruebas) |

Stack acordado: **Python + MySQL, menú por terminal**. El código está en el repo privado https://github.com/felipemelo720/inventario-pymes y también se comparte por Google Drive.

### Calendario
- Sprints de **1 semana**: S1 desde 15-10-2026, S2 la semana siguiente, semana 3 de cierre (video, informe, README, Release Notes).
- Sprint 1 Goal: *registrar productos y controlar entradas y salidas de stock*.
- Sprint 2 Goal: *avisar cuando un producto tenga poco stock y exportar el inventario a CSV*.

### Product Backlog (`Sprint 1/Documentos/Sprint planning/Sprint_Planning_Inventario_Pymes(Sprint1).xlsx`)
| ID | Épica | Historia (resumen) | Prio | Valor | Sprint | Depende de |
|---|---|---|---|---|---|---|
| HU-01 | Productos | Registrar producto (nombre, SKU, categoría, stock inicial, mínimo; rechaza campos vacíos o SKU repetido) | 1 | Muy alto | S1 | T-01 |
| HU-05 | Movimientos | Entrada de stock (10 + 5 = 15; guarda movimiento con fecha) | 2 | Muy alto | S1 | HU-01 |
| HU-06 | Movimientos | Salida de stock (5 − 8 se rechaza y el stock queda en 5; si es válida, baja y guarda movimiento) | 3 | Muy alto | S1 | HU-01, HU-05 |
| HU-04 | Productos | Listado + búsqueda por nombre o SKU | 4 | Muy alto | S1 | HU-01 |
| HU-08 | Alertas | Aviso cuando stock ≤ stock mínimo | 5 | Muy alto | S2 | HU-01, HU-06 |
| HU-10 | Reportes | Exportar inventario a CSV (código, nombre, categoría, stock, mínimo; tildes OK en Excel) | 6 | Muy alto | S2 | HU-01 |
| HU-02 | Productos | Editar producto (sin vacíos ni SKU repetido) | 7 | Alto | S2 | HU-01 |
| HU-03 | Productos | Dar de baja producto con confirmación | 8 | Alto | S2 | HU-01 |
| HU-09 | Alertas | Listado de productos con stock bajo | 9 | Medio | Si sobra tiempo | HU-08 |
| HU-07 | Movimientos | Historial de movimientos por producto (más reciente primero) | 10 | Medio | Si sobra tiempo | HU-05, HU-06 |
| HU-12 | Acceso | Login con usuario y contraseña | 11 | Medio | Si sobra tiempo | T-01 |
| HU-11 | Reportes | Exportar movimientos por rango de fechas a CSV | 12 | Bajo | Si sobra tiempo | HU-07 |
| HU-13 | Acceso | Roles admin/vendedor (vendedor no puede dar de baja) | 13 | Bajo | Fuera de alcance | HU-12 |

Los CA de S1 están acordados; el resto es propuesta. Mapeo MoSCoW natural: Must = S1, Should = S2, Could = "si sobra tiempo", Won't = HU-13.

### Capacidad declarada (hoja "Cálculo de Capacidad")
5 miembros × 2 h/día × 5 días = 50 h, menos 15 de reuniones y 5 de ausencias = **30 h**. Velocidad histórica 0 (primer sprint), rango "0 - 0".

Sprint 2 (`Sprint_Planning_Inventario_PymesSprint2.xlsx`): misma capacidad (30 h), **velocidad del Sprint 1 = 11 pts** (T-01 3 + HU-01 3 + HU-05 5), buffer 10 %, rango **9,9 - 12,1 pts**. El tablero del Sprint 2 suma 28 pts: muy por encima del rango.

### DoR / DoD del equipo
- DoR: formato Como/quiero/para, CA claros, el equipo la entiende, estimada y priorizada, sin impedimentos.
- DoD: cumple CA, código hecho y probado, integrado al proyecto, documentación breve, aprobada por la PO.

### Tablero
Estados: Por hacer, En progreso, En revisión, Terminado. **Solo la PO pasa a Terminado.** Cada cambio de estado se anota en la hoja "Registro de movimientos" (vacía al 23-10).

Sprint 1, cierre (`Sprint 1/Documentos/Scrum Board/ScrumBoard_InventarioPymes.xlsx`, hoja "Sprint 1"): terminados T-01 (3 pts), HU-01 (3) y HU-05 (5), del 15 al 16-10. HU-04 (5) y HU-06 (2) quedan en progreso y pasan completas al Sprint 2; sus puntos no cuentan en la velocidad.

Sprint 2, estado al 23-10-2026 (`Sprint 2/Tablero/Tablero_Sprint2_InventarioPymes.xlsx` + 2 capturas):

| ID | Tarea | Responsable | Estado | Pts |
|---|---|---|---|---|
| T-03 | Juntar el código: una sola versión con el código de Antonella y la BD de Benjamín | Antonella, Benjamín | Terminado | 2 |
| HU-04 | Ver y buscar productos (viene del S1) | Felipe | En progreso | 3 |
| HU-06 | Salidas de stock sin quedar en negativo (viene del S1; revisar la versión de Antonella) | Felipe | En progreso | 2 |
| HU-08 | Alerta de stock bajo | Benjamín | Por hacer | 3 |
| HU-10 | Exportar a CSV | Benjamín | Por hacer | 5 |
| HU-02 | Editar productos | Antonella | En progreso | 3 |
| HU-03 | Dar de baja productos, con confirmación | Antonella | Por hacer | 5 |
| T-02 | Pruebas según los CA; anotar errores | Felipe | En progreso | 5 |

Total 28 pts, 26 pendientes. El tablero va atrasado respecto del código: HU-04 y HU-06 ya están hechas y probadas, y HU-02 y HU-03 están integradas en `main` local (PRs #1-#3).

### Plan del Sprint 2 (`Sprint 2/Que debe hacer cada uno.docx`)
- Orden: Planning (velocidad S1 + Planning Poker) → T-03 primero → HU-04 y HU-06 → HU-08, HU-10, HU-02, HU-03 → T-02 pruebas → Review → Retro.
- Si sobra tiempo (decide la PO): HU-09 y HU-07.
- Pendientes del S1: juntar el código (T-03), `CREATE DATABASE` + productos de prueba en el `.sql`, borrar `pyme.py`. Todo hecho en el repo.
- HU-03: baja lógica con columna `activo`, el listado muestra solo los activos. HU-08: aviso al abrir el menú o después de una salida. HU-10: `utf-8-sig` y `;`.
- **Felipe**: HU-06 (revisar la versión de Antonella y asegurar los CA) y T-02: probar todas las historias de S1 y S2 según los CA, avisar los errores al responsable, y una **tabla de casos de prueba** (por historia: qué se probó, qué debía pasar, qué pasó) como evidencia para el informe. Bonus +5 por pruebas automatizadas (ya hechas).
- Checklist de cierre del S2: código en una sola versión; HU-04, 06, 08, 10, 02 y 03 funcionando; tabla de casos de prueba; puntos y velocidad del S1 en el Excel; tablero con capturas; dailies; burndown; minutas de Review y Retro; resumen de velocidad S1 vs S2 (carpeta Métricas).
- Semana de cierre: video demo de 3-5 min, README, Release Notes, informe final de 12-15 páginas.
- Riesgos del S2: Felipe se integra recién; sprints de 1 semana; otros ramos; juntar el código; HU-04 y HU-06 atrasadas.

### Riesgos registrados
~~Felipe no confirmado como Dev 3~~ (resuelto: programador en jefe); sprints de 1 semana; pruebas de otros ramos; integración del código; tecnología no definida (ya resuelto: Python + MySQL).

---

## Código (`Sprint 1/Codigo/`)

`Sprint 1/Codigo/` es la copia original tal como llegó del Drive (evidencia; no editar). La copia de trabajo es el repo `~/inacap/inventario-pymes/` (GitHub), reorganizada el 17-10-2026 en una sola app:

```
app/         main.py, conexion.py, productos.py, stock.py, requirements.txt
app/tests/   pruebas pytest (fixture en app/conftest.py)
db/          inventario_pymes.sql
docs/        contexto-ramo.md
```
Material descartado (`pyme.py`, `Avance_inventario/`) borrado el 17-10-2026: el original de `Avance_inventario/` sigue en `~/inacap/metodologia-agil/Sprint 1/Codigo/Avance_inventario/` y `pyme.py` se recupera con `git show eda602f:_archivo/pyme.py`.

### `app/` (versión modular, la base)
| Archivo | Contenido |
|---|---|
| `conexion.py` | `obtener_conexion()`, `CONFIG` localhost/root/sin clave, BD `inventario_pymes` |
| `productos.py` | HU-01 `registrar_producto()` (valida vacíos, negativos, SKU repetido); HU-04 `listar_productos(busqueda)`; `pantalla_registrar`, `pantalla_listado`, `mostrar_tabla` |
| `stock.py` | HU-05 `entrada_stock()`; HU-06 `salida_stock()` con `UPDATE ... WHERE stock_actual >= %s` + `rowcount` (evita negativos también con concurrencia); commit/rollback atómico de stock + movimiento |
| `main.py` | Menú principal (opciones 1 a 4 y 0). Antes se llamaba `inventario para pyme.py` |

Las funciones de lógica reciben `conexion` y devuelven `(ok, mensaje)`; las de pantalla hacen el `input/print`. Mantener esa separación porque facilita probar sin terminal.

### `db/inventario_pymes.sql` (aporte de Benjamín, corregido)
El original es un dump de MySQL 8.0 sin `CREATE DATABASE`, con la collation `utf8mb4_0900_ai_ci`, que no existe en MariaDB. La versión de `db/` está corregida (16-10-2026):
- Crea la BD y usa la collation `utf8mb4_unicode_ci`.
- Agrega la columna `activo` y los CHECK; `fecha` pasa a `NOT NULL` y se agrega el índice `(producto_id, fecha)`.
- Trae 4 productos de prueba (`SKU-002` con stock 5 para HU-06; `SKU-003` y `SKU-004` para el `<=` de HU-08).
- Probado en MariaDB 11.8 (16-10-2026): 24 pruebas de esquema y 9 de la lógica de `app/` pasan. Hoy lo cubren los 27 tests pytest de `app/tests/`.
- **Hace `DROP TABLE`: reimportarlo borra los datos.**

### Esquema (`db/inventario_pymes.sql`)
```sql
productos(id PK AI, sku VARCHAR(50) UNIQUE NOT NULL, nombre VARCHAR(100) NOT NULL,
          categoria VARCHAR(100) NULL, stock_actual INT NOT NULL DEFAULT 0,
          stock_minimo INT NOT NULL DEFAULT 0, activo TINYINT(1) NOT NULL DEFAULT 1,
          CHECK (stock_actual >= 0), CHECK (stock_minimo >= 0))
movimientos(id PK AI, producto_id FK→productos.id, tipo ENUM('entrada','salida'),
            cantidad INT NOT NULL CHECK (cantidad > 0),
            fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX (producto_id, fecha))
```
La collation `unicode_ci` no distingue mayúsculas ni tildes: `SKU-001` y `sku-001` chocan como duplicado, y buscar `cafe` encuentra `Café`.

### Ejecutar
```bash
pip install mysql-connector-python
mysql -u root -p < db/inventario_pymes.sql   # desde la raíz del repo; crea la BD; borra datos si ya existe
cd app && python main.py
```

### Pendientes técnicos detectados
- ~~Unificar en una sola carpeta~~: hecho el 17-10-2026 (`app/`, `db/`). `_archivo/` borrado el 17-10-2026.
- `mostrar_tabla` marca "bajo mínimo" con `stock < minimo`, pero el CA de HU-08 pide `stock <= minimo`.
- HU-04: la historia menciona "filtro por categoría"; el CA solo pide nombre o código. Aclarar con la PO.
- HU-10: escribir el CSV con `encoding="utf-8-sig"` y `;` como separador para que Excel en español lea bien tildes y columnas.
- HU-03 (baja): la columna `activo` ya existe en la BD corregida, pero falta el código: la baja hace `UPDATE ... SET activo = 0`, y el listado, la búsqueda, el CSV y las alertas filtran `activo = 1`. Un `DELETE` falla porque `movimientos` tiene FK hacia `productos`.
- El `.sql` corregido está en el repo (`db/`): compartirlo con el equipo por Drive y avisar que reimportarlo borra los datos.
- ~~Tests + CI~~: hecho el 17-10-2026 (27 tests pytest de S1 en `app/tests/`, CI en `.github/workflows/ci.yml`; bonus +5). Falta agregar tests de cada HU de S2.
- ~~Repositorio git~~: hecho (https://github.com/felipemelo720/inventario-pymes). Falta `README.md`, que la guía exige.

---

## Estado de evidencias Sprint 2 (zip del 23-10-2026)

Entrega del 23-10 (según `Sprint 2/Entrega hoy, 23-10-2026.txt`): **Daily, Scrum Board y tablero activo**.

| Evidencia | Archivo (`Sprint 2/`) | Estado |
|---|---|---|
| Tablero + capturas | `Tablero/Tablero_Sprint2_InventarioPymes.xlsx`, 2 capturas | Al día (tabla de arriba) |
| Scrum Board | `Documentos/Scrum Board/ScrumBoard_InventarioPymes.xlsx` | Hoja "Sprint 1" al día; hoja "Sprint 2" todo en "Por hacer" y sin puntos (no cuadra con el tablero) |
| Sprint Planning | `Documentos/Sprint planning/Sprint_Planning_Inventario_PymesSprint2.xlsx` | Backlog con CA de S2; estimaciones solo en HU-01, 04, 05, 06; Sprint Backlog S2 suma 7 pts; Dev3 aún dice "Felipe Melo (por verificar)" |
| Dailies | `Documentos/Registro dailies/RegistroDailies_Sprint2.docx` | Copia del S1: dice "Sprint 1" y solo trae la Daily 1 del 16-10 |
| Review | `Documentos/Minuta Sprint Review/MinutaReview_Sprint2.docx` | Plantilla vacía; el título dice "Sprint 1" y la tabla lista las HU del S1 |
| Retro | `Documentos/Minuta Retrospectiva/MinutaRetrospectiva_Sprint2.docx` | Plantilla vacía |
| Burndown | `Metricas/Gráfico burndown/Burndown_Sprint1.xlsx` | Copia vacía del S1 (nombre y fechas del S1) |

Inconsistencias: HU-04 es de Benjamín en el plan y en el Sprint Backlog, pero de Felipe en el tablero. HU-04 vale 5 pts en el backlog y el Scrum Board, 3 en el tablero. En el Scrum Board del S1, HU-06 figura a nombre de Benjamín. Las minutas de Review y Retro del S2 siguen sin **Felipe Melo** entre los asistentes.

## Estado de evidencias Sprint 1 (al 16-10-2026; actualizado el 23-10 en lo que cambió)

| Evidencia | Archivo | Estado |
|---|---|---|
| Estimaciones (pts) | planilla Sprint Planning, columna "Estimación (pts)" | **Vacía**. Falta el Planning Poker (el plan propone 1, 2, 3, 5, 8) |
| Velocidad | hoja Capacidad del Sprint Planning S2 | 11 pts |
| Burndown | `Metricas/Gráfico burndown/Burndown_Sprint1.xlsx` | Sin puntos. Dice "Días del Sprint: 1" (15 al 16-10), pero el plan dice 1 semana: corregir |
| Dailies | `Documentos/Registro dailies/RegistroDailies_Sprint1.docx` | Daily 1 (16-10) llenada + tabla de complicaciones del S1; Daily 2 vacía |
| Review | `Documentos/Minuta Sprint Review/MinutaReview_Sprint1.docx` | Plantilla vacía |
| Retro | `Documentos/Minuta Retrospectiva/MinutaRetrospectiva_Sprint1.docx` | Plantilla vacía |
| Tablero + capturas | `Tablero/` (capturas) + `Documentos/Scrum Board/` | 2 capturas del 15-10; Scrum Board con el cierre del S1 |
| Notas de clase | `Sprint 1/Notas clase.txt` | Notas de Planning, Daily, Scrum Board y tablero activo |

Inconsistencias en las plantillas: las minutas de Review y Retro listan como asistentes solo a Antonella y Benjamín; falta **Felipe Melo**, que aparece como responsable de HU-06 en la misma minuta. En `Primera entrega/` la planilla de Sprint Planning no tiene la columna de CA (la versión de `Sprint 1/` sí), y `Product Backlog.xlsx` es una plantilla vacía (HU-INV-001 a 012).

---

## Cómo ayudar con documentos del ramo

- Redactar HU con el formato Como/quiero/para + CA Dado/Cuando/Entonces + INVEST. Separar las reglas de negocio de los CA.
- Estimar en story points de la escala Fibonacci del curso; nunca convertir puntos a horas.
- Calcular capacidad y rango con la fórmula de la presentación de Sprint Planning.
- Las minutas y el informe usan el lenguaje simple del plan del equipo (tono de estudiante, sin jerga innecesaria).
- El código sigue el estilo de `app/`: español, funciones `(ok, mensaje)`, consultas parametrizadas `%s`, commit/rollback en las escrituras.
- No editar los `.docx` ni los `.xlsx` sin pedirlo: son las evidencias que se entregan y el equipo los comparte por Drive.
