import json
import os
from clases.desarrollador import Desarrollador
from clases.gerente import Gerente

# Nombre del archivo donde guardaremos todo
ARCHIVO_DB = "empleados.json"

def guardar_datos(lista_empleados):
    """
    Recibe una lista de OBJETOS (Desarrolladores o Gerentes).
    Los convierte a diccionarios y los guarda en el JSON.
    """
    # 1. Convertimos cada objeto a diccionario usando el método .to_dict()
    # Esto es una "List Comprehension" (una forma elegante de hacer un bucle for)
    datos_para_guardar = [emp.to_dict() for emp in lista_empleados]
    
    try:
        with open(ARCHIVO_DB, 'w', encoding='utf-8') as f:
            json.dump(datos_para_guardar, f, indent=4)
        print("Datos guardados correctamente.")
    except Exception as e:
        print(f"Error al guardar datos: {e}")

def cargar_datos():
    """
    Lee el JSON y convierte los diccionarios de vuelta a OBJETOS.
    Devuelve una lista de objetos Desarrollador o Gerente.
    """
    # Si el archivo no existe, devolvemos una lista vacía
    if not os.path.exists(ARCHIVO_DB):
        return []

    try:
        with open(ARCHIVO_DB, 'r', encoding='utf-8') as f:
            datos_json = json.load(f) # Esto es una lista de diccionarios
            
        lista_objetos = []
        
        for d in datos_json:
            # Aquí es donde decidimos qué clase crear basándonos en el "tipo"
            if d["tipo"] == "Desarrollador":
                # Creamos el objeto Desarrollador recuperando sus datos
                emp = Desarrollador(
                    d["id_emp"], d["nombre"], d["salario_base"], 
                    d["lenguaje"], d["nivel"]
                )
            elif d["tipo"] == "Gerente":
                # Creamos el objeto Gerente
                emp = Gerente(
                    d["id_emp"], d["nombre"], d["salario_base"], 
                    d["departamento"], d["empleados_a_cargo"]
                )
            else:
                continue # Si no reconocemos el tipo, lo saltamos
            
            lista_objetos.append(emp)
            
        return lista_objetos

    except (json.JSONDecodeError, Exception) as e:
        print(f"Error al cargar datos (archivo corrupto o vacío): {e}")
        return []