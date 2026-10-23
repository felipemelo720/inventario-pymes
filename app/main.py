"""
Inventario ligero para Pymes - Sprint 1
Ejecutar con:  python main.py
"""
# Trae las dos pantallas de productos desde productos.py.
from productos import pantalla_registrar, pantalla_listado
# Trae las dos pantallas de stock desde stock.py.
from stock import pantalla_entrada, pantalla_salida

# Función del menú principal.
def menu():
    # "while True" = repetir para siempre, hasta que un "break" lo corte.
    while True:
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
