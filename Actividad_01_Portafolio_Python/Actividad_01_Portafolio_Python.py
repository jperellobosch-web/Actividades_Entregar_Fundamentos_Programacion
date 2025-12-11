import os # Carga el módulo estándar que permite al script interactuar con el sistema operativo para realizar tareas de gestión de archivos y directorios.
import csv # Carga el módulo estándar para manejar archivos CSV.
import random # Carga el módulo estándar para generar números aleatorios y realizar selecciones aleatorias.

# --- CONSTANTES GLOBALES ---
NOMBRE_FICHERO_CSV = 'ejercicios.csv' # Almacena el nombre del archivo CSV con los ejercicios.

# Resolver el directorio de rutinas de forma portable:
# - Primero se intenta con la variable de entorno `RUTINAS_DIR` (permite personalizar por equipo).
# - Si no está definida, se usa la carpeta "rutinas" relativa al script actual.
DIRECTORIO_RUTINAS = os.environ.get('RUTINAS_DIR') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rutinas')
# Normalizar la ruta (expande ~ y la deja absoluta)
DIRECTORIO_RUTINAS = os.path.abspath(os.path.expanduser(DIRECTORIO_RUTINAS))

# --- 1. FUNCIONES DE GESTIÓN DE DATOS Y ARCHIVOS ---

def cargar_ejercicios_csv(nombre_fichero):
    """
    Lee el fichero CSV y devuelve un diccionario donde la clave es el
    grupo muscular y el valor es una lista de ejercicios.
    """
    datos_ejercicios = {}
    try:
        with open(nombre_fichero, mode='r', encoding='utf-8') as f: # Abre el archivo CSV en modo lectura (read) con codificación UTF-8.
            lector = csv.reader(f) # Crea un objeto lector CSV para iterar sobre las filas del archivo.
            for linea in lector:
                if len(linea) >= 2: # Verifica que la línea tenga al menos dos columnas (ejercicio y grupo muscular).
                    ejercicio = linea[0].strip() # Asigna el nombre del ejercicio (primera columna) y elimina espacios en blanco.
                    grupo = linea[1].strip() # Asigna el grupo muscular (segunda columna) y elimina espacios en blanco.
                    
                    if grupo not in datos_ejercicios: # Si el grupo muscular no está en el diccionario, lo inicializa con una lista vacía.
                        datos_ejercicios[grupo] = [] 
                    datos_ejercicios[grupo].append(ejercicio) # Añade el ejercicio a la lista correspondiente del grupo muscular. Esta información la saca del .cvs.
        return datos_ejercicios
    except FileNotFoundError:
        print(f"❌Error: No se encuentra el fichero {nombre_fichero}.") # Manejo de error si el archivo no existe.
        return None


def guardar_rutina_txt(nombre_rutina, contenido): # Función para guardar la rutina generada en un archivo de texto.
    """
    Guarda el contenido de la rutina generada en un archivo .txt
    dentro del directorio 'rutinas'.
    """
    # Crear directorio si no existe
    if not os.path.exists(DIRECTORIO_RUTINAS):
        os.makedirs(DIRECTORIO_RUTINAS)

    ruta_completa = os.path.join(DIRECTORIO_RUTINAS, f"{nombre_rutina}.txt") # Construye la ruta completa del archivo a guardar.
    
    try:
        with open(ruta_completa, 'w', encoding='utf-8') as f: # Abre el archivo en modo escritura con codificación UTF-8.
            f.write(contenido)
        print(f"\n✅ Rutina guardada exitosamente en: {ruta_completa}")
    except Exception as e: 
        print(f"❌ Error al guardar la rutina: {e}")


def listar_y_cargar_rutinas(): # Función para listar y cargar rutinas guardadas.
    """
    Muestra los archivos .txt en el directorio rutinas y permite al usuario
    seleccionar uno para ver su contenido.
    """
    if not os.path.exists(DIRECTORIO_RUTINAS): # Verifica si el directorio de rutinas existe.
        print("\n⚠️ No existe el directorio de rutinas. Crea una primero.")
        return

    ficheros = [f for f in os.listdir(DIRECTORIO_RUTINAS) if f.endswith('.txt')] # Lista todos los archivos .txt en el directorio de rutinas.

    if not ficheros:
        print("\n⚠️ No hay rutinas guardadas todavía.")
        return

    print("\n--- 📂 Rutinas Guardadas ---")
    for i, fichero in enumerate(ficheros, 1): # Muestra la lista de archivos con un índice comenzando en 1. Se fuerza el inicio en 1 para facilitar la selección por parte del usuario.
        print(f"{i}. {fichero}")

    eleccion = pedir_entero_rango("\nElige el número de la rutina a cargar: ", 1, len(ficheros)) # Solicita al usuario que elija un archivo por su número y recorre el rango de ficheros disponibles.
    
    archivo_elegido = ficheros[eleccion - 1] # Ajuste de índice para lista (0-based). Es decir, nosotros empezamos a contar desde 1, pero las listas en Python empiezan desde 0.
    ruta_completa = os.path.join(DIRECTORIO_RUTINAS, archivo_elegido) 

    print(f"\n--- CONTENIDO DE: {archivo_elegido} ---")
    with open(ruta_completa, 'r', encoding='utf-8') as f:
        print(f.read())
    print("-" * 40)


# --- 2. FUNCIONES DE AYUDA A LOS INPUTS ---

def pedir_entero_rango(mensaje, min_val, max_val): # Función para pedir un entero dentro deL rango específico de rutinas guardadas.
    """
    Solicita un entero al usuario y valida que esté dentro de un rango.
    """
    while True:
        try:
            dato = int(input(mensaje))
            if min_val <= dato <= max_val: # min_val y max_val cogen el valor mínimo y máximo según el número de rutinas guardadas.
                return dato
            else:
                print(f"Error: Debes introducir un valor entre {min_val} y {max_val}.")
        except ValueError:
            print("Error: Debes introducir un número entero.")


# --- 3. LÓGICA DE GENERACIÓN DE RUTINA ---

def generar_rutina(dias, tiempo, diccionario_ejercicios): # Función para generar la rutina de entrenamiento. Le pasamos los días, tiempo y el diccionario de ejercicios.
    """
    Genera el texto de la rutina distribuyendo los grupos musculares
    según los días disponibles y el tiempo.
    """
    grupos_musculares = list(diccionario_ejercicios.keys()) # Obtenemos la lista de grupos musculares del diccionario y los guardamos en una lista.
    random.shuffle(grupos_musculares) # Barajamos los grupos para que no siempre sea el mismo orden.

    ejercicios_por_dia = tiempo // 10 # Cálculo aproximado: Asumimos que un ejercicio toma 10 minutos en realizarlo.
    
    rutina_texto = f"RUTINA DE ENTRENAMIENTO ({dias} días - {tiempo} min/día)\n" 
    rutina_texto += "=" * 50 + "\n\n"

    distribucion_semanal = [[] for _ in range(dias)] # Algoritmo de distribución: Repartir los 7 grupos en N días. Si hay 3 días: [G1, G2], [G3, G4], [G5, G6, G7]. 
    # Se usa el operador _ para indicar que no nos importa el valor del elemento en sí, solo necesitamos la cantidad de elementos (días).
    
    for i, grupo in enumerate(grupos_musculares):
        dia_asignado = i % dias # Asignamos el grupo muscular al día correspondiente usando el operador módulo (%).
        distribucion_semanal[dia_asignado].append(grupo)

    # Construcción del texto día a día
    for i, grupos_dia in enumerate(distribucion_semanal, 1):
        rutina_texto += f"--- DÍA {i}: {', '.join(grupos_dia).upper()} ---\n" # Formatea el contenido de las listas [] creadas en distribucion_semanal a texto "Pecho, Espalda"...
        
        if len(grupos_dia) > 0:
            ejercicios_por_grupo = max(1, ejercicios_por_dia // len(grupos_dia)) # Repartimos los ejercicios totales del día entre los grupos que tocan.
            
            for grupo in grupos_dia:
                rutina_texto += f"\n  Bloque: {grupo}\n"
                lista_posibles = diccionario_ejercicios.get(grupo, []) # Obtiene la lista de ejercicios para el grupo muscular actual.
                
                k = min(len(lista_posibles), ejercicios_por_grupo) # Si pedimos más ejercicios de los que hay, cogemos todos los disponibles. Pedimos 4 y sólo hay 2, pues coge 2.
                seleccionados = random.sample(lista_posibles, k) # Selecciona k ejercicios únicos de la lista de posibles ejercicios para ese grupo muscular.
                
                for ej in seleccionados:
                    rutina_texto += f"    [ ] {ej} (3 series x 10-12 reps)\n"
        
        rutina_texto += "\n"

    return rutina_texto


# --- 4. FUNCIÓN DEL MENÚ PRINCIPAL ---

def menu_principal():
    """
    Gestiona el flujo principal del programa.
    """
    # 1. Obtenemos la ruta absoluta del script actual
    ruta_del_script = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Unimos esa ruta con el nombre del CSV
    ruta_completa_csv = os.path.join(ruta_del_script, NOMBRE_FICHERO_CSV)
    
    # 3. Le pasamos la ruta completa (y segura) a la función de carga
    diccionario_ejercicios = cargar_ejercicios_csv(ruta_completa_csv)
    
    if not diccionario_ejercicios: # Si no se pudo cargar el diccionario, salimos del programa. Que no se cargue el diccionario significa que no se encontró el fichero CSV.
        print("No se puede iniciar el programa sin el fichero de ejercicios.")
        return

    while True:
        print("\n" + "="*30)
        print("   🏋️  GENERADOR DE RUTINAS 🏋️")
        print("="*30)
        print("1. Crear nueva rutina")
        print("2. Cargar rutina guardada")
        print("3. Salir")
        
        opcion = pedir_entero_rango("\nSelecciona una opción: ", 1, 3) # Pedimos al usuario que seleccione una opción del menú principal, llamando a la función de pedir_entero_rango creada arriba.

        if opcion == 1:
            print("\n--- Configuración de Nueva Rutina ---")
            dias = pedir_entero_rango("¿Cuántos días a la semana vas a entrenar? [3-5]: ", 3, 5)
            tiempo = pedir_entero_rango("¿Minutos por sesión? [45-90]: ", 45, 90)

            contenido_rutina = generar_rutina(dias, tiempo, diccionario_ejercicios) # Llamamos a la función generar_rutina para crear la rutina basada en los días y tiempo proporcionados por el usuario.
            
            print("\n" + "*"*20 + " VISTA PREVIA " + "*"*20)
            print(contenido_rutina)
            
            # Preguntamos nombre para guardar
            confirmacion = input("¿Quieres guardar esta rutina? (s/n): ").strip().lower()
            if confirmacion == 's':
                nombre = input("Dime un nombre para el archivo (ej: rutina_playa): ").strip()
                if nombre:
                    guardar_rutina_txt(nombre, contenido_rutina)
                else:
                    print("\n⚠️ No has escrito un nombre. Operación cancelada.")
            else:
                print("\n❌ Rutina descartada. Volviendo al menú...")

        elif opcion == 2:
            listar_y_cargar_rutinas()

        elif opcion == 3:
            print("\n¡A darle duro al hierro! Hasta la próxima. 💪")
            break


# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    menu_principal()