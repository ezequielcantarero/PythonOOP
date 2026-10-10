# Heredamos de la clase base Exception de Python
class RegistroDuplicadoError(Exception):
    """Excepción lanzada cuando se intenta insertar un ID que ya existe."""
    def __init__(self, id_registro, mensaje="El registro ya existe y será omitido."):
        self.id_registro = id_registro
        self.mensaje = f"[CÓDIGO 1062] ID {id_registro}: {mensaje}"
        # Inicializamos la clase padre con nuestro mensaje armado
        super().__init__(self.mensaje)

class ConexionPerdidaError(Exception):
    """Excepción para caídas críticas de red."""
    pass # A veces ni siquiera necesitas un __init__, solo el nombre específico basta

def insertar_registro(self, registro: dict):
    # Simulamos una validación rápida en la base de datos
    ids_existentes = [1, 2, 3] 
    
    if registro["id"] in ids_existentes:
        # Usamos 'raise' para disparar nuestra excepción personalizada
        raise RegistroDuplicadoError(id_registro=registro["id"])
    
    print(f"Registro {registro['id']} insertado correctamente en PostgreSQL.")

def ejecutar_etl(self, lote_datos):
    for registro in lote_datos:
        try:
            self.destino.insertar_registro(registro)
            
        except RegistroDuplicadoError as e:
            # El programa toma una decisión: Si es un duplicado, solo avisa y SIGUE iterando.
            print(f"⚠️ Omisión silenciosa: {e.mensaje}")
            
        except ConexionPerdidaError:
            # Si se cae la red, la decisión es abortar todo inmediatamente.
            print("🚨 ERROR CRÍTICO: Se perdió la conexión con el destino. Abortando ETL.")
            break 
            
        except Exception as e:
            # La red gigante atrapa cualquier cosa que no hayamos previsto
            print(f"❌ Error desconocido: {e}")