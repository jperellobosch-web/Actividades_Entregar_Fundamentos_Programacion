import tkinter as tk
from tkinter import ttk, messagebox
from clases.gerente import Gerente

class TabGerente:
    def __init__(self, notebook, lista_empleados, callback_guardar):
        self.lista_empleados = lista_empleados
        self.callback_guardar = callback_guardar
        
        self.frame = ttk.Frame(notebook)
        
        # --- FORMULARIO ---
        self.frame_form = ttk.LabelFrame(self.frame, text="Datos del Gerente")
        self.frame_form.pack(fill="x", padx=10, pady=5)
        
        # ID, Nombre, Salario (Igual que antes)
        ttk.Label(self.frame_form, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(self.frame_form)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame_form, text="Nombre:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self.frame_form)
        self.entry_nombre.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(self.frame_form, text="Salario Base:").grid(row=0, column=4, padx=5, pady=5)
        self.entry_salario = ttk.Entry(self.frame_form)
        self.entry_salario.grid(row=0, column=5, padx=5, pady=5)
        
        # DATOS ESPECÍFICOS DE GERENTE
        # Departamento
        ttk.Label(self.frame_form, text="Departamento:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_depto = ttk.Entry(self.frame_form)
        self.entry_depto.grid(row=1, column=1, padx=5, pady=5)
        
        # Empleados a cargo (Usamos Spinbox para números)
        ttk.Label(self.frame_form, text="Personas a cargo:").grid(row=1, column=2, padx=5, pady=5)
        self.spin_cargo = ttk.Spinbox(self.frame_form, from_=0, to=1000)
        self.spin_cargo.grid(row=1, column=3, padx=5, pady=5)
        
        # --- BOTONES ---
        self.frame_botones = ttk.Frame(self.frame)
        self.frame_botones.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(self.frame_botones, text="Agregar Gerente", command=self.agregar).pack(side="left", padx=5)
        ttk.Button(self.frame_botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=5)
        ttk.Button(self.frame_botones, text="Borrar", command=self.borrar).pack(side="left", padx=5)
        ttk.Button(self.frame_botones, text="Limpiar", command=self.limpiar_form).pack(side="left", padx=5)

        # --- TREEVIEW ---
        columns = ("id", "nombre", "salario", "depto", "cargo")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("salario", text="Salario Base")
        self.tree.heading("depto", text="Departamento")
        self.tree.heading("cargo", text="Pers. a Cargo")
        
        for col in columns:
            self.tree.column(col, width=100)
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_item)

        self.refrescar_tabla()

    # --- LÓGICA (Adaptada para Gerente) ---
    
    def refrescar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for emp in self.lista_empleados:
            # FILTRO: Solo mostramos Gerentes
            if isinstance(emp, Gerente):
                self.tree.insert("", "end", values=(
                    emp.id_emp, emp.nombre, emp.salario_base, 
                    emp.departamento, emp.empleados_a_cargo
                ))

    def limpiar_form(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_salario.delete(0, tk.END)
        self.entry_depto.delete(0, tk.END)
        self.spin_cargo.delete(0, tk.END)
        self.spin_cargo.insert(0, 0)

    def agregar(self):
        try:
            # Crear objeto GERENTE
            nuevo_gerente = Gerente(
                self.entry_id.get(),
                self.entry_nombre.get(),
                float(self.entry_salario.get()),
                self.entry_depto.get(),
                int(self.spin_cargo.get())
            )
            
            self.lista_empleados.append(nuevo_gerente)
            self.callback_guardar()
            self.refrescar_tabla()
            self.limpiar_form()
            messagebox.showinfo("Éxito", "Gerente agregado")
            
        except ValueError:
            messagebox.showerror("Error", "Revisa que Salario y Personas a Cargo sean números.")

    def seleccionar_item(self, event):
        selection = self.tree.selection()
        if not selection: return
        
        valores = self.tree.item(selection[0])['values']
        self.limpiar_form()
        
        self.entry_id.insert(0, valores[0])
        self.entry_nombre.insert(0, valores[1])
        self.entry_salario.insert(0, valores[2])
        self.entry_depto.insert(0, valores[3])
        self.spin_cargo.delete(0, tk.END)
        self.spin_cargo.insert(0, valores[4])

    def borrar(self):
        selection = self.tree.selection()
        if not selection: return
        
        id_borrar = str(self.tree.item(selection[0])['values'][0])
        
        for emp in self.lista_empleados:
            if str(emp.id_emp) == id_borrar and isinstance(emp, Gerente):
                self.lista_empleados.remove(emp)
                break
        
        self.callback_guardar()
        self.refrescar_tabla()
        self.limpiar_form()

    def actualizar(self):
        self.borrar()
        self.agregar()