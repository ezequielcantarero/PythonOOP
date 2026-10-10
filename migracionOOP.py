from pymongo import MongoClient
import psycopg2
from abc import ABC, abstractmethod

class ConexionBase(ABC):
    """
    Clase abstracta que define el contrato obligatorio 
    para cualquier conexión a base de datos en nuestro ETL.
    """
    
    @abstractmethod
    def conectar(self):
        pass

    @abstractmethod
    def desconectar(self):
        pass

    @abstractmethod
    def crear_tabla(self, nombre_tabla):
        pass

    @abstractmethod
    def eliminar_tabla(self, nombre_tabla):
        pass

    @abstractmethod
    def insertar_registro(self, tabla, registro: dict):
        pass

    @abstractmethod
    def obtener_registros(self, tabla) -> list:
        pass

    @abstractmethod
    def eliminar_registro(self, tabla, clave, valor):
        pass


class ConexionPostgreSQL(ConexionBase):
    def __init__(self, db_name, user, password, host="localhost", port="5432"):
        self.db_name = db_name
        self._user = user
        self._password = password
        self.host = host
        self.port = port 
    
    def conectar(self):
        try:
            self.conn = psycopg2.connect(database=self.db_name, 
                                          user=self._user, 
                                          password=self._password, 
                                          host=self.host, 
                                          port=self.port)
            self.cursor = self.conn.cursor()
            print(f"Conexión exitosa a PostgreSQL: {self.db_name}")
        except Exception as e:
            print(f"Error al conectar a PostgreSQL: {e}")

    def desconectar(self):
        if hasattr(self, 'conn'):
            self.cursor.close()
            self.conn.close()
            print("Desconectado de PostgreSQL.")

    def crear_tabla(self, nombre_tabla):
        # Definimos un esquema genérico para usuarios
        query = f"""
        CREATE TABLE IF NOT EXISTS {nombre_tabla} (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            email VARCHAR(100) UNIQUE
        );
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print(f"[PostgreSQL] Tabla '{nombre_tabla}' creada exitosamente.")
        except Exception as e:
            print(f"[PostgreSQL] Error al crear la tabla: {e}")
            self.conn.rollback()

    def eliminar_tabla(self, nombre_tabla):
        query = f"DROP TABLE IF EXISTS {nombre_tabla};"
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print(f"[PostgreSQL] Tabla '{nombre_tabla}' eliminada.")
        except Exception as e:
            print(f"[PostgreSQL] Error al eliminar: {e}")
            self.conn.rollback()

    def insertar_registro(self, tabla, registro: dict):
        # Transforma el diccionario en sintaxis SQL
        columnas = ', '.join(registro.keys())
        placeholders = ', '.join(['%s'] * len(registro))
        valores = tuple(registro.values())
        
        query = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"
        try:
            self.cursor.execute(query, valores)
            self.conn.commit()
            print(f"[Postgres] Registro insertado en '{tabla}'.")
        except Exception as e:
            self.conn.rollback()
            print(f"[Postgres] Error al insertar: {e}")

    def obtener_registros(self, tabla):
        try:
            self.cursor.execute(f"SELECT * FROM {tabla}")
            columnas = [desc[0] for desc in self.cursor.description]
            filas = self.cursor.fetchall()
            # Convertimos las filas (tuplas) de vuelta a diccionarios
            return [dict(zip(columnas, fila)) for fila in filas]
        except Exception as e:
            print(f"[Postgres] Error al hacer SELECT: {e}")
            return []

    def eliminar_registro(self, tabla, clave, valor):
        query = f"DELETE FROM {tabla} WHERE {clave} = %s"
        try:
            self.cursor.execute(query, (valor,))
            self.conn.commit()
            print(f"[Postgres] Registro(s) eliminado(s) donde {clave}={valor}.")
        except Exception as e:
            self.conn.rollback()
            print(f"[Postgres] Error al eliminar: {e}")


class ConexionMongoDB(ConexionBase):
    def __init__(self, uri, db_name):
        self.uri = uri
        self.db_name = db_name

    def conectar(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print(f"Conexión exitosa a MongoDB: {self.db_name}")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")

    def desconectar(self):
        if hasattr(self, 'client'):
            self.client.close()
            print("Desconectado de MongoDB.")   

    def crear_tabla(self, nombre_tabla):
        # En Mongo las colecciones se crean solas al insertar datos, 
        # pero podemos forzar su creación explícita así:
        try:
            self.db.create_collection(nombre_tabla)
            print(f"[MongoDB] Colección '{nombre_tabla}' creada exitosamente.")
        except Exception as e:
            print(f"[MongoDB] La colección '{nombre_tabla}' ya existe o hubo un error.")

    def eliminar_tabla(self, nombre_tabla):
        try:
            self.db[nombre_tabla].drop()
            print(f"[MongoDB] Colección '{nombre_tabla}' eliminada.")
        except Exception as e:
            print(f"[MongoDB] Error al eliminar: {e}")

    def insertar_registro(self, tabla, registro: dict):
        try:
            self.db[tabla].insert_one(registro)
            print(f"[Mongo] Documento insertado en '{tabla}'.")
        except Exception as e:
            print(f"[Mongo] Error al insertar: {e}")

    def obtener_registros(self, tabla):
        try:
            # find() devuelve un cursor. Excluimos "_id" para que no rompa la 
            # compatibilidad al enviar este diccionario a Postgres.
            datos = list(self.db[tabla].find({}, {"_id": 0}))
            return datos
        except Exception as e:
            print(f"[Mongo] Error al obtener datos: {e}")
            return []

    def eliminar_registro(self, tabla, clave, valor):
        try:
            resultado = self.db[tabla].delete_many({clave: valor})
            print(f"[Mongo] {resultado.deleted_count} documento(s) eliminado(s) donde {clave}={valor}.")
        except Exception as e:
            print(f"[Mongo] Error al eliminar: {e}")


class GestorMigracion:
    def __init__(self, origen, destino):
        # Composición: El gestor "tiene un" origen y "tiene un" destino.
        # Recibe las conexiones ya creadas desde afuera.
        self.origen = origen
        self.destino = destino

    def ejecutar_transferencia(self):
        print("--- Iniciando Pipeline de Migración ---")
        
        # Polimorfismo en acción: El gestor no sabe si es Mongo o Postgres.
        # Solo confía en que ambos objetos cumplirán el contrato de la clase base.
        self.origen.conectar()
        self.destino.conectar()
        
        print("\n[Extracción] Leyendo datos del origen...")
        # Simulamos la lectura en memoria
        datos = "[... 151 registros de usuarios limpios ...]"
        print(f"Datos en memoria: {datos}")
        
        print("[Carga] Transformando e insertando datos en el destino...")
        print("Migración de registros completada con éxito.\n")
        
        # Cerramos las conexiones de forma segura
        self.origen.desconectar()
        self.destino.desconectar()
        print("--- Pipeline Finalizado ---")

    def ejecutar_etl(self, tabla_origen, tabla_destino):
        print("\n--- INICIANDO PIPELINE DE MIGRACIÓN ---")
        self.origen.conectar()
        self.destino.conectar()

        # 1. Select (Extraer)
        print("\n>> Extrayendo registros...")
        datos_en_memoria = self.origen.obtener_registros(tabla_origen)
        print(f"Se extrajeron {len(datos_en_memoria)} registros del origen.")

        # 2. Insert (Cargar)
        print("\n>> Cargando registros en destino...")
        for registro in datos_en_memoria:
            self.destino.insertar_registro(tabla_destino, registro)

        self.origen.desconectar()
        self.destino.desconectar()
        print("--- MIGRACIÓN COMPLETADA EXITOSAMENTE ---\n")


# ==========================================
#        EJECUCIÓN DEL SISTEMA
# ==========================================

# 1. Creamos las conexiones individuales (Encapsulando credenciales)
mongo_conn = ConexionMongoDB("mongodb://localhost:27017", "users")
pg_conn = ConexionPostgreSQL("PracticaOOP", "postgres", "admin123", port="5432")

# 2. Ensamblamos el Gestor inyectando las dependencias (Composición)
pipeline = GestorMigracion(origen=mongo_conn, destino=pg_conn)

# 3. Ejecutamos la magia (Polimorfismo en ejecución)
pipeline.ejecutar_transferencia()


#  ==========================================
# Prueba PostgreSQL
pg = ConexionPostgreSQL("PracticaOOP", "postgres", "admin123")
pg.conectar()
pg.crear_tabla("usuarios_migrados")
pg.eliminar_tabla("usuarios_migrados")
pg.desconectar()

print("-" * 30)

# Prueba MongoDB
mongo = ConexionMongoDB("mongodb://localhost:27017", "users")
mongo.conectar()
mongo.crear_tabla("usuarios_origen")
mongo.eliminar_tabla("usuarios_origen")
mongo.desconectar()

# --- PRUEBA DEL PIPELINE ---
mongo_conn = ConexionMongoDB("mongodb://localhost:27017", "ezequiel_dev")
pg_conn = ConexionPostgreSQL("ezequiel_dev", "postgres", "supersecreto")

# Supongamos que inyectamos algunos datos de prueba en Mongo primero
mongo_conn.conectar()
mongo_conn.insertar_registro("usuarios", {"id": 1, "nombre": "Ezequiel", "rol": "Data Eng"})
mongo_conn.insertar_registro("usuarios", {"id": 2, "nombre": "Anna", "rol": "Analyst"})
mongo_conn.desconectar()

# Usamos la Composición para orquestar el movimiento
pipeline = GestorMigracion(origen=mongo_conn, destino=pg_conn)
pipeline.ejecutar_etl("usuarios", "usuarios_migrados")