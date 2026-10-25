"""
Pruebas de HU-10 (exportar inventario a CSV).
CA: columnas código, nombre, categoría, stock, mínimo.
    Se abre bien en Excel, con tildes.

Cada prueba recibe "conexion" (ver conftest.py): una BD de prueba recién
creada con estos 4 productos:
-SKU-001  Arroz grado 1 1kg       Abarrotes  stock 20  mínimo 5
-SKU-002  Café molido 250g        Abarrotes  stock 5   mínimo 3
-SKU-003  Detergente líquido 3L   Limpieza   stock 2   mínimo 4
-SKU-004  Cuaderno universitario  Librería   stock 10  mínimo 10
"""
import csv

from productos import dar_de_baja_producto, exportar_inventario_csv

ENCABEZADO = ["Código", "Nombre", "Categoría", "Stock", "Mínimo"]


def leer_csv(ruta):
    """Lee el CSV igual que Excel en español: tildes y separador ";"."""
    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        return list(csv.reader(archivo, delimiter=";"))


# ---------------------------------------------------------------
# HU-10: Exportar inventario a CSV
# ---------------------------------------------------------------

def test_exporta_el_archivo_y_devuelve_ok(conexion, tmp_path):
    ruta = tmp_path / "inventario.csv"

    ok, mensaje = exportar_inventario_csv(conexion, ruta)

    assert ok is True
    assert ruta.exists()
    assert "4 productos" in mensaje


def test_encabezado_y_columnas_del_ca(conexion, tmp_path):
    ruta = tmp_path / "inventario.csv"
    exportar_inventario_csv(conexion, ruta)

    filas = leer_csv(ruta)
    assert filas[0] == ENCABEZADO
    assert len(filas) == 5  # encabezado + los 4 productos
    for fila in filas[1:]:
        assert len(fila) == 5


def test_exporta_los_datos_de_cada_producto(conexion, tmp_path):
    ruta = tmp_path / "inventario.csv"
    exportar_inventario_csv(conexion, ruta)

    filas = leer_csv(ruta)
    assert ["SKU-002", "Café molido 250g", "Abarrotes", "5", "3"] in filas


def test_usa_utf8_sig_para_que_excel_lea_las_tildes(conexion, tmp_path):
    ruta = tmp_path / "inventario.csv"
    exportar_inventario_csv(conexion, ruta)

    with open(ruta, "rb") as archivo:
        assert archivo.read(3) == b"\xef\xbb\xbf"


def test_no_exporta_productos_dados_de_baja(conexion, tmp_path):
    dar_de_baja_producto(conexion, "SKU-001", True)
    ruta = tmp_path / "inventario.csv"
    exportar_inventario_csv(conexion, ruta)

    skus = [fila[0] for fila in leer_csv(ruta)[1:]]
    assert "SKU-001" not in skus
    assert len(skus) == 3


def test_ruta_invalida_devuelve_error(conexion, tmp_path):
    ruta = tmp_path / "no_existe" / "inventario.csv"

    ok, mensaje = exportar_inventario_csv(conexion, ruta)

    assert ok is False
    assert "No se pudo escribir" in mensaje
