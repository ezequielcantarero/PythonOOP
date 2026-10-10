class Empleado:
    def __init__(self, nombre, puesto):
        self.nombre = nombre
        self.puesto = puesto

    # 1. MÉTODO NORMAL
    def presentarse(self):
        return f"Hola, soy {self.nombre} ({self.puesto})."

    # 2. MÉTODO DE CLASE (Constructor alternativo)
    @classmethod
    def desde_texto_csv(cls, texto):
        # Recibimos "Ezequiel,Data Engineer" y lo separamos por la coma
        nombre, puesto = texto.split(",")
        
        # 'cls' es la clase Empleado. Esto crea y devuelve el objeto nuevo.
        return cls(nombre, puesto) 

    # 3. MÉTODO ESTÁTICO (Utilidad aislada)
    @staticmethod
    def es_dia_laborable(dia):
        dias_laborables = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        return dia in dias_laborables

# ==========================================
#        CÓMO SE USAN EN LA PRÁCTICA
# ==========================================

# 1. Usando el constructor normal
empleado_1 = Empleado("Anna", "Analista")
print(empleado_1.presentarse()) 
# Salida: Hola, soy Anna (Analista).

# 2. Usando el CLASSMETHOD para crear un empleado desde un formato raro
empleado_2 = Empleado.desde_texto_csv("Ezequiel,Data Engineer")
print(empleado_2.presentarse()) 
# Salida: Hola, soy Ezequiel (Data Engineer).

# 3. Usando el STATICMETHOD para una consulta general (no necesitamos un empleado)
print(Empleado.es_dia_laborable("Sábado")) 
# Salida: False