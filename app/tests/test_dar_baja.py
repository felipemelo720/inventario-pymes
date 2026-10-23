"""Pruebas de HU-02 (editar producto) y HU-03 (dar de baja producto).
Cada prueba recibe "conexion" (ver conftest.py): una BD de prueba recién
creada con estos 4 productos:
-SKU-001  Arroz grado 1 1kg       Abarrotes  stock 20  mínimo 5
-SKU-002  Café molido 250g        Abarrotes  stock 5   mínimo 3
-SKU-003  Detergente líquido 3L   Limpieza   stock 2   mínimo 4
-SKU-004  Cuaderno universitario  Librería   stock 10  mínimo 10"""

from productos import (
    editar_producto,
    dar_de_baja_producto,
    listar_productos,
    registrar_producto,
)
 
 
def producto_en_listado(conexion, sku):
    """Devuelve la fila del producto en el listado, o None si no aparece."""
    for fila in listar_productos(conexion):
        if fila[0] == sku:
            return fila
    return None
 
# HU-02: Editar producto
# CA: el cambio se ve en el listado. Sin campos vacíos ni SKU repetido.
 
def test_editar_producto_el_cambio_se_ve_en_el_listado(conexion):
    ok, mensaje = editar_producto(conexion, "SKU-001", "SKU-001", "Arroz premium 1kg", "Abarrotes", 8)
 
    assert ok is True
    # El stock actual (20) no cambia al editar
    assert producto_en_listado(conexion, "SKU-001") == ("SKU-001", "Arroz premium 1kg", "Abarrotes", 20, 8)
 
 
def test_editar_cambiando_el_sku(conexion):
    ok, mensaje = editar_producto(conexion, "SKU-001", "SKU-101", "Arroz grado 1 1kg", "Abarrotes", 5)
 
    assert ok is True
    assert producto_en_listado(conexion, "SKU-001") is None
    assert producto_en_listado(conexion, "SKU-101") is not None
 
 
def test_no_edita_si_el_sku_ya_es_de_otro_producto(conexion):
    ok, mensaje = editar_producto(conexion, "SKU-001", "SKU-002", "Arroz grado 1 1kg", "Abarrotes", 5)
 
    assert ok is False
    # Nada cambió: los dos productos siguen como estaban
    assert producto_en_listado(conexion, "SKU-001") == ("SKU-001", "Arroz grado 1 1kg", "Abarrotes", 20, 5)
    assert producto_en_listado(conexion, "SKU-002")[1] == "Café molido 250g"
 
 
def test_no_edita_si_falta_el_nombre(conexion):
    ok, mensaje = editar_producto(conexion, "SKU-001", "SKU-001", "", "Abarrotes", 5)
 
    assert ok is False
    assert producto_en_listado(conexion, "SKU-001")[1] == "Arroz grado 1 1kg"
 
 
def test_no_edita_si_falta_el_sku(conexion):
    ok, mensaje = editar_producto(conexion, "SKU-001", "", "Arroz grado 1 1kg", "Abarrotes", 5)
 
    assert ok is False
    assert producto_en_listado(conexion, "SKU-001") is not None
 
 
def test_no_edita_si_falta_la_categoria(conexion):
    ok, mensaje = editar_producto(conexion, "SKU-001", "SKU-001", "Arroz grado 1 1kg", "", 5)
 
    assert ok is False
    assert producto_en_listado(conexion, "SKU-001")[2] == "Abarrotes"
 
 
def test_no_edita_si_falta_el_stock_minimo(conexion):
    ok, mensaje = editar_producto(conexion, "SKU-001", "SKU-001", "Arroz grado 1 1kg", "Abarrotes", None)
 
    assert ok is False
    assert producto_en_listado(conexion, "SKU-001")[4] == 5
 
 
def test_no_edita_con_stock_minimo_negativo(conexion):
    ok, mensaje = editar_producto(conexion, "SKU-001", "SKU-001", "Arroz grado 1 1kg", "Abarrotes", -1)
 
    assert ok is False
    assert producto_en_listado(conexion, "SKU-001")[4] == 5
 
 
def test_no_edita_un_producto_que_no_existe(conexion):
    ok, mensaje = editar_producto(conexion, "SKU-999", "SKU-999", "Algo", "Abarrotes", 1)
 
    assert ok is False
 
 
# HU-03: Dar de baja producto
# CA: pide confirmación. Si se confirma, deja de aparecer en el listado;
#     si se cancela, no cambia nada.
 
def test_baja_confirmada_deja_de_aparecer_en_el_listado(conexion):
    ok, mensaje = dar_de_baja_producto(conexion, "SKU-003", confirmado=True)
 
    assert ok is True
    assert producto_en_listado(conexion, "SKU-003") is None
    assert len(listar_productos(conexion)) == 3
 
 
def test_baja_cancelada_no_cambia_nada(conexion):
    ok, mensaje = dar_de_baja_producto(conexion, "SKU-003", confirmado=False)
 
    assert ok is False
    assert producto_en_listado(conexion, "SKU-003") is not None
    assert len(listar_productos(conexion)) == 4
 
 
def test_producto_dado_de_baja_no_aparece_en_la_busqueda(conexion):
    dar_de_baja_producto(conexion, "SKU-003", confirmado=True)
 
    assert listar_productos(conexion, "Detergente") == []
 
 
def test_no_da_de_baja_un_producto_que_no_existe(conexion):
    ok, mensaje = dar_de_baja_producto(conexion, "SKU-999", confirmado=True)
 
    assert ok is False
    assert len(listar_productos(conexion)) == 4
 
 
def test_no_se_puede_registrar_un_sku_de_un_producto_dado_de_baja(conexion):
    # El SKU es UNIQUE en la BD, aunque el producto esté dado de baja
    dar_de_baja_producto(conexion, "SKU-003", confirmado=True)
 
    ok, mensaje = registrar_producto(conexion, "SKU-003", "Otro producto", "Limpieza", 1, 1)
 
    assert ok is False
