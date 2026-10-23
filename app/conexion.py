"""
Conexión de Python a MySQL.
Todos los demás archivos usan obtener_conexion() para hablar con la base de datos.

Requisito:  pip install mysql-connector-python
"""
# Trae la librería que sabe conversar con MySQL (se instala con pip).
import mysql.connector

# Diccionario (pares "clave": valor) con los datos para conectarse.
# Va en MAYÚSCULAS por convención: indica que es una constante que no se modifica.
CONFIG = {
    # Dirección del servidor MySQL. "localhost" = este mismo computador.
    "host": "localhost",
    # Usuario de MySQL con el que se entra.
    "user": "root",
    # Clave de ese usuario (aquí vacía).
    "password": "",
    # Nombre de la base de datos que se va a usar.
    "database": "inventario_pymes",
}

# "def" crea una función. Esta no recibe parámetros (paréntesis vacíos).
def obtener_conexion():
    # Texto entre triple comilla justo bajo el def = docstring: describe la función.
    """Devuelve una conexión abierta a la base de datos."""
    # connect(...) abre la conexión. "**CONFIG" desarma el diccionario en
    # parámetros con nombre: equivale a connect(host="localhost", user="root", ...).
    # "return" entrega esa conexión a quien llamó la función.
    return mysql.connector.connect(**CONFIG)
