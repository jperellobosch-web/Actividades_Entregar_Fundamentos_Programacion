class Empleado:
    def __init__(self, id_emp, nombre, salario_base):
        """
        Constructor de la clase Padre.
        Definimos los atributos comunes a todos los empleados.
        """
        self.id_emp = id_emp
        self.nombre = nombre
        self.salario_base = float(salario_base)

    def calcular_salario(self):
        """
        Método genérico. En las clases hijas lo modificaremos (polimorfismo)
        si es necesario. Por defecto devuelve el salario base.
        """
        return self.salario_base

    def to_dict(self):
        """
        Este método convierte el Objeto en un Diccionario.
        Necesitamos esto obligatoriamente para poder guardar los datos en JSON,
        ya que JSON no entiende de 'Clases Python', solo de texto y diccionarios.
        """
        return {
            "id_emp": self.id_emp,
            "nombre": self.nombre,
            "salario_base": self.salario_base,
            "tipo": "Generico" # Nos ayudará a distinguir clases al cargar
        }

    def __str__(self):
        return f"ID: {self.id_emp} | {self.nombre} | ${self.salario_base}"