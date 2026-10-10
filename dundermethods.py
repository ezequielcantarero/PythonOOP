class LoteDatos:
    def __init__(self, origen, registros: list):
        self.origen = origen
        self.registros = registros

    # Magia 1: Interceptamos el print()
    def __str__(self):
        return f"📦 [Lote de {self.origen}] -> Contiene {len(self.registros)} registros limpios."

    # Magia 2: Interceptamos el símbolo '+'
    def __add__(self, otro_lote):
        # Medida de seguridad: verificamos que estemos sumando peras con peras
        if not isinstance(otro_lote, LoteDatos):
            raise TypeError("Solo puedes sumar otro objeto de tipo LoteDatos")
        
        # Combinamos los nombres y las listas
        nuevo_origen = f"{self.origen} + {otro_lote.origen}"
        nuevos_registros = self.registros + otro_lote.registros
        
        # Devolvemos un NUEVO objeto con la fusión
        return LoteDatos(nuevo_origen, nuevos_registros)

# ==========================================
#        PROBANDO LA MAGIA
# ==========================================

# 1. Creamos dos lotes distintos
lote_postgres = LoteDatos("PostgreSQL", [{"id": 1, "user": "ezequiel"}])
lote_mongo = LoteDatos("MongoDB", [{"id": 2, "user": "anna"}, {"id": 3, "user": "lucas"}])

# Se invoca automáticamente a __str__
print(lote_postgres) 
# Salida: 📦 [Lote de PostgreSQL] -> Contiene 1 registros limpios.

# Se invoca automáticamente a __add__
lote_maestro = lote_postgres + lote_mongo 

# Vemos el resultado de la fusión
print(lote_maestro)
# Salida: 📦 [Lote de PostgreSQL + MongoDB] -> Contiene 3 registros limpios.



class GestorRegistros:
    def __init__(self, lote_id, registros):
        self.lote_id = lote_id
        self.registros = registros

    # 1. len(objeto)
    def __len__(self):
        return len(self.registros)

    # 2. objeto[indice]
    def __getitem__(self, indice):
        return self.registros[indice]

    # 3. objeto_A == objeto_B
    def __eq__(self, otro):
        if isinstance(otro, GestorRegistros):
            # Decidimos que dos lotes son iguales si tienen el mismo ID
            return self.lote_id == otro.lote_id
        return False

    # 4. repr(objeto) o al imprimir en consola interactiva
    def __repr__(self):
        return f"GestorRegistros(lote_id='{self.lote_id}', cantidad={len(self.registros)})"

    # 5. objeto()
    def __call__(self):
        print(f"Ejecutando proceso principal sobre el lote {self.lote_id}...")

# ==========================================
#        USANDO LOS MÉTODOS MÁGICOS
# ==========================================

lote_primario = GestorRegistros("LOTE_100", ["Registro_A", "Registro_B", "Registro_C"])
lote_secundario = GestorRegistros("LOTE_100", []) 

# __len__: Imprime 3
print(len(lote_primario))            

# __getitem__: Imprime "Registro_B"
print(lote_primario[1])              

# __eq__: Imprime True (porque tienen el mismo lote_id, sin importar los registros internos)
print(lote_primario == lote_secundario) 

# __repr__: Imprime el formato técnico
print(repr(lote_primario))           

# __call__: Dispara la ejecución simplemente poniendo paréntesis
lote_primario()