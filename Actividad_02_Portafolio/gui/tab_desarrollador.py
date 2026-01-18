import tkinter as tk
from tkinter import ttk, messagebox
from clases.desarrollador import Desarrollador

class TabDesarrollador:
    def __init__(self, notebook, lista_empleados, callback_guardar):
        self.lista_empleados = lista_empleados
        self.callback_guardar = callback_guardar
        
        # Crear el Frame (el contenedor de esta pestaña)
        self.frame = ttk.Frame(notebook)
        
        # --- SECCIÓN 1: FORMULARIO (Arriba) ---
        self.frame_form = ttk.LabelFrame(self.frame, text="Datos del Desarrollador")
        self.frame_form.pack(fill="x", padx=10, pady=5)
        
        # ID
        ttk.Label(self.frame_form, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(self.frame_form)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        # Nombre
        ttk.Label(self.frame_form, text="Nombre:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self.frame_form)
        self.entry_nombre.grid(row=0, column=3, padx=5, pady=5)
        
        # Salario
        ttk.Label(self.frame_form, text="Salario Base:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_salario = ttk.Entry(self.frame_form)
        self.entry_salario.grid(row=0, column=5, padx=5, pady=5)
        
        # Lenguaje (Específico de Desarrollador)
        ttk.Label(self.frame_form, text="Lenguaje:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_lenguaje = ttk.Entry(self.frame_form)
        self.entry_lenguaje.grid(row=1, column=1, padx=5, pady=5)
        
        # Nivel (Combo Box para elegir)
        ttk.Label(self.frame_form, text="Nivel:").grid(row=1, column=2, padx=5, pady=5)
        self.combo_nivel = ttk.Combobox(self.frame_form, values=["Junior", "Senior", "Mid-Level"])
        self.combo_nivel.grid(row=1, column=3, padx=5, pady=5)
        self.combo_nivel.current(0) # Seleccionar el primero por defecto
        
        # --- SECCIÓN 2: BOTONES (Medio) ---
        self.frame_botones = ttk.Frame(self.frame)
        self.frame_botones.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(self.frame_botones, text="Agregar (Alta)", command=self.agregar).pack(side="left", padx=5)
        ttk.Button(self.frame_botones, text="Actualizar Seleccionado", command=self.actualizar).pack(side="left", padx=5)
        ttk.Button(self.frame_botones, text="Borrar Seleccionado", command=self.borrar).pack(side="left", padx=5)
        ttk.Button(self.frame_botones, text="Limpiar Formulario", command=self.limpiar_form).pack(side="left", padx=5)

        # --- SECCIÓN 3: TABLA / TREEVIEW (Abajo) ---
        # Definimos las columnas
        columns = ("id", "nombre", "salario", "lenguaje", "nivel")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        # Configurar cabeceras
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("salario", text="Salario Base")
        self.tree.heading("lenguaje", text="Lenguaje")
        self.tree.heading("nivel", text="Nivel")
        
        # Configurar anchos de columna
        for col in columns:
            self.tree.column(col, width=100)
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # EVENTO: Cuando haces clic en la tabla, rellenar el formulario
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_item)

        # Cargar datos iniciales en la tabla
        self.refrescar_tabla()

    # --- LÓGICA ---
    
    def refrescar_tabla(self):
        """Borra la tabla y la vuelve a llenar con los datos de la lista"""
        # 1. Borrar todo lo que hay en el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 2. Recorrer la lista global de empleados
        for emp in self.lista_empleados:
            # Solo nos interesan los Desarrolladores (Instancia de clase)
            if isinstance(emp, Desarrollador):
                self.tree.insert("", "end", values=(
                    emp.id_emp, emp.nombre, emp.salario_base, emp.lenguaje, emp.nivel
                ))

    def limpiar_form(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_salario.delete(0, tk.END)
        self.entry_lenguaje.delete(0, tk.END)
        self.combo_nivel.current(0)

    def agregar(self):
        # Recogemos datos del formulario
        try:
            id_emp = self.entry_id.get()
            nombre = self.entry_nombre.get()
            salario = float(self.entry_salario.get())
            lenguaje = self.entry_lenguaje.get()
            nivel = self.combo_nivel.get()
            
            # Validación simple
            if not id_emp or not nombre:
                messagebox.showerror("Error", "ID y Nombre son obligatorios")
                return

            # Crear objeto NUEVO
            nuevo_dev = Desarrollador(id_emp, nombre, salario, lenguaje, nivel)
            
            # Añadir a la lista COMPARTIDA y guardar
            self.lista_empleados.append(nuevo_dev)
            self.callback_guardar() # Guardar en JSON
            
            # Actualizar vista
            self.refrescar_tabla()
            self.limpiar_form()
            messagebox.showinfo("Éxito", "Desarrollador agregado correctamente")
            
        except ValueError:
            messagebox.showerror("Error", "El salario debe ser un número")

    def seleccionar_item(self, event):
        """Carga los datos de la fila seleccionada en el formulario"""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Obtener valores de la fila
        item = self.tree.item(selection[0])
        valores = item['values']
        
        # Poner valores en los Entrys
        self.limpiar_form()
        self.entry_id.insert(0, valores[0])
        self.entry_nombre.insert(0, valores[1])
        self.entry_salario.insert(0, valores[2])
        self.entry_lenguaje.insert(0, valores[3])
        self.combo_nivel.set(valores[4])

    def borrar(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecciona un empleado de la tabla para borrar")
            return
        
        # Obtener el ID de la fila seleccionada
        item = self.tree.item(selection[0])
        id_a_borrar = str(item['values'][0]) # ID es el primer valor
        
        # Buscar en la lista y borrar
        for emp in self.lista_empleados:
            # Comparamos como string para asegurar
            if str(emp.id_emp) == id_a_borrar and isinstance(emp, Desarrollador):
                self.lista_empleados.remove(emp)
                break
        
        self.callback_guardar()
        self.refrescar_tabla()
        self.limpiar_form()
        messagebox.showinfo("Borrado", "Empleado eliminado")

    def actualizar(self):
        # Para actualizar, primero borramos el viejo y creamos uno nuevo con los datos del formulario
        self.borrar() # Borra el viejo (basado en la selección)
        self.agregar() # Crea el nuevo (basado en el formulario)