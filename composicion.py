class Procesador:
    def __init__(self, modelo, nucleos):
        self.modelo = modelo
        self.nucleos = nucleos

    def ejecutar_calculos(self):
        print(f"Procesando datos en {self.nucleos} núcleos...")

class Teclado:
    def __init__(self, idioma, iluminacion):
        self.idioma = idioma
        self.iluminacion = iluminacion

    def tipear(self, texto):
        print(f"Escribiendo: '{texto}' [Luz activa: {self.iluminacion}]")

class Laptop:
    # Pasamos los objetos ya creados al constructor
    def __init__(self, marca, procesador, teclado):
        self.marca = marca
        self.procesador = procesador  # ¡Esto es Composición!
        self.teclado = teclado        # ¡Esto también!

    # La laptop no procesa ni tipea por sí misma, 
    # DELEGA el trabajo a sus componentes.
    def iniciar_entorno_desarrollo(self):
        print(f"--- Iniciando {self.marca} ---")
        self.procesador.ejecutar_calculos()
        self.teclado.tipear("jupyter notebook")
        print("Entorno listo para codear.")

# 1. Fabricamos las piezas
mi_cpu = Procesador("Intel Core i7", 8)
# Usamos un teclado con las características que nos gustan
mi_teclado = Teclado("Español", "RGB horizontal") 

# 2. Ensamblamos la computadora usando las piezas
mi_equipo = Laptop("Lenovo", mi_cpu, mi_teclado)

# 3. La usamos
mi_equipo.iniciar_entorno_desarrollo()