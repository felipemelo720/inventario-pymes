"""
HU-01: Registrar un producto nuevo.
HU-04: Ver el listado de productos y buscar uno.
"""
# Trae la función obtener_conexion desde el archivo conexion.py.
from conexion import obtener_conexion



# ============================================================
# LÓGICA (no usa input/print, por eso se puede probar con pytest)
# ============================================================

# Función que recibe la conexión abierta y el código a revisar.
def existe_sku(conexion, sku):
    """True si ya hay un producto con ese código (SKU)."""
    # El cursor es el objeto que envía consultas SQL y recibe los resultados.
    cursor = conexion.cursor()
    # Ejecuta la consulta. "%s" es un hueco que se rellena con el valor de la tupla
    # (sku,). La coma es obligatoria: sin ella Python no lo trata como tupla.
    # Así se evita la inyección SQL (nunca armar la consulta pegando texto).
    cursor.execute("SELECT id FROM productos WHERE sku = %s", (sku,))
    # fetchone() trae una sola fila del resultado, o None si no hubo ninguna.
    fila = cursor.fetchone()
    # Cierra el cursor para liberar recursos.
    cursor.close()
    # "is not None" = "hay algo". Devuelve True si se encontró una fila.
    return fila is not None


# Recibe la conexión y los cinco datos del producto.
def registrar_producto(conexion, sku, nombre, categoria, stock_inicial, stock_minimo):
    """
    Guarda un producto nuevo.
    Devuelve (True, mensaje) si se guardó, o (False, motivo) si no.
    """
    # "not texto" es True si el texto está vacío (""). Si falta alguno, no sigue.
    if not sku or not nombre or not categoria:
        # Devuelve dos valores a la vez (una tupla): éxito False + mensaje.
        return False, "Faltan datos: nombre, código y categoría son obligatorios."
    # None = "sin valor". pedir_entero devuelve None si el usuario no escribió un número.
    if stock_inicial is None or stock_minimo is None:
        # Corta la función y avisa qué falta.
        return False, "Faltan datos: stock inicial y stock mínimo son obligatorios."
    # Revisa que ningún stock sea negativo.
    if stock_inicial < 0 or stock_minimo < 0:
        # Corta la función con el error.
        return False, "El stock no puede ser negativo."

    # Llama a la función de arriba para ver si el código ya está usado.
    if existe_sku(conexion, sku):
        # f"...{sku}..." es un f-string: mete el valor de la variable dentro del texto.
        return False, f"Ya existe un producto con el código {sku}."

    # Crea un cursor nuevo para hacer el INSERT.
    cursor = conexion.cursor()
    # Ejecuta el INSERT. Los paréntesis permiten partir la llamada en varias líneas.
    cursor.execute(
        # Dos textos seguidos se unen solos en uno: es la misma consulta en dos líneas.
        "INSERT INTO productos (sku, nombre, categoria, stock_actual, stock_minimo) "
        # Cinco huecos %s, uno por cada valor.
        "VALUES (%s, %s, %s, %s, %s)",
        # Tupla con los valores, en el mismo orden que las columnas.
        (sku, nombre, categoria, stock_inicial, stock_minimo),
    )
    # commit() confirma el cambio. Sin esto MySQL no guarda el producto.
    conexion.commit()
    # Cierra el cursor.
    cursor.close()
    # Devuelve éxito True + mensaje de confirmación.
    return True, f"Producto '{nombre}' registrado correctamente."


# busqueda="" es un parámetro con valor por defecto: si no se pasa, vale "".
def listar_productos(conexion, busqueda=""):
    """
    Devuelve una lista de productos.
    Si 'busqueda' tiene texto, filtra por nombre o por código (SKU).
    Cada producto es una tupla: (sku, nombre, categoria, stock_actual, stock_minimo)
    """
    # Crea el cursor para la consulta.
    cursor = conexion.cursor()
    # Arma la parte base de la consulta: qué columnas traer y de qué tabla.
    consulta = "SELECT sku, nombre, categoria, stock_actual, stock_minimo FROM productos"
    # Un texto con contenido cuenta como True; uno vacío como False.
    if busqueda:
        # "+=" agrega texto al final. LIKE busca coincidencias parciales.
        consulta += " WHERE nombre LIKE %s OR sku LIKE %s"
        # "%" en LIKE = "cualquier cosa". "%caf%" encuentra "Café", "Cafetera", etc.
        patron = f"%{busqueda}%"
        # Ejecuta ordenando por nombre. Se pasa el patrón dos veces: un hueco por cada %s.
        cursor.execute(consulta + " ORDER BY nombre", (patron, patron))
    # "else" = si no hubo búsqueda.
    else:
        # Trae todos los productos ordenados por nombre (sin huecos que rellenar).
        cursor.execute(consulta + " ORDER BY nombre")
    # fetchall() trae todas las filas como una lista de tuplas.
    filas = cursor.fetchall()
    # Cierra el cursor.
    cursor.close()
    # Entrega la lista.
    return filas



# ============================================================
# PANTALLAS (hablan con el usuario: input/print)
# ============================================================

# Recibe el texto que se le muestra al usuario.
def pedir_entero(mensaje):
    """Pide un número entero; devuelve None si se deja vacío o no es número."""
    # input() muestra el mensaje y espera que el usuario escriba. Siempre devuelve texto.
    # .strip() quita espacios al inicio y al final.
    texto = input(mensaje).strip()
    # "==" compara (un solo "=" asigna). Si el usuario solo apretó Enter...
    if texto == "":
        # ...devuelve None (sin valor).
        return None
    # "try" intenta algo que puede fallar.
    try:
        # int() convierte el texto a número entero. Falla si el texto es "abc".
        return int(texto)
    # Si int() falló, Python lanza ValueError y se salta aquí en vez de cerrar el programa.
    except ValueError:
        # Texto no numérico: devuelve None.
        return None

# Recibe la lista de tuplas que devuelve listar_productos.
def mostrar_tabla(productos):
    # Una lista vacía cuenta como False, así que "not productos" = "no hay productos".
    if not productos:
        # Muestra el aviso en pantalla.
        print("No se encontraron productos.")
        # "return" sin valor: sale de la función sin hacer nada más.
        return
    # Encabezado. "\n" = salto de línea. {'CÓDIGO':<12} alinea a la izquierda en 12
    # espacios; ">7" alinea a la derecha en 7. Así las columnas quedan parejas.
    print(f"\n{'CÓDIGO':<12}{'NOMBRE':<25}{'CATEGORÍA':<18}{'STOCK':>7}{'MÍNIMO':>8}")
    # Multiplicar un texto lo repite: imprime 70 guiones.
    print("-" * 70)
    # "for" recorre la lista. Cada tupla se desarma en cinco variables a la vez.
    for sku, nombre, categoria, stock, minimo in productos:
        # Forma corta de if/else: aviso vale el texto si stock < minimo, si no vale "".
        aviso = "  <- bajo mínimo" if stock < minimo else ""
        # Imprime la fila. "categoria or 'sin categoría'" usa el texto de reemplazo
        # si la categoría viene vacía o None.
        print(f"{sku:<12}{nombre:<25}{categoria or 'sin categoría':<18}{stock:>7}{minimo:>8}{aviso}")
    # print() sin nada imprime una línea en blanco.
    print()

# Pantalla de la opción 1 del menú. No recibe parámetros.
def pantalla_registrar():
    # Título de la pantalla.
    print("\n--- Registrar producto nuevo ---")
    # Pide el código y le quita espacios sobrantes.
    sku = input("Código (SKU): ").strip()
    # Pide el nombre.
    nombre = input("Nombre: ").strip()
    # Pide la categoría.
    categoria = input("Categoría: ").strip()
    # Pide el stock inicial como número (None si no es válido).
    stock_inicial = pedir_entero("Stock inicial: ")
    # Pide el stock mínimo como número.
    stock_minimo = pedir_entero("Stock mínimo: ")

    # Abre la conexión a la base de datos.
    conexion = obtener_conexion()
    # Llama a la lógica. Como devuelve dos valores, se reciben en dos variables.
    ok, mensaje = registrar_producto(conexion, sku, nombre, categoria, stock_inicial, stock_minimo)
    # Cierra la conexión.
    conexion.close()
    # Elige el prefijo según ok y lo une con "+" al mensaje.
    print(("OK: " if ok else "ERROR: ") + mensaje)

# Pantalla de la opción 2 del menú.
def pantalla_listado():
    # Título de la pantalla.
    print("\n--- Listado de productos ---")
    # Pide el texto a buscar. Si aprieta Enter queda "" y se listan todos.
    busqueda = input("Buscar por nombre o código (Enter para ver todos): ").strip()
    # Abre la conexión.
    conexion = obtener_conexion()
    # Trae los productos (filtrados o todos).
    productos = listar_productos(conexion, busqueda)
    # Cierra la conexión.
    conexion.close()
    # Imprime la tabla.
    mostrar_tabla(productos)
