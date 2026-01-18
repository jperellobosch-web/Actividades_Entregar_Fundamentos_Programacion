from clases.empleado import Empleado

class Gerente(Empleado):
    def __init__(self, id_emp, nombre, salario_base, departamento, empleados_a_cargo):
        """
        Constructor del Gerente.
        """
        # 1. Inicializamos la parte de Empleado (Padre)
        super().__init__(id_emp, nombre, salario_base)
        
        # 2. Guardamos lo específico del Gerente
        self.departamento = departamento
        self.empleados_a_cargo = int(empleados_a_cargo)

    def calcular_salario(self):
        """
        POLIMORFISMO: El gerente cobra un plus por responsabilidad.
        Si tiene más de 10 personas a cargo, suma un 15%.
        """
        salario = super().calcular_salario()
        if self.empleados_a_cargo > 10:
            return salario * 1.15  # 15% extra
        return salario

    def to_dict(self):
        """
        Convertimos a diccionario para el JSON.
        """
        data = super().to_dict()
        data["departamento"] = self.departamento
        data["empleados_a_cargo"] = self.empleados_a_cargo
        data["tipo"] = "Gerente" # Etiqueta para diferenciarlo
        return data

    def __str__(self):
        return f"{super().__str__()} | Dpto: {self.departamento} (Eq: {self.empleados_a_cargo})"