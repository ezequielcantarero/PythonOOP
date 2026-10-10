import time

# 1. Las Excepciones Personalizadas (La inteligencia)
class RegistroDuplicadoError(Exception):
    pass

class ConexionPerdidaError(Exception):
    pass

# 2. El Decorador Selectivo (El escudo)
def reintentar_solo_conexion(intentos=3, espera=2):
    def decorador(funcion_original):
        def envoltura(*args, **kwargs):
            for intento in range(1, intentos + 1):
                try:
                    return funcion_original(*args, **kwargs)
                
                # REGLA 1: Si es un fallo de red, el decorador lo frena y reintenta.
                except ConexionPerdidaError as e:
                    print(f"🔌 [Fallo de Red] Intento {intento}/{intentos}. Reintentando... ({e})")
                    if intento < intentos:
                        time.sleep(espera)
                    else:
                        raise # Si se acaban los intentos, relanza el error hacia arriba
                
                # REGLA 2: No capturamos RegistroDuplicadoError aquí. 
                # Al no atraparlo, el error "pasa de largo" el decorador y cancela los reintentos.

        return envoltura
    return decorador

# 3. La Aplicación en la Base de Datos
class ConexionPostgreSQL:
    
    @reintentar_solo_conexion(intentos=3, espera=1)
    def insertar_registro(self, id_registro):
        # Simulamos la desconexión
        if id_registro == 999:
            raise ConexionPerdidaError("El servidor PostgreSQL dejó de responder.")
        
        # Simulamos la validación de un duplicado
        if id_registro == 2:
            raise RegistroDuplicadoError("El ID 2 ya existe en la tabla.")
            
        print(f"✅ Registro {id_registro} insertado.")