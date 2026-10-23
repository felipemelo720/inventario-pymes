# CLAUDE.md

App de consola en Python + MySQL: **Inventario ligero para Pymes**. Proyecto Scrum del ramo Metodología de Desarrollo Ágil (INACAP 2026-P). Felipe Melo es el **programador en jefe**. Repo privado: https://github.com/felipemelo720/inventario-pymes (sin protección de `main`: requiere GitHub Pro). El equipo también comparte el código por Google Drive.

Contexto completo del ramo (teoría, requisitos de evaluación, estado de evidencias): `docs/contexto-ramo.md`. Leerlo solo si la tarea lo necesita. Documentos originales en `~/inacap/metodologia-agil/`.

## Equipo y asignación

| Quién | Rol | Sprint 1 | Sprint 2 |
|---|---|---|---|
| Anastasia Fuentes | PO: acepta o rechaza según los CA; solo ella pasa tareas a "Terminado" | | |
| José Oporto | Scrum Master (no programa) | | |
| Benjamín Ceballos | Dev | T-01 BD + conexión, HU-04 | T-03, HU-08, HU-10 |
| Antonella Pezzopane | Dev | HU-01, HU-05 | T-03, HU-02, HU-03 |
| Felipe Melo | Dev / jefe técnico | HU-06 | HU-04, HU-06, T-02 pruebas |

T-03 = juntar el código (terminado). Tablero del Sprint 2, con estados y puntos: `docs/contexto-ramo.md`, sección Tablero. Velocidad S1 = 11 pts. El plan de la PO asigna HU-04 a Benjamín; el tablero, a Felipe.

Sprints de 1 semana: S1 desde 15-10-2026, después S2, y una semana 3 de cierre (video demo de 3-5 min, README, Release Notes).

## Backlog: la especificación

Los CA son el contrato con la PO; implementar exactamente lo que dicen. Los de S1 están acordados; los demás son propuesta.

| ID | Sprint | Historia | Criterio de aceptación |
|---|---|---|---|
| HU-01 | S1 | Registrar producto | Pide nombre, SKU, categoría, stock inicial y stock mínimo. No guarda si falta un dato o si el SKU existe |
| HU-04 | S1 | Listado + búsqueda | Muestra todos los productos con su stock. Busca por nombre o SKU. (La historia menciona filtro por categoría, el CA no: confirmar con la PO) |
| HU-05 | S1 | Entrada de stock | 10 + 5 = 15. Guarda el movimiento con fecha |
| HU-06 | S1 | Salida de stock | Con 5 en stock, sacar 8 avisa error y el stock queda en 5. Si es válida, baja y guarda el movimiento |
| HU-08 | S2 | Alerta de stock mínimo | Si `stock_actual <= stock_minimo`, aviso con el nombre del producto |
| HU-10 | S2 | Exportar inventario a CSV | Columnas código, nombre, categoría, stock, mínimo. Se abre bien en Excel, con tildes |
| HU-02 | S2 | Editar producto | El cambio se ve en el listado. Sin campos vacíos ni SKU repetido |
| HU-03 | S2 | Dar de baja producto | Pide confirmación. Si se confirma, deja de aparecer en el listado; si se cancela, no cambia nada |
| HU-09 | extra | Listado de stock bajo | Solo productos con stock ≤ mínimo, con su stock y su mínimo |
| HU-07 | extra | Historial por producto | Entradas y salidas con fecha, tipo y cantidad, la más reciente primero |
| HU-12 | extra | Login | Usuario y clave correctos dejan entrar; incorrectos muestran error |
| HU-11 | extra | CSV de movimientos por rango de fechas | Solo los movimientos dentro del rango |
| HU-13 | fuera | Roles admin/vendedor | Un vendedor no puede dar de baja productos |

**DoD**: cumple los CA, código probado, integrado al proyecto, documentación breve, aprobado por la PO.

## Código actual

Reorganizado el 17-10-2026 (respaldo del estado anterior en el scratchpad de la sesión).

```
app/         código ejecutable: main.py, conexion.py, productos.py, stock.py, requirements.txt
app/tests/   pruebas pytest (fixture en app/conftest.py)
db/          inventario_pymes.sql
docs/        contexto-ramo.md
```
Material descartado (`pyme.py`, `Avance_inventario/`) borrado el 17-10-2026: el original de `Avance_inventario/` sigue en `~/inacap/metodologia-agil/Sprint 1/Codigo/Avance_inventario/` y `pyme.py` se recupera con `git show eda602f:_archivo/pyme.py`.

### `app/`
- `conexion.py`: `obtener_conexion()` con el dict `CONFIG` (localhost, root, clave vacía).
- `productos.py`: HU-01 `registrar_producto`, HU-04 `listar_productos(busqueda)`. Pantallas `pantalla_registrar`, `pantalla_listado`, `mostrar_tabla`.
- `stock.py`: HU-05 `entrada_stock`, HU-06 `salida_stock`. Actualizan el stock e insertan el movimiento en una sola transacción. La salida usa `WHERE stock_actual >= %s` + `rowcount` para impedir stock negativo.
- `main.py`: menú principal (antes `inventario para pyme.py`); captura las excepciones de BD.

### `db/inventario_pymes.sql`
Esquema oficial, corregido el 16-10-2026 (el dump original sigue intacto en `~/inacap/metodologia-agil/Sprint 1/Codigo/Avance_inventario/`, que es evidencia y no se edita). Crea la BD (`CREATE DATABASE IF NOT EXISTS` + `USE`) y **hace `DROP TABLE`: reimportar borra los datos**. Trae 4 productos de prueba (`SKU-001` a `SKU-004`). Probado en MariaDB 11.8.

### Esquema
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
- Collation `utf8mb4_unicode_ci` (funciona en MySQL 8 y MariaDB): no distingue mayúsculas ni tildes. `SKU-001` y `sku-001` chocan como duplicado; buscar `cafe` encuentra `Café`.
- `activo = 0` = producto dado de baja (HU-03). La FK bloquea el `DELETE` si hay movimientos. El código todavía no filtra por `activo`.
- `app/productos.py` exige `categoria`, aunque en la BD es nullable.

### Ejecutar
```bash
pip install mysql-connector-python
mysql -u root -p < db/inventario_pymes.sql   # crea la BD; borra datos si ya existe
cd app && python main.py
```

### Tests
`app/conftest.py` + `app/tests/` (pytest, 27 tests de HU-01, HU-04, HU-05, HU-06). Usan la BD `inventario_pymes_test`, que se recrea desde `db/inventario_pymes.sql` antes de cada test: nunca tocan la BD real. Conexión por defecto = `CONFIG`; se puede cambiar con `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`.
```bash
pip install -r app/requirements.txt
cd app && pytest
```
En este PC, root de MariaDB solo entra por socket: correr con `DB_USER=inventario DB_PASSWORD=inventario` (usuario creado el 23-10-2026, permisos solo en `inventario_pymes%`). Si MariaDB no arranca tras reiniciar (`/run/mysqld` no existe): `sudo install -d -o mysql -g mysql /run/mysqld && sudo systemctl start mariadb`.
Los imports son por nombre de módulo (`from conexion import ...`), así que hay que ejecutar desde dentro de `app/`.

## Convenciones

- Código, nombres, mensajes y comentarios en español.
- Las funciones de lógica reciben `conexion` y devuelven `(ok: bool, mensaje: str)`. Las `pantalla_*` hacen `input()`/`print()` y abren y cierran la conexión. Así la lógica se prueba sin terminal.
- SQL siempre parametrizado con `%s`; nunca f-strings en consultas.
- Validar en Python (obligatorios, no negativos, SKU duplicado) antes de tocar la BD.
- Toda escritura que modifique stock + movimientos va con commit/rollback juntos.

## Entrega final (lo que toca al código)

```
/increment  ZIP o link al repo + video demo de 3-5 min
README.md   instrucciones de ejecución
```
Más Release Notes. El tablero y el burndown los lleva el SM, pero las tarjetas se mueven en el OneDrive de la PO: `Sprint 2/Tablero/Tablero_Sprint2_InventarioPymes.xlsx` (registrar cada cambio de estado en la hoja "Registro de movimientos"). Copia local: bajar el zip (último: `C:\Users\fmelo\Downloads\OneDrive_2026-10-23.zip`); estado de cada evidencia en `docs/contexto-ramo.md`.

## Deuda técnica / próximos pasos

1. ~~Unificar en una sola app~~ (hecho el 17-10-2026). `_archivo/` borrado el 17-10-2026.
2. Credenciales por variables de entorno (`os.getenv`), no hardcodeadas.
3. `mostrar_tabla` marca "bajo mínimo" con `<`; HU-08 exige `<=`.
4. HU-10: escribir el CSV con `encoding="utf-8-sig"` y `delimiter=";"` para Excel en español.
5. HU-03: la columna `activo` ya existe en la BD. Falta el código: la baja hace `UPDATE ... SET activo = 0`, y el listado, la búsqueda, el CSV y las alertas filtran `activo = 1`. `existe_sku` debe seguir mirando todos los productos, porque el `UNIQUE` incluye a los dados de baja.
6. ~~Tests con pytest de S1 + CI~~ (hecho el 17-10-2026). CI: `.github/workflows/ci.yml` (GitHub Actions, MySQL 8, corre `pytest` en cada push a `main` y en cada PR). Tests + CI dan **+5 de bonus**. Agregar tests de cada HU de S2.
7. Crear `README.md` (lo exige la entrega). `app/requirements.txt` y el repo git ya existen.
8. **PRs #1-#3 de Antonella (HU-02, HU-03), integrados en `main` local el 23-10-2026, sin push.** Corregido después: `listar_productos` y `buscar_por_sku` (stock) filtran `activo = 1`, CRLF pasado a LF, nuevo test de movimientos sobre producto dado de baja. `pytest`: 42 pasan (23-10-2026). Falta aprobar en GitHub el CI de los PR (fork, `action_required`).
9. **T-02 (Felipe)**: tabla de casos de prueba por historia (qué se probó, qué debía pasar, qué pasó), evidencia para el informe.
