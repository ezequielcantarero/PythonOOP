# Sin dataclass:
class LibroTradicional:
    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas

    def __repr__(self):
        return f"LibroTradicional(titulo='{self.titulo}', autor='{self.autor}', paginas={self.paginas})"

    def __eq__(self, otro):
        if isinstance(otro, LibroTradicional):
            return (self.titulo == otro.titulo and 
                    self.autor == otro.autor and 
                    self.paginas == otro.paginas)
        return False

# Con dataclass:
from dataclasses import dataclass

@dataclass
class Libro:
    titulo: str
    autor: str
    paginas: int

# 1. Ya tiene un __init__ automático
mi_libro = Libro("Tráguese ese sapo", "Brian Tracy", 120)
otro_libro = Libro("Tráguese ese sapo", "Brian Tracy", 120)

# 2. Ya tiene un __repr__ automático (se imprime perfecto)
print(mi_libro)
# Salida: Libro(titulo='Tráguese ese sapo', autor='Brian Tracy', paginas=120)

# 3. Ya tiene un __eq__ automático (compara sus valores, no su espacio en memoria)
print(mi_libro == otro_libro)
# Salida: True

