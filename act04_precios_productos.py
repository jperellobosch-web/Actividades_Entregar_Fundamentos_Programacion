# Funciones de Ayuda
def pedir_precio(mensaje: str) -> float: #Pedimos precio del producto al usuario.
    while True:
        try:
            precio = float(input(mensaje))
            if precio >= 0:
                return precio
            else:
                print("Error: El precio no puede ser negativo.")
        except ValueError:
            print("Error: Introduce un número válido (usa punto para decimales).")


def pedir_continuar() -> bool:
    while True:
        respuesta = input("\n¿Añadir otro producto? (s/n): ").strip().lower()
        if respuesta == 's':
            return True
        elif respuesta == 'n':
            return False
        else:
            print("Error: Escribe 's' o 'n'.")


# Función Principal
def gestionar_compra():
    # Lista vacía donde guardaremos cada producto
    cesta_compra = []

    print("🛒 --- INICIANDO CAJA REGISTRADORA --- 🛒")

    # Preguntamos al Usuario
    while True:
        nombre_prod = input("Nombre del producto: ").capitalize()
        precio_prod = pedir_precio(f"Precio de '{nombre_prod}': €")

        # Guardamos el par de datos en un diccionario
        producto_actual = {
            "nombre": nombre_prod,
            "precio": precio_prod
        }

        # Añadimos ese diccionario a la lista principal
        cesta_compra.append(producto_actual)
        print(f"{nombre_prod} añadido.")

        if not pedir_continuar():
            break

    # Cálculos y Resultados

    # Comprobamos si la lista no está vacía para evitar errores
    if len(cesta_compra) > 0:

        # Truco Pro: Creamos una lista SOLO con los precios para facilitar los cálculos
        lista_precios = []
        for p in cesta_compra:
            lista_precios.append(p["precio"])

        # Ahora usamos las funciones nativas de Python sobre la lista de precios
        total = sum(lista_precios)
        precio_maximo = max(lista_precios)
        precio_minimo = min(lista_precios)

        # (Opcional) Buscamos qué productos corresponden al máx y mín
        # Esto recorre la cesta buscando quién tiene ese precio
        prod_caro = ""
        prod_barato = ""

        for p in cesta_compra:
            if p["precio"] == precio_maximo:
                prod_caro = p["nombre"]
            if p["precio"] == precio_minimo:
                prod_barato = p["nombre"]

        # --- Mostrar Informe ---
        print("\n" + "=" * 40)
        print("TICKET DE COMPRA")
        print("=" * 40)
        # Mostramos lista rápida
        for p in cesta_compra:
            print(f"- {p['nombre']:<20}: {p['precio']:.2f}€")

        print("-" * 40)
        print(f"GASTO TOTAL:      {total:.2f}€")
        print(f"PRODUCTO MÁS CARO:  {prod_caro} ({precio_maximo:.2f}€)")
        print(f"PRODUCTO MÁS BARATO:{prod_barato} ({precio_minimo:.2f}€)")
        print("=" * 40)

    else:
        print("\nNo has comprado nada. ¡Gasto 0!")


# --- 3. Ejecución ---
if __name__ == "__main__":
    gestionar_compra()