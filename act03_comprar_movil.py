# Catálogo Constante de Móviles. Una lista de diccionarios. Cada móvil tiene sus características.

CATALOGO_MOVILES = [
    # Rango 1 (150€ - 300€)
    {'nombre': 'Samsung Galaxy A36', 'precio': 255, 'os': 'Android', 'camara_top': False},
    {'nombre': 'POCO X7 Pro', 'precio': 299, 'os': 'Android', 'camara_top': True},

    # Rango 2 (300€ - 450€)
    {'nombre': 'Samsung Galaxy A56', 'precio': 359, 'os': 'Android', 'camara_top': False},
    {'nombre': 'realme 14 Pro+', 'precio': 399, 'os': 'Android', 'camara_top': True},

    # Rango 3 (450€ - 600€)
    {'nombre': 'iPhone 16e', 'precio': 529, 'os': 'iOS', 'camara_top': False},
    {'nombre': 'Google Pixel 9a', 'precio': 549, 'os': 'Android', 'camara_top': True},

    # Rango 4 (600€ - 800€)
    {'nombre': 'iPhone 15', 'precio': 759, 'os': 'iOS', 'camara_top': False},
    {'nombre': 'Google Pixel 9', 'precio': 799, 'os': 'Android', 'camara_top': True},

    # Rango 5 (800€ - 1000€)
    {'nombre': 'iPhone 16', 'precio': 859, 'os': 'iOS', 'camara_top': True},
    {'nombre': 'Samsung Galaxy S25', 'precio': 959, 'os': 'Android', 'camara_top': True},

    # Rango 6 (1000€+)
    {'nombre': 'Samsung Galaxy S25 Ultra', 'precio': 1459, 'os': 'Android', 'camara_top': True},
    {'nombre': 'iPhone 17 Pro Max', 'precio': 1469, 'os': 'iOS', 'camara_top': True}
]

# 2. Funciones

# En esta función pedimos el presupuesto al usuario.
def preguntar_presupuesto() -> float: # Dejamos claro que la respuesta del input tiene que ser un valor flotante.

    while True:
        try:
            presupuesto_str = input("¿Cuál es tu presupuesto máximo?: €")
            presupuesto = float(presupuesto_str) # Aseguramos que el valor de entrada del input sea un núm., no un string.

            if presupuesto >= 0:
                return presupuesto
            else:
                print("Error: El presupuesto no puede ser negativo.\n")

        except ValueError:
            print("Error: Introduce solo cifras.\n")

# Pedimos el sistema operativo al usuario.
def preguntar_os() -> str: # Dejamos claro que la respuesta del input tiene que ser un valor integer.

    print("\n¿Qué Sistema Operativo prefieres?")
    while True:
        opcion = input("Escribe [1] para Android o [2] para iOS: ")

        if opcion == '1':
            return "Android"
        elif opcion == '2':
            return "iOS"

        print(f"Error: Opción '{opcion}' no válida. Escribe solo 1 o 2.\n")

# Pedimos la importancia de la cámara al usuario.
def preguntar_camara() -> bool: # Dejamos claro que la respuesta del input tiene que ser un valor bool.

    print("\n¿La calidad de la cámara es importante para ti?")
    while True:
        opcion = input("Escribe [s] para Sí, o [n] para No: ")

        if opcion.lower() == 's':
            return True
        elif opcion.lower() =='n':
            return False

        print(f"Error: Opción '{opcion}' no válida. Escribe solo s o n.\n")

# 3. Función Principal de la Lógica

def encontrar_movil_ideal(presupuesto: float, os_preferido: str, camara_importante: bool):

    # 3.1 Creamos una lista de los modelos que cumplen los filtros
    candidatos = []
    for movil in CATALOGO_MOVILES:

        # Filtro 1: ¿Entra en el presupuesto?
        if movil['precio'] > presupuesto:
            continue  # Demasiado caro, saltamos al siguiente

        # Filtro 2: ¿Es el S.O. elegido?
        if movil['os'] != os_preferido:
            continue  # S.O. incorrecto, saltamos

        # Filtro 3: ¿Cumple los requisitos de cámara?
        # Si la cámara es importante (True), el móvil DEBE ser 'camara_top' (True)
        # Si "camara_importante es True" y (movil['camara_top'] es False) lo descartamos
        if camara_importante and not movil['camara_top']:
            continue  # La cámara no es lo suficientemente buena, saltamos

        # Si el móvil ha pasado todos los filtros, es un candidato
        candidatos.append(movil)

    # 3.2 De todos los candidatos, ¿cuál es el mejor?
    # El "mejor" es el más caro que entra en el presupuesto.
    if not candidatos:
        return None  # No se encontró nada

    # Ordenamos la lista de candidatos de más caro a más barato
    candidatos.sort(key=lambda m: m['precio'], reverse=True)

    # Devolvemos el primero de la lista (el más caro/mejor que cumple)
    return candidatos[0]


# 4. Función Main

def main():
    print("👋 ¡Bienvenido al recomendador de móviles!")
    print("Te ayudaré a encontrar tu próximo móvil ideal.")
    print("-" * 40)

    # 1. Preguntar Presupuesto y aplicar regla de 150€
    presupuesto = preguntar_presupuesto()

    if presupuesto < 150:
        print("""
        ¡Menos de 150€!😱
        Con menos de 150€, no podemos recomendarte nada.
        Cualquier móvil en ese rango será una castaña.
        Ahorra un poco más pobre.😈""")
        return  # Termina el programa

    # 2. Preguntar resto de preferencias
    os_pref = preguntar_os()
    cam_imp = preguntar_camara()

    # 3. Buscar el móvil
    print("\nBuscando la mejor opción para ti...")
    movil_recomendado = encontrar_movil_ideal(presupuesto, os_pref, cam_imp)

    # 4. Dar el resultado
    print("-" * 40)
    if movil_recomendado:
        print("🎉 ¡Tenemos un ganador!")
        print(f"Según tus preferencias, tu móvil ideal es el:")
        print(f"   >>> {movil_recomendado['nombre']} <<<")
        print(f"Su precio es de {movil_recomendado['precio']}€, que encaja en tu presupuesto de {presupuesto}€.")

        if cam_imp:
            print("Además, es un modelo conocido por su ¡excelente cámara! 📸")

    else:
        print("😔 Vaya... no hemos encontrado un móvil ideal.")
        print("Con esos filtros (S.O., cámara y presupuesto) no hay nada en nuestro catálogo.")
        print("Intenta ser un poco más flexible (ej: con la cámara o el presupuesto).")


# --- 5. Punto de entrada ---
if __name__ == "__main__":
    main()