# --- 1. Nuestro Catálogo Constante de Móviles ---
# Una lista de diccionarios. Cada móvil tiene sus características.
# 'camara_top' es True si es conocido por su cámara (ej: un Pixel o un iPhone Pro)

CATALOGO_MOVILES = [
    # Rango 1 (150€ - 300€)
    {'nombre': 'Samsung Galaxy A15', 'precio': 170, 'os': 'Android', 'camara_top': False},
    {'nombre': 'Xiaomi Redmi Note 13', 'precio': 220, 'os': 'Android', 'camara_top': True},

    # Rango 2 (300€ - 450€)
    {'nombre': 'Samsung Galaxy A35', 'precio': 350, 'os': 'Android', 'camara_top': False},
    {'nombre': 'Google Pixel 7a', 'precio': 400, 'os': 'Android', 'camara_top': True},

    # Rango 3 (450€ - 600€)
    {'nombre': 'Samsung Galaxy A55', 'precio': 480, 'os': 'Android', 'camara_top': False},
    {'nombre': 'iPhone SE (3ª Gen)', 'precio': 529, 'os': 'iOS', 'camara_top': False},

    # Rango 4 (600€ - 800€)
    {'nombre': 'Google Pixel 8', 'precio': 700, 'os': 'Android', 'camara_top': True},
    {'nombre': 'iPhone 13', 'precio': 739, 'os': 'iOS', 'camara_top': False},

    # Rango 5 (800€ - 1000€)
    {'nombre': 'Samsung Galaxy S24', 'precio': 900, 'os': 'Android', 'camara_top': True},
    {'nombre': 'iPhone 15', 'precio': 959, 'os': 'iOS', 'camara_top': True},

    # Rango 6 (1000€+)
    {'nombre': 'Samsung Galaxy S24 Ultra', 'precio': 1300, 'os': 'Android', 'camara_top': True},
    {'nombre': 'iPhone 15 Pro Max', 'precio': 1469, 'os': 'iOS', 'camara_top': True}
]


# --- 2. Funciones de Ayuda para Preguntar ---

def preguntar_presupuesto() -> float:
    """
    Pregunta al usuario su presupuesto y valida que sea
    un número positivo. Devuelve el float.
    """
    while True:
        try:
            presupuesto_str = input("¿Cuál es tu presupuesto máximo? (ej: 400): €")
            presupuesto = float(presupuesto_str)

            if presupuesto >= 0:
                return presupuesto
            else:
                print("Error: El presupuesto no puede ser negativo.\n")

        except ValueError:
            print("Error: Eso no es un número. Introduce solo cifras (ej: 400).\n")


def preguntar_os() -> str:
    """
    Pregunta al usuario por su S.O. preferido y
    devuelve "Android" o "iOS".
    """
    print("\n¿Qué Sistema Operativo prefieres?")
    while True:
        opcion = input("Escribe [1] para Android o [2] para iOS: ")

        if opcion == '1':
            return "Android"
        elif opcion == '2':
            return "iOS"

        print(f"Error: Opción '{opcion}' no válida. Escribe solo 1 o 2.\n")


def preguntar_camara() -> bool:
    """
    Pregunta al usuario si la cámara es importante.
    Devuelve True (si) o False (no).
    """
    print("\n¿La calidad de la cámara es una prioridad alta para ti?")
    while True:
        opcion = input("Escribe [s] para Sí, o [n] para No: ")

        if opcion.lower().startswith('s'):
            return True
        elif opcion.lower().startswith('n'):
            return False

        print(f"Error: Opción '{opcion}' no válida. Escribe solo s o n.\n")


# --- 3. Función Principal de Lógica ---

def encontrar_movil_ideal(presupuesto: float, os_preferido: str, camara_importante: bool):
    """
    Filtra el CATÁLOGO para encontrar la mejor opción.
    Devuelve el diccionario del móvil, o None si no hay match.
    """

    # 1. Creamos una lista de candidatos que cumplen los filtros
    candidatos = []
    for movil in CATALOGO_MOVILES:

        # Filtro 1: ¿Me lo puedo permitir?
        if movil['precio'] > presupuesto:
            continue  # Demasiado caro, saltamos al siguiente

        # Filtro 2: ¿Es el S.O. que quiero?
        if movil['os'] != os_preferido:
            continue  # S.O. incorrecto, saltamos

        # Filtro 3: ¿Cumple mis requisitos de cámara?
        # Si la cámara es importante (True), el móvil DEBE ser 'camara_top' (True)
        # Si (camara_importante es True) Y (movil['camara_top'] es False) -> Lo descartamos
        if camara_importante and not movil['camara_top']:
            continue  # La cámara no es lo suficientemente buena, saltamos

        # Si el móvil ha pasado todos los filtros, es un candidato
        candidatos.append(movil)

    # 2. De todos los candidatos, ¿cuál es el mejor?
    # El "mejor" es el más caro que me puedo permitir.
    if not candidatos:
        return None  # No se encontró nada

    # Ordenamos la lista de candidatos de más caro a más barato
    candidatos.sort(key=lambda m: m['precio'], reverse=True)

    # Devolvemos el primero de la lista (el más caro/mejor que cumple)
    return candidatos[0]


# --- 4. Función Main (la que orquesta todo) ---

def main():
    """
    Función principal del script.
    """
    print("👋 ¡Bienvenido al recomendador de móviles!")
    print("Te ayudaré a encontrar tu próximo móvil ideal.")
    print("-" * 40)

    # 1. Preguntar Presupuesto y aplicar regla de 150€
    presupuesto = preguntar_presupuesto()

    if presupuesto < 150:
        print("\nLo sentimos... 😔")
        print(f"Con menos de 150€, no podemos recomendarte nada.")
        print("Cualquier móvil en ese rango será una castaña y te frustrará.")
        print("Te aconsejamos ahorrar un poco más.")
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