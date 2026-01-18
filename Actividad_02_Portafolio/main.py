import tkinter as tk
from gui.app import App

if __name__ == "__main__":
    # Crear la ventana raíz de Tkinter
    root = tk.Tk()
    
    # Iniciar la aplicación
    app = App(root)
    
    # Bucle principal de ejecución
    root.mainloop()