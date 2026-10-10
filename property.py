class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self._edad = edad  # El guion bajo indica que la protegemos

    # 1. El GETTER (@property): Nos permite LEER el dato
    @property
    def edad(self):
        return self._edad

    # 2. El SETTER (@atributo.setter): Intercepta cuando queremos MODIFICAR el dato
    @edad.setter
    def edad(self, nuevo_valor):
        if nuevo_valor < 0:
            print("❌ Error: La edad no puede ser un número negativo.")
        else:
            self._edad = nuevo_valor

persona = Persona("Ezequiel", 30)

# 1. Leemos la variable normalmente (sin paréntesis)
print(persona.edad)  
# Salida: 30

# 2. Modificamos la variable con un dato válido
persona.edad = 31    
print(persona.edad)  
# Salida: 31

# 3. Alguien intenta meter un dato inválido por error
persona.edad = -5    
# Salida: ❌ Error: La edad no puede ser un número negativo.
# La variable nunca se modificó, sigue siendo 31.