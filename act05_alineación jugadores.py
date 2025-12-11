# 1. Creamos diccionario. Creamos un diccionario vacío donde vamos a almacenar todos los jugadores con sus respectivas
# características que el usuario añada.
Jugadores = {}


# 2. Funciones de validación para asegurar que cuando al usuario se le pida la información correspondiente, nos devuelva
# los datos como se debe. Número de jugador como un entero, la altura en float...

def preguntar_numero_jugador(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Introduce un número entero válido. (ej: 23 como Jordan)")


def preguntar_altura_jugador(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Debes introducir un número válido (ej: 1.98).")


def preguntar_continuar() -> bool:
    while True:
        respuesta = input("\n¿Quieres añadir otro jugador? (s/n): ").strip().lower()
        if respuesta == 's':
            return True
        elif respuesta == 'n':
            return False
        else:
            print("Error: Escribe 's' para sí o 'n' para no.")


# 3. Función Principal. Le pedimos la información del jugador al usuario.
def preguntar_jugador():
    print("\n--- FICHA DE NUEVO JUGADOR ---")
    nombre = input("Nombre del jugador: ")
    # Usamos nuestras funciones validadas
    numero = preguntar_numero_jugador("Dorsal: ")
    altura = preguntar_altura_jugador("Altura (m) (ej: 1.98): ")
    return nombre, numero, altura


# 4. Bloque de Ejecución (Guardar en Diccionario)
if __name__ == "__main__":
    print("BIENVENIDO AL GESTOR DE JUGADORES")

    while True:
        # Pedimos los datos de un jugador
        nom, num, alt = preguntar_jugador()

        # Guardamos en el diccionario
        Jugadores[nom] = {
            "dorsal": num,
            "altura": alt
        }
        print(f"{nom} guardado.")

        # Preguntamos si quiere añadir otro jugador. Si respuesta es NO break al bucle.
        if not preguntar_continuar():
            break

    # Mostrar Resultados
    print("\n" + "=" * 40)
    print("RESUMEN FINAL DE LA PLANTILLA")
    print("=" * 40)

    # Iteramos sobre el diccionario
    for nombre, datos in Jugadores.items():
        print(f"{nombre:<20} | #{datos['dorsal']:<3} | {datos['altura']}m")

    print("=" * 40)
    print("¡Programa finalizado!")

