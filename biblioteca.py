from abc import ABC, abstractmethod

class MaterialBiblioteca:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        # Atributo privado: solo la clase puede modificarlo directamente
        self.__disponible = True 

    # Método para consultar el estado (Getter)
    def esta_disponible(self):
        return self.__disponible

    # Método para prestar el material (Modifica el estado de forma segura)
    def prestar(self):
        if self.__disponible:
            self.__disponible = False
            print(f"Prestado: {self.titulo}")
        else:
            print(f"No disponible: {self.titulo}")

    # Método para devolver el material
    def devolver(self):
        self.__disponible = True
        print(f"Devuelto: {self.titulo}")

    @abstractmethod
    def obtener_detalles(self):
        pass

class LibroFisico(MaterialBiblioteca):
    def __init__(self, titulo, autor, estante):
        # Llamamos al constructor de la clase padre
        super().__init__(titulo, autor) 
        self.estante = estante

    def obtener_detalles(self):
        estado = "Disponible" if self.esta_disponible() else "Prestado"
        return f"📘 [Físico] {self.titulo} por {self.autor} - {estado} (Estante {self.estante})"

class RecursoDigital(MaterialBiblioteca):
    def __init__(self, titulo, autor, enlace):
        super().__init__(titulo, autor)
        self.enlace = enlace

    def obtener_detalles(self):
        estado = "Acceso habilitado" if self.esta_disponible() else "Licencias en uso"
        return f"💻 [Digital] {self.titulo} por {self.autor} - {estado} (URL: {self.enlace})"

class Biblioteca:
    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = [] # Una lista para guardar nuestros objetos

    def agregar_material(self, material):
        self.catalogo.append(material)
        print(f"Material agregado al catálogo: {material.titulo}")

    def mostrar_inventario(self):
        print(f"\n--- Inventario de {self.nombre} ---")
        for item in self.catalogo:
            # Aquí brilla el polimorfismo: no nos importa si es físico o digital,
            # solo le pedimos que nos dé sus detalles y cada uno sabrá cómo hacerlo.
            print(item.obtener_detalles())
        print("-----------------------------------\n")

# 1. Creamos la biblioteca
mi_biblioteca = Biblioteca("Biblioteca Central")

# 2. Creamos los objetos (Instancias)
libro_1 = LibroFisico("Meditaciones", "Marco Aurelio", "Filosofía A1")
libro_2 = LibroFisico("Tráguese ese sapo", "Brian Tracy", "Productividad B4")
recurso_1 = RecursoDigital("Guía de Gramática B2", "Cambridge", "www.biblioteca.com/gramatica")

# 3. Agregamos los materiales al sistema
mi_biblioteca.agregar_material(libro_1)
mi_biblioteca.agregar_material(libro_2)
mi_biblioteca.agregar_material(recurso_1)

# 4. Mostramos el inventario inicial
mi_biblioteca.mostrar_inventario()

# 5. Interactuamos con los objetos (Encapsulamiento en acción)
libro_1.prestar()
libro_1.prestar() # Intentamos prestarlo de nuevo para forzar un error
recurso_1.prestar()

# 6. Mostramos el inventario actualizado
mi_biblioteca.mostrar_inventario()