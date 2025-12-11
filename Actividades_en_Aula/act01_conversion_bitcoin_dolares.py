# Actividad 1_Conversion_Bitcoin_Dolares

# 1. La equivalencia de 1 BTC a $:
# (Usamos mayúsculas para indicar que es una constante, es decir, un valor que no va a cambiar).
UN_BTC_A_USD= 103656.40

# 2. Definición de Funciones.
def USD_a_BTC(cantidad_USD): # Función para calcular cuántos BTC son x $. Usa la constante UN_BTC_A_USD para realizar el cálculo..
    return cantidad_USD / UN_BTC_A_USD

def BTC_a_USD(cantidad_BTC): # Función para calcular cuántos $ son x BTC. Usa la constante UN_BTC_A_USD para realizar el cálculo..
    return cantidad_BTC * UN_BTC_A_USD

# 3. Parte Principal del Script.
def main():

    while True:
        print("\n" + "=" * 30)
        print("CALCULADORA BTC/USD SENZILLA")
        print("=" * 30)

        while True: # Creamos un bucle para que los únicos valores aceptables sean escoger la opción de número [1] o [2].
            opcion = input("\n¿Qué conversión desea realizar? [1: USD a BTC] o [2: BTC a USD]")

            if opcion == '1' or opcion == '2':
                break  # Salimos del bucle si la opción escogida es válida. Si no, se avisará del error con el siguiente print.
            print(f"\nError: Opción '{opcion}' no es válida. Escribe solo 1 o 2.")

        if opcion == "1":
            while True: # Creamos otro bucle para asegurar que el usuario ingresa un valor válido, un float.
                try:
                    cantidad_USD = float(input("\nIngrese la cantidad de USD: "))
                    break # Si el valor es correcto, "rompemos" el bucle.
                except ValueError: # Si da un valor erróneo, le damos un aviso.
                    print("\nError: Eso no es un número. Inténtalo de nuevo (ej: 0.5)")

            resultado_USD_a_BTC = USD_a_BTC(cantidad_USD) # Llamamos a la función que habrá realizado la conversión.
            print(f"\nEso son {resultado_USD_a_BTC:.8f} BTC")
            # El .8f es para enseñar hasta 8 decimales, ya que las fracciones de criptos son muy pequeñas.

        elif opcion == "2":
            while True:
                try:
                    cantidad_BTC = float(input("\nIngrese la cantidad de BTC: "))
                    break
                except ValueError:
                    print("\nError: Eso no es un número. Inténtalo de nuevo (ej: 0.5)")

            resultado_BTC_a_USD = BTC_a_USD(cantidad_BTC)
            print(f"Eso son {resultado_BTC_a_USD:.2f} $")

        respuesta = input("\n¿Quieres realizar otra conversión? (s/n): ")
        if respuesta.lower().startswith('n'):
            break  # Rompe el "Bucle Principal"
    print("\n¡Gracias por usar la calculadora! Adiós.")

if __name__ == "__main__":
    main()