from clases.empleado import Empleado

class Desarrollador(Empleado):
    def __init__(self, id_emp, nombre, salario_base, lenguaje, nivel):
        """
        Constructor del Desarrollador.
        Usamos super() para aprovechar el constructor del Padre.
        """
        # 1. Llamamos al constructor del Padre (Empleado) para que guarde lo básico
        super().__init__(id_emp, nombre, salario_base)
        
        # 2. Guardamos lo específico del Desarrollador
        self.lenguaje = lenguaje
        self.nivel = nivel  # Ej: "Junior", "Senior"

    def calcular_salario(self):
        """
        POLIMORFISMO: Sobrescribimos el método del padre.
        Si es Senior, le damos un bonus del 20%.
        """
        salario = super().calcular_salario()
        if self.nivel.lower() == "senior":
            return salario * 1.20  # 20% extra
        return salario

    def to_dict(self):
        """
        Extendemos el diccionario para incluir lenguaje y nivel.
        """
        # Obtenemos el diccionario básico del padre
        data = super().to_dict()
        
        # Añadimos los datos propios
        data["lenguaje"] = self.lenguaje
        data["nivel"] = self.nivel
        data["tipo"] = "Desarrollador" # Importante para distinguir
        return data

    def __str__(self):
        return f"{super().__str__()} | Dev: {self.lenguaje} ({self.nivel})"