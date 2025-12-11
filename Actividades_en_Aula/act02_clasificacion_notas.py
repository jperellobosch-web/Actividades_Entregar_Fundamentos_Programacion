# Función para clasificar las notas en las diferentes posibles calificaciones.
def clasificar_nota(nota: float) -> str: #Toma una nota numérica (float) y devuelve su calificación en texto (string).

    if nota < 5.0:  # 0-4.9
        return "Suspenso"
    elif nota < 7.0:  # 5.0-6.9
        return "Aprobado"
    elif nota < 9.0:  # 7.0-8.9
        return "Notable"
    else:  # 9.0-10
        return "Sobresaliente"

def main(): # Función principal del script de notas.

    # 1. Lista de asignaturas
    asignaturas = ("Cálculo","Álgebra Lineal","Probabilidad y Estadística","Fundamentos de Programación")

    while True:  # Bucle Principal para permitir repetir la clasificación si el usuario lo desea.

        # 2. Un diccionario vacío para guardar las notas
        resultados = {}

        print("\n--- Introducción de Notas ---")
        print("Por favor, introduce tus notas (de 0 a 10).\n")

        # 3. Bucle para preguntar por cada asignatura de la lista
        for asignatura in asignaturas:
            while True:
                try:
                    nota_str = input(f"Introduce tu nota para {asignatura}: ") # Pedimos la nota para la asignatura actual
                    nota_num = float(nota_str)

                    if 0 <= nota_num <= 10: # Comprobamos que la nota esté en el rango 0-10
                        break  # Si es válida, salimos del bucle 'while'
                    else:
                        print("Error: La nota debe estar entre 0 y 10. Inténtalo de nuevo.\n")

                except ValueError:
                    print("Error: Eso no es un número. Inténtalo de nuevo (ej: 7.5).\n")

            # 4. Clasificar y guardar la nota. # Llamamos a la función que creamos arriba
            
            calificacion = clasificar_nota(nota_num)
            
            resultados[asignatura] = { # Guardamos en el diccionario vacío que habíamos creado. # Creamos una "entrada" nueva, ej: "Cálculo": {"nota": 7.5, "calificacion": "Notable"}
                "nota": nota_num,
                "calificacion": calificacion
            }

        #5. Mostrar todos los resultados al final
        print("\n" + "=" * 30)
        print("   RESUMEN DE CALIFICACIONES")
        print("=" * 30)

        for asignatura, info in resultados.items(): # Iteramos sobre el diccionario de resultados que hemos llenado. # .items() nos da la clave (asignatura) y el valor (info)

            print(f"-> {asignatura:<30} | Nota: {info['nota']:<4} | {info['calificacion']}") # Usamos un f-string para alinear la salida. # :<30  -> alinea el texto a la izquierda en un espacio de 30 caracteres

        respuesta = input("\n¿Quieres realizar otra clasificación? (s/n): ")
        if respuesta.lower().startswith('n'):
            print("\n¡Gracias! Adiós.")
            break

# --- Punto de entrada del script ---
if __name__ == "__main__":
    main()