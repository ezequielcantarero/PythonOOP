class Libro:
    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo  # "Mi título es..."
        self.autor = autor    # "Mi autor es..."
        self.paginas = paginas
        self.pagina_actual = 1

    def leer_paginas(self, cantidad):
        self.pagina_actual += cantidad
        print(f"Leyendo {self.titulo}. Ahora estoy en la página {self.pagina_actual}.")

# Creando objetos reales
# libro_1 = Libro("Hábitos Atómicos", "James Clear")
# print(libro_1.titulo) # Salida: Hábitos Atómicos
# print(libro_1.autor)  # Salida: James Clear

#mi_libro = Libro("El Principito",  "Antoine de Saint-Exupéry", 100)
#mi_libro.leer_paginas(10)

class LibroFisico(Libro): # Hereda todo lo de Libro
    def __init__(self, titulo, autor,paginas, peso_gramos):
        super().__init__(titulo,autor, paginas) # Inicializa lo que hereda del padre
        self.peso_gramos = peso_gramos    # Añade su atributo único

    def comprobar_peso(self):
        print(f"Este libro pesa {self.peso_gramos} gramos en la mochila.")

libro_pesado = LibroFisico("La Enciclopedia", "Anonymus", 1000, 2500)
libro_pesado.leer_paginas(5)   # Puede usar el método del padre
libro_pesado.comprobar_peso()  # Y también el suyo propio

class LibroProtegido:
    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        # El doble guion bajo hace que el atributo sea privado
        self.__paginas = paginas 

    # Método Getter: nos permite "ver" el dato sin modificarlo
    def obtener_paginas(self):
        return self.__paginas

    # Método Setter: nos permite modificar el dato bajo nuestras reglas
    def actualizar_paginas(self, nuevas_paginas):
        if nuevas_paginas > 0:
            self.__paginas = nuevas_paginas
            print("Número de páginas actualizado correctamente.")
        else:
            print("Error: Un libro no puede tener páginas negativas.")

libro = LibroProtegido("Tráguese ese sapo", "Brian Tracy", 120)

# Si intentamos hacer esto, Python dará un error porque está oculto:
# print(libro.__paginas) 

# La forma correcta de interactuar es a través de los métodos:
print(f"Páginas originales: {libro.obtener_paginas()}")
libro.actualizar_paginas(135)

# Clase Padre
class MaterialLectura:
    def __init__(self, titulo):
        self.titulo = titulo

    def consumir(self):
        pass # Se definirá en las clases hijas

# Clase Hija 1
class LibroPapel(MaterialLectura):
    def consumir(self):
        print(f"Abriendo '{self.titulo}' y pasando las páginas de papel con las manos.")

# Clase Hija 2
class Audiolibro(MaterialLectura):
    def consumir(self):
        print(f"Poniendo los auriculares y dándole play a '{self.titulo}'.")

# Creamos los objetos
mi_libro = LibroPapel("Si lo crees, lo creas")
mi_audio = Audiolibro("Habla menos y actúa más")

# Polimorfismo en acción:
# Agrupamos los objetos y les damos la MISMA orden.
coleccion = [mi_libro, mi_audio]

for item in coleccion:
    item.consumir() 
    # Cada objeto "sabe" cómo debe consumirse a sí mismo.