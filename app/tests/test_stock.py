"""
Pruebas de HU-05 (entrada de stock) y HU-06 (salida de stock).

Cada prueba recibe "conexion" (ver conftest.py): una BD de prueba recién
creada, sin movimientos, con estos productos (entre otros):

    SKU-002  Café molido 250g        stock 5
    SKU-004  Cuaderno universitario  stock 10
"""
from datetime import datetime

from productos import dar_de_baja_producto
from stock import entrada_stock, salida_stock


def stock_de(conexion, sku):
    """Lee el stock actual de un producto directo desde la BD."""
    cursor = conexion.cursor()
    cursor.execute("SELECT stock_actual FROM productos WHERE sku = %s", (sku,))
    fila = cursor.fetchone()
    cursor.close()
    return fila[0]


def movimientos_de(conexion, sku):
    """Lista de movimientos (tipo, cantidad, fecha) de un producto, del más antiguo al más nuevo."""
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT m.tipo, m.cantidad, m.fecha "
        "FROM movimientos m JOIN productos p ON p.id = m.producto_id "
        "WHERE p.sku = %s ORDER BY m.id",
        (sku,),
    )
    filas = cursor.fetchall()
    cursor.close()
    return filas


# ---------------------------------------------------------------
# HU-05: Entrada de stock
# CA: 10 + 5 = 15. Guarda el movimiento con fecha.
# ---------------------------------------------------------------

def test_entrada_suma_al_stock(conexion):
    # El cuaderno tiene 10; llegan 5
    ok, mensaje = entrada_stock(conexion, "SKU-004", 5)

    assert ok is True
    assert stock_de(conexion, "SKU-004") == 15


def test_entrada_guarda_el_movimiento_con_fecha(conexion):
    entrada_stock(conexion, "SKU-004", 5)

    movimientos = movimientos_de(conexion, "SKU-004")
    assert len(movimientos) == 1

    tipo, cantidad, fecha = movimientos[0]
    assert tipo == "entrada"
    assert cantidad == 5
    assert isinstance(fecha, datetime)  # tiene fecha y hora


def test_entrada_con_cantidad_cero_se_rechaza(conexion):
    ok, mensaje = entrada_stock(conexion, "SKU-004", 0)

    assert ok is False
    assert stock_de(conexion, "SKU-004") == 10    # no cambió
    assert movimientos_de(conexion, "SKU-004") == []  # no se guardó nada


def test_entrada_con_cantidad_negativa_se_rechaza(conexion):
    ok, mensaje = entrada_stock(conexion, "SKU-004", -3)

    assert ok is False
    assert stock_de(conexion, "SKU-004") == 10


def test_entrada_con_cantidad_no_numerica_se_rechaza(conexion):
    # None es lo que entrega pedir_cantidad() si se escribe algo que no es número
    ok, mensaje = entrada_stock(conexion, "SKU-004", None)

    assert ok is False
    assert stock_de(conexion, "SKU-004") == 10


def test_entrada_a_producto_que_no_existe(conexion):
    ok, mensaje = entrada_stock(conexion, "SKU-999", 5)

    assert ok is False


def test_entrada_y_salida_a_producto_dado_de_baja_se_rechazan(conexion):
    # HU-03: un producto dado de baja ya no acepta movimientos
    dar_de_baja_producto(conexion, "SKU-001", confirmado=True)

    assert entrada_stock(conexion, "SKU-001", 5)[0] is False
    assert salida_stock(conexion, "SKU-001", 5)[0] is False
    assert stock_de(conexion, "SKU-001") == 20


# ---------------------------------------------------------------
# HU-06: Salida de stock
# CA: con 5 en stock, sacar 8 avisa error y el stock queda en 5.
#     Si es válida, baja el stock y guarda el movimiento.
# ---------------------------------------------------------------

def test_salida_mayor_al_stock_se_rechaza_y_no_cambia_nada(conexion):
    # El café tiene 5; se intenta sacar 8
    ok, mensaje = salida_stock(conexion, "SKU-002", 8)

    assert ok is False
    assert stock_de(conexion, "SKU-002") == 5         # el stock queda en 5
    assert movimientos_de(conexion, "SKU-002") == []  # no se guardó movimiento


def test_salida_valida_resta_al_stock(conexion):
    ok, mensaje = salida_stock(conexion, "SKU-002", 3)

    assert ok is True
    assert stock_de(conexion, "SKU-002") == 2


def test_salida_valida_guarda_el_movimiento(conexion):
    salida_stock(conexion, "SKU-002", 3)

    movimientos = movimientos_de(conexion, "SKU-002")
    assert len(movimientos) == 1

    tipo, cantidad, fecha = movimientos[0]
    assert tipo == "salida"
    assert cantidad == 3
    assert isinstance(fecha, datetime)


def test_salida_de_todo_el_stock_deja_cero(conexion):
    # Sacar exactamente lo que hay sí está permitido
    ok, mensaje = salida_stock(conexion, "SKU-002", 5)

    assert ok is True
    assert stock_de(conexion, "SKU-002") == 0


def test_salida_con_cantidad_cero_se_rechaza(conexion):
    ok, mensaje = salida_stock(conexion, "SKU-002", 0)

    assert ok is False
    assert stock_de(conexion, "SKU-002") == 5


def test_salida_de_producto_que_no_existe(conexion):
    ok, mensaje = salida_stock(conexion, "SKU-999", 1)

    assert ok is False


def test_entrada_y_salida_seguidas(conexion):
    # 5 + 10 - 12 = 3, y quedan 2 movimientos guardados en orden
    entrada_stock(conexion, "SKU-002", 10)
    salida_stock(conexion, "SKU-002", 12)

    assert stock_de(conexion, "SKU-002") == 3

    movimientos = movimientos_de(conexion, "SKU-002")
    assert movimientos[0][0] == "entrada"
    assert movimientos[1][0] == "salida"
