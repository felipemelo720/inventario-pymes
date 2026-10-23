"""
HU-05: Sumar stock cuando llega mercadería (entrada).
HU-06: Restar stock cuando se vende algo, sin quedar en negativo (salida).
"""
# Trae "datetime" desde la librería estándar "datetime" (sirve para fecha y hora).
from datetime import datetime

# Trae la función que abre la conexión, desde conexion.py.
from conexion import obtener_conexion


# ============================================================
# LÓGICA (no usa input/print, por eso se puede probar con pytest)
# ============================================================

# Busca un producto por su código.
def buscar_por_sku(conexion, sku):
    """Devuelve (id, nombre, stock_actual) del producto, o None si no existe o está dado de baja."""
    # Crea el cursor que envía la consulta.
    cursor = conexion.cursor()
    # Consulta parametrizada: %s se rellena con (sku,). La coma hace que sea tupla.
    # "activo = 1" deja fuera los productos dados de baja (HU-03).
    cursor.execute("SELECT id, nombre, stock_actual FROM productos WHERE sku = %s AND activo = 1", (sku,))
    # Trae una fila (tupla de 3 valores) o None si no hay.
    fila = cursor.fetchone()
    # Cierra el cursor.
    cursor.close()
    # Entrega la fila (o None).
    return fila

# Recibe un cursor ya abierto (no la conexión): así el INSERT queda dentro de
# la misma transacción que el UPDATE del stock.
def guardar_movimiento(cursor, producto_id, tipo, cantidad):
    """Registra el movimiento con la fecha y hora actual."""
    # Ejecuta el INSERT en la tabla de movimientos.
    cursor.execute(
        # Cuatro columnas, cuatro huecos %s.
        "INSERT INTO movimientos (producto_id, tipo, cantidad, fecha) VALUES (%s, %s, %s, %s)",
        # Valores en el mismo orden. datetime.now() = fecha y hora de este momento.
        (producto_id, tipo, cantidad, datetime.now()),
    )

# HU-05: suma unidades al stock.
def entrada_stock(conexion, sku, cantidad):
    """
    Suma 'cantidad' al stock del producto y guarda el movimiento.
    Devuelve (True, mensaje) o (False, motivo).
    """
    # Rechaza cantidad vacía (None), cero o negativa.
    if cantidad is None or cantidad <= 0:
        # Corta la función con el error.
        return False, "La cantidad debe ser un número mayor que 0."

    # Busca el producto en la BD.
    producto = buscar_por_sku(conexion, sku)
    # Si no lo encontró...
    if producto is None:
        # ...avisa y corta.
        return False, f"No existe un producto con el código {sku}."
    # Desarma la tupla (id, nombre, stock_actual) en tres variables.
    producto_id, nombre, stock_actual = producto

    # Crea el cursor para las dos escrituras.
    cursor = conexion.cursor()
    # "try" agrupa lo que puede fallar.
    try:
        # Ejecuta el UPDATE que suma la cantidad.
        cursor.execute(
            # Suma en la misma BD (stock_actual + cantidad) solo en el producto con ese id.
            "UPDATE productos SET stock_actual = stock_actual + %s WHERE id = %s",
            # Valores para los dos huecos.
            (cantidad, producto_id),
        )
        # Inserta el movimiento de tipo "entrada" con el mismo cursor.
        guardar_movimiento(cursor, producto_id, "entrada", cantidad)
        # Confirma las dos operaciones juntas.
        conexion.commit()   # se guardan los dos cambios juntos
    # "Exception" atrapa cualquier error ocurrido dentro del try.
    except Exception:
        # Deshace todo lo que no se confirmó.
        conexion.rollback()  # si algo falla, no se guarda nada
        # "raise" vuelve a lanzar el mismo error para que main.py lo muestre.
        raise
    # "finally" se ejecuta siempre, haya error o no.
    finally:
        # Cierra el cursor en cualquier caso.
        cursor.close()

    # Calcula el stock nuevo para mostrarlo.
    nuevo = stock_actual + cantidad
    # Devuelve éxito + mensaje con el antes y el después.
    return True, f"Entrada registrada. '{nombre}': {stock_actual} -> {nuevo} unidades."

# HU-06: resta unidades sin dejar el stock negativo.
def salida_stock(conexion, sku, cantidad):
    """
    Resta 'cantidad' al stock sin dejarlo en negativo y guarda el movimiento.
    Devuelve (True, mensaje) o (False, motivo).
    """
    # Rechaza cantidad vacía, cero o negativa.
    if cantidad is None or cantidad <= 0:
        # Corta con el error.
        return False, "La cantidad debe ser un número mayor que 0."

    # Busca el producto.
    producto = buscar_por_sku(conexion, sku)
    # Si no existe...
    if producto is None:
        # ...avisa y corta.
        return False, f"No existe un producto con el código {sku}."
    # Desarma la tupla en tres variables.
    producto_id, nombre, stock_actual = producto
    # Primera revisión (en Python): ¿se quiere sacar más de lo que hay?
    if cantidad > stock_actual:
        # Los paréntesis permiten partir el texto en dos f-strings que se unen solos.
        return False, (f"No hay stock suficiente. '{nombre}' tiene {stock_actual} "
                       f"unidades y se intentó sacar {cantidad}. El stock no cambió.")

    # Crea el cursor para las escrituras.
    cursor = conexion.cursor()
    # Bloque que puede fallar.
    try:
        # Ejecuta el UPDATE que resta.
        cursor.execute(
            # Resta la cantidad...
            "UPDATE productos SET stock_actual = stock_actual - %s "
            # ...pero solo si en ese instante el stock alcanza. Segunda revisión, ahora
            # en la BD: cubre el caso de que otra persona haya vendido justo antes.
            "WHERE id = %s AND stock_actual >= %s",
            # Tres huecos: cantidad a restar, id, cantidad mínima requerida.
            (cantidad, producto_id, cantidad),
        )
        # rowcount = cuántas filas cambió el UPDATE. 0 = el WHERE no se cumplió.
        if cursor.rowcount == 0:
            # Deshace por seguridad.
            conexion.rollback()
            # Avisa que no hubo stock.
            return False, "No hay stock suficiente. El stock no cambió."
        # Inserta el movimiento de tipo "salida".
        guardar_movimiento(cursor, producto_id, "salida", cantidad)
        # Confirma UPDATE + INSERT juntos.
        conexion.commit()
    # Si algo falló...
    except Exception:
        # ...deshace todo.
        conexion.rollback()
        # Relanza el error para que lo muestre main.py.
        raise
    # Siempre, pase lo que pase...
    finally:
        # ...cierra el cursor. (También corre después del "return False" de arriba.)
        cursor.close()

    # Calcula el stock nuevo.
    nuevo = stock_actual - cantidad
    # Devuelve éxito + mensaje.
    return True, f"Salida registrada. '{nombre}': {stock_actual} -> {nuevo} unidades."


# ============================================================
# PANTALLAS (hablan con el usuario: input/print)
# ============================================================

# Pide la cantidad por teclado.
def pedir_cantidad():
    # Lee el texto y quita espacios.
    texto = input("Cantidad: ").strip()
    # Intenta convertirlo...
    try:
        # ...a número entero.
        return int(texto)
    # Si no era número (o venía vacío)...
    except ValueError:
        # ...devuelve None; entrada_stock/salida_stock lo rechazan.
        return None

# Pantalla de la opción 3 del menú.
def pantalla_entrada():
    # Título.
    print("\n--- Entrada de stock (llegó mercadería) ---")
    # Pide el código.
    sku = input("Código (SKU) del producto: ").strip()
    # Pide la cantidad.
    cantidad = pedir_cantidad()
    # Abre la conexión.
    conexion = obtener_conexion()
    # Llama a la lógica y recibe los dos valores.
    ok, mensaje = entrada_stock(conexion, sku, cantidad)
    # Cierra la conexión.
    conexion.close()
    # Muestra "OK: ..." o "ERROR: ..." según el resultado.
    print(("OK: " if ok else "ERROR: ") + mensaje)

# Pantalla de la opción 4 del menú.
def pantalla_salida():
    # Título.
    print("\n--- Salida de stock (venta) ---")
    # Pide el código.
    sku = input("Código (SKU) del producto: ").strip()
    # Pide la cantidad.
    cantidad = pedir_cantidad()
    # Abre la conexión.
    conexion = obtener_conexion()
    # Llama a la lógica.
    ok, mensaje = salida_stock(conexion, sku, cantidad)
    # Cierra la conexión.
    conexion.close()
    # Muestra el resultado.
    print(("OK: " if ok else "ERROR: ") + mensaje)
