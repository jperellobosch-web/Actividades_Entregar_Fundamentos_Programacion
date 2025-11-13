import requests
import sys

# URL de la API de Coinbase para el precio de BTC en USD. En mayúsculas para indicar que es una constante.
API_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"

def get_btc_price() -> float | None:
    """
    Obtiene el precio actual de 1 Bitcoin en USD desde la API de Coinbase.
    Retorna el precio como un float, o None si hay un error.
    """
    print("El precio actual de Bitcoin...")
    try:
        # 1. Hacer la petición GET a la API
        response = requests.get(API_URL)

        # 2. Comprobar si la petición fue exitosa (código 200)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200

        # 3. Convertir la respuesta de JSON a un diccionario de Python
        data = response.json()

        # 4. Extraer el precio (que viene como string) y convertirlo a float
        precio_str = data['data']['amount']
        return float(precio_str)

    except requests.exceptions.ConnectionError:
        print("\nError: No se pudo conectar a la API. Revisa tu conexión a internet.", file=sys.stderr)
        return None
    except requests.exceptions.HTTPError as e:
        print(f"\nError HTTP: {e}", file=sys.stderr)
        return None
    except requests.exceptions.JSONDecodeError:
        print("\nError: La respuesta de la API no es un JSON válido.", file=sys.stderr)
        return None
    except KeyError:
        print("\nError: El formato de la respuesta de la API ha cambiado.", file=sys.stderr)
        return None

def main():
    """
    Función principal del programa.
    """

    # 1. Obtener el precio actual de BTC
    precio_actual_btc = get_btc_price()

    # Si get_btc_price devolvió None, hubo un error. Terminamos el programa.
    if precio_actual_btc is None:
        print("\nNo se pudo obtener el precio. Saliendo del programa.")
        return  # Salir de la función main

    def USD_to_BTC(cantidad_USD):
        return cantidad_USD / precio_actual_btc
    # Función para calcular cuántos BTC son x $. Usa la constante ONE_BTC_TO_USD para realizar el cálculo..

    def BTC_to_USD(cantidad_BTC):
        return cantidad_BTC * precio_actual_btc
    # Función para calcular cuántos $ son x BTC. Usa la constante ONE_BTC_TO_USD para realizar el cálculo..

    print(f"\nEl precio actual de 1 BTC es: {precio_actual_btc:.2f} USD")
    # Imprimir el precio actual de 1 BTC.

    while True:
        print("\n" + "=" * 30)
        print("CALCULADORA BTC/USD SENZILLA")
        print("=" * 30)

        while True:  # Creamos un bucle para que los únicos valores aceptales sean escoger la opción de número [1] o [2].
            opcion = input("\n¿Qué conversión desea realizar? [1: USD a BTC] o [2: BTC a USD] ")

            if opcion == '1' or opcion == '2':
                break  # Salimos del bucle si la opción escogida es válida. Si no, se avisará del error con el siguiente print.
            print(f"\nError: Opción '{opcion}' no es válida. Escribe solo 1 o 2.")

        if opcion == "1":
            while True:  # Creamos otro bucle para asegurar que el usuario ingresa un valor válido, un float.
                try:
                    cantidad_USD = float(input("\nIngrese la cantidad de USD: "))
                    break  # Si el valor es correcto, "rompemos" el bucle.
                except ValueError:  # Si da un valor erróneo, le damos un aviso.
                     print("\nError: Eso no es un número. Inténtalo de nuevo (ej: 0.5)\n")

            resultado_USD_to_BTC = USD_to_BTC(cantidad_USD)  # Llamamos a la función que habrá realizado la conversión.
            print(f"\nEso son {resultado_USD_to_BTC:.8f} BTC")
            # El .8f es para enseñar hasta 8 decimales, ya que las fracciones de criptos son muy pequeñas

        elif opcion == "2":
            while True:
                try:
                    cantidad_BTC = float(input("\nIngrese la cantidad de BTC: "))
                    break
                except ValueError:
                    print("\nError: Eso no es un número. Inténtalo de nuevo (ej: 0.5)\n")

            resultado_BTC_to_USD = BTC_to_USD(cantidad_BTC)
            print(f"\nEso son {resultado_BTC_to_USD:.2f} $")

        respuesta = input("\n¿Quieres realizar otra conversión? (s/n): ")
        if respuesta.lower().startswith('n'):
            break  # Rompe el "Bucle Principal"
    print("\n¡Gracias por usar la calculadora! Adiós. 👋")

if __name__ == "__main__":
    main()