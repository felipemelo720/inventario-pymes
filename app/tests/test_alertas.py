"""
Pruebas de HU-08 (alerta de stock mínimo).
CA: si stock_actual <= stock_minimo, aviso con el nombre del producto.

Cada prueba recibe "conexion" (ver conftest.py): una BD de prueba recién
creada con estos 4 productos:
-SKU-001  Arroz grado 1 1kg       Abarrotes  stock 20  mínimo 5
-SKU-002  Café molido 250g        Abarrotes  stock 5   mínimo 3
-SKU-003  Detergente líquido 3L   Limpieza   stock 2   mínimo 4
-SKU-004  Cuaderno universitario  Librería   stock 10  mínimo 10
"""
from productos import (
    dar_de_baja_producto,
    mostrar_alertas,
    productos_bajo_stock,
)
from stock import salida_stock


def skus_en_alerta(conexion):
    """Lista de códigos (SKU) que aparecen en la alerta."""
    return [fila[0] for fila in productos_bajo_stock(conexion)]


# ---------------------------------------------------------------
# HU-08: Alerta de stock mínimo
# ---------------------------------------------------------------

def test_avisa_stock_por_debajo_del_minimo(conexion):
    # SKU-003 tiene 2 y el mínimo es 4
    filas = productos_bajo_stock(conexion)

    assert ("SKU-003", "Detergente líquido 3L", 2, 4) in filas


def test_avisa_stock_igual_al_minimo(conexion):
    # SKU-004 tiene 10 y el mínimo es 10: el CA usa <=
    assert "SKU-004" in skus_en_alerta(conexion)


def test_no_avisa_stock_sobre_el_minimo(conexion):
    # SKU-001 (20/5) y SKU-002 (5/3) tienen stock suficiente
    skus = skus_en_alerta(conexion)

    assert "SKU-001" not in skus
    assert "SKU-002" not in skus


def test_avisa_cuando_una_salida_deja_el_stock_en_el_minimo(conexion):
    # SKU-002 tiene 5 y el mínimo 3; sacando 2 queda justo en el mínimo
    assert "SKU-002" not in skus_en_alerta(conexion)

    ok, _ = salida_stock(conexion, "SKU-002", 2)

    assert ok is True
    assert "SKU-002" in skus_en_alerta(conexion)


def test_no_avisa_productos_dados_de_baja(conexion):
    # SKU-003 está bajo el mínimo, pero se da de baja (HU-03)
    dar_de_baja_producto(conexion, "SKU-003", True)

    assert "SKU-003" not in skus_en_alerta(conexion)


def test_mostrar_alertas_incluye_el_nombre(conexion, capsys):
    mostrar_alertas(productos_bajo_stock(conexion))

    salida = capsys.readouterr().out
    assert "Detergente líquido 3L" in salida
    assert "Cuaderno universitario" in salida


def test_mostrar_alertas_no_imprime_si_no_hay_stock_bajo(capsys):
    mostrar_alertas([])

    assert capsys.readouterr().out == ""
