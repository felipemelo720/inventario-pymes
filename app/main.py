"""
Inventario ligero para Pymes - Sprint 1
Ejecutar con:  python main.py
"""
# Trae las pantallas de productos desde productos.py.
from productos import (
    pantalla_registrar,
    pantalla_listado,
    pantalla_editar,
    pantalla_baja,
    pantalla_alertas,
    pantalla_exportar_csv,
)
# Trae las dos pantallas de stock desde stock.py.
from stock import pantalla_entrada, pantalla_salida

# Función del menú principal.
def menu():
    # "while True" = repetir para siempre, hasta que un "break" lo corte.
    while True:
        # HU-08: al abrir el menú se avisa si algún producto está en el mínimo.
        try:
            pantalla_alertas()
        except Exception as error:
            print(f"Ocurrió un error con la base de datos: {error}")
        # Imprime el título del menú (con línea en blanco antes).
        print("\nINVENTARIO PYMES")
        # Opción 1.
        print("1. Registrar producto nuevo")
        # Opción 2.
        print("2. Ver listado / buscar producto")
        # Opción 3.
        print("3. Entrada de stock (llegó mercadería)")
        # Opción 4.
        print("4. Salida de stock (venta)")
        # Opción 5.
        print("5. Editar los datos de un producto")
        # Opción 6.
        print("6. Dar de baja producto")
        # Opción 7.
        print("7. Exportar inventario a CSV")
        # Opción para salir.
        print("0. Salir")
        # Lee la opción como texto (por eso se compara con "1" y no con 1).
        opcion = input("Elige una opción: ").strip()

        # Si una pantalla falla (por ejemplo, MySQL apagado), el error cae al except.
        try:
            # Si eligió 1...
            if opcion == "1":
                # ...abre la pantalla de registro.
                pantalla_registrar()
            # "elif" = "si no, y si...". Revisa la siguiente opción.
            elif opcion == "2":
                # Pantalla de listado/búsqueda.
                pantalla_listado()
            # Opción 3.
            elif opcion == "3":
                # Pantalla de entrada de stock.
                pantalla_entrada()
            # Opción 4.
            elif opcion == "4":
                # Pantalla de salida de stock.
                pantalla_salida()
            # Opción 5.
            elif opcion == "5":
                # Pantalla de edición.
                pantalla_editar()
            # Opción 6.
            elif opcion == "6":
                # Pantalla de baja.
                pantalla_baja()
            # Opción 7.
            elif opcion == "7":
                # Pantalla de exportación a CSV.
                pantalla_exportar_csv()
            # Opción 0.
            elif opcion == "0":
                # Despedida.
                print("Hasta luego.")
                # "break" corta el while: el programa termina.
                break
            # Cualquier otra cosa escrita.
            else:
                # Avisa y el while vuelve a mostrar el menú.
                print("Opción no válida.")
        # Atrapa cualquier error y lo guarda en la variable "error".
        except Exception as error:
            # Muestra el error sin cerrar el programa; el menú sigue.
            print(f"Ocurrió un error con la base de datos: {error}")

# __name__ vale "__main__" solo si este archivo se ejecuta directo (python main.py),
# no cuando otro archivo lo importa (por ejemplo, pytest).
if __name__ == "__main__":
    # Arranca el menú.
    menu()
