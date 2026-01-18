import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from clases.desarrollador import Desarrollador
from clases.gerente import Gerente

class TabInformes:
    def __init__(self, notebook, lista_empleados):
        self.lista_empleados = lista_empleados
        
        self.frame = ttk.Frame(notebook)
        
        # Título
        ttk.Label(self.frame, text="Informes y Estadísticas", font=("Arial", 16)).pack(pady=20)
        
        # Descripción
        ttk.Label(self.frame, text="Genera gráficos visuales a partir de los datos actuales.").pack(pady=5)
        
        # --- BOTONES PARA GENERAR GRÁFICOS ---
        frame_botones = ttk.Frame(self.frame)
        frame_botones.pack(pady=20)
        
        # Botón 1: Distribución de Personal
        btn_barras = ttk.Button(frame_botones, text="📊 Ver Distribución de Personal (Barras)", command=self.grafico_barras)
        btn_barras.pack(fill="x", pady=10, ipady=5)
        
        # Botón 2: Comparativa Salarial
        btn_tarta = ttk.Button(frame_botones, text="💰 Comparativa de Salarios (Tarta)", command=self.grafico_tarta)
        btn_tarta.pack(fill="x", pady=10, ipady=5)

    def grafico_barras(self):
        """Genera un gráfico de barras: Cantidad de Devs vs Gerentes"""
        if not self.lista_empleados:
            messagebox.showinfo("Información", "No hay empleados para graficar.")
            return

        # 1. Contar datos
        num_devs = sum(1 for e in self.lista_empleados if isinstance(e, Desarrollador))
        num_gerentes = sum(1 for e in self.lista_empleados if isinstance(e, Gerente))
        
        # 2. Preparar datos para Matplotlib
        categorias = ['Desarrolladores', 'Gerentes']
        valores = [num_devs, num_gerentes]
        colores = ['#4CAF50', '#FF9800'] # Verde y Naranja

        # 3. Crear gráfico
        plt.figure(figsize=(8, 5)) # Tamaño de la ventana
        plt.bar(categorias, valores, color=colores)
        plt.title('Distribución de la Plantilla')
        plt.ylabel('Número de Empleados')
        
        # Mostrar ventana
        plt.show()

    def grafico_tarta(self):
        """Genera un gráfico de tarta: % del Gasto Salarial Total por tipo"""
        if not self.lista_empleados:
            messagebox.showinfo("Información", "No hay empleados para graficar.")
            return

        # 1. Calcular gasto total por grupo
        gasto_devs = sum(e.calcular_salario() for e in self.lista_empleados if isinstance(e, Desarrollador))
        gasto_gerentes = sum(e.calcular_salario() for e in self.lista_empleados if isinstance(e, Gerente))
        
        total = gasto_devs + gasto_gerentes
        if total == 0:
            messagebox.showinfo("Información", "Los salarios son 0, no se puede graficar.")
            return

        # 2. Preparar datos
        etiquetas = ['Salarios Desarrolladores', 'Salarios Gerentes']
        valores = [gasto_devs, gasto_gerentes]
        explode = (0.1, 0)  # "Saca" un poco la primera rebanada para destacar

        # 3. Crear gráfico
        plt.figure(figsize=(7, 7))
        plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, explode=explode, shadow=True)
        plt.title('Distribución del Presupuesto Salarial')
        
        # Mostrar ventana
        plt.show()
        
    def actualizar_graficos(self):
        # Como generamos los gráficos al pulsar el botón (on-demand), 
        # no necesitamos refrescar nada aquí, pero mantenemos el método 
        # para cumplir con la llamada que hicimos en app.py
        pass