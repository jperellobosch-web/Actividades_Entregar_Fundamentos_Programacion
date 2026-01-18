import tkinter as tk
from tkinter import ttk
import data_manager

# Importamos las clases de las pestañas 
from gui.tab_desarrollador import TabDesarrollador
from gui.tab_gerente import TabGerente
from gui.tab_informes import TabInformes

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de RRHH - Actividad Python")
        self.root.geometry("1000x650")

        # 1. Cargar datos de la "Base de Datos" al iniciar
        self.lista_empleados = data_manager.cargar_datos()

        # 2. Crear el control de pestañas (Notebook)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # 3. Inicializar las Pestañas
        # Les pasamos la lista de empleados y la función de guardar para que puedan usarlas
        self.tab_dev = TabDesarrollador(self.notebook, self.lista_empleados, self.guardar_cambios)
        self.tab_gerente = TabGerente(self.notebook, self.lista_empleados, self.guardar_cambios)
        self.tab_informes = TabInformes(self.notebook, self.lista_empleados)

        # 4. Añadir las pestañas al Notebook (pantalla)
        self.notebook.add(self.tab_dev.frame, text="Gestión Desarrolladores")
        self.notebook.add(self.tab_gerente.frame, text="Gestión Gerentes")
        self.notebook.add(self.tab_informes.frame, text="Informes y Gráficos")

    def guardar_cambios(self):
        """
        Esta función actúa como 'Callback'.
        Las pestañas la llamarán cuando añadan o borren a alguien.
        """
        data_manager.guardar_datos(self.lista_empleados)
        print("Cambios guardados en JSON.")
        
        # Avisar a la pestaña de informes que los datos han cambiado
        self.tab_informes.actualizar_graficos()