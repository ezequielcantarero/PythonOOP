import time

# 1. Creamos el decorador
def reintentar_conexion(funcion_original):
    def envoltura(*args, **kwargs):
        intentos = 3
        for i in range(intentos):
            try:
                # Intentamos ejecutar la función original tal cual vino
                return funcion_original(*args, **kwargs)
            except Exception as e:
                print(f"[Fallo] Intento {i+1} de {intentos}. Error: {e}")
                time.sleep(2) # Esperamos 2 segundos antes del próximo ciclo
        print("Se agotaron los intentos. Abortando operación.")
    return envoltura


# 2. Aplicamos el decorador 
@reintentar_conexion
def extraer_datos_api(url):
    print(f"Conectando a {url}...")
    # Simulamos un error de red para ver el decorador en acción
    raise ConnectionError("Timeout en el servidor destino")

# 3. Ejecutamos nuestra función de forma normal
#extraer_datos_api("api.binance.com/v3/ticker")

""" 
Conectando a api.binance.com/v3/ticker...
[Fallo] Intento 1 de 3. Error: Timeout en el servidor destino
Conectando a api.binance.com/v3/ticker...
[Fallo] Intento 2 de 3. Error: Timeout en el servidor destino
Conectando a api.binance.com/v3/ticker...
[Fallo] Intento 3 de 3. Error: Timeout en el servidor destino
Se agotaron los intentos. Abortando operación.
"""

"""
Ejemplos de aplicaciones
Medición de rendimiento (Profiling): Un decorador @medir_tiempo que inicia un cronómetro antes de que arranque la función y lo detiene al final. Es vital para detectar cuellos de botella y saber, por ejemplo, si una extracción masiva de datos está tardando más de lo normal.
Registro de actividad (Logging): Un decorador @guardar_log que anota automáticamente en un archivo de texto cada vez que se ejecuta una función, indicando la hora exacta, qué parámetros recibió y si tuvo éxito. Ideal para rastrear procesos automáticos que corren solos de madrugada.
Sistemas de caché: Un decorador @usar_cache (Python ya trae uno nativo llamado @lru_cache). Si tienes una función que descarga datos históricos o realiza un cálculo matemático pesado, el decorador guarda la respuesta en memoria. Si vuelves a llamar a la función con los mismos parámetros, el decorador te devuelve el resultado guardado al instante sin volver a procesar nada.
Verificación de seguridad o permisos: Un decorador @requiere_autenticacion. Antes de dejar que una función modifique una base de datos o dispare una acción crítica, el decorador frena el proceso, verifica si las credenciales o el token son válidos y solo entonces deja pasar la orden.
Validación de formato de datos: Un decorador @limpiar_entradas que revisa y estandariza la información antes de que llegue a la función principal. Por ejemplo, asegurarse de que todos los textos lleguen en minúsculas o que los números no tengan valores nulos antes de procesarlos.
Tolerancia a fallos (Reintentos): Un decorador @reintentar, como el que vimos antes, que captura desconexiones temporales de internet o caídas momentáneas de servidores, y vuelve a intentar la ejecución un par de veces antes de rendirse.
"""

# Capa 1: El Decorador (Recibe la función original)
def medir_tiempo(funcion_original):
    
    # Capa 2: La Envoltura (Recibe los argumentos de la función original)
    def envoltura(*args, **kwargs):
        
        # --- ANTES DE LA EJECUCIÓN ---
        tiempo_inicio = time.time()  # Arrancamos el cronómetro
        
        # Capa 3: Ejecutamos la función original de forma normal
        resultado = funcion_original(*args, **kwargs) 
        
        # --- DESPUÉS DE LA EJECUCIÓN ---
        tiempo_fin = time.time()     # Detenemos el cronómetro
        
        # Calculamos la diferencia
        milisegundos = (tiempo_fin - tiempo_inicio) * 1000
        print(f"[⏱️] La función '{funcion_original.__name__}' tardó {milisegundos:.2f} ms.")
        
        # Devolvemos el resultado para que el programa siga funcionando como si nada
        return resultado
        
    # El decorador devuelve la función envuelta, lista para usarse
    return envoltura

    # Aplicamos el decorador
@medir_tiempo
def procesar_extraccion_datos(filas):
    print(f"Extrayendo {filas} filas de la base de datos...")
    time.sleep(1.2)  # Simulamos una consulta pesada que tarda 1.2 segundos
    return "Extracción finalizada"

@medir_tiempo
def calcular_metricas():
    # Simulamos un cálculo muy rápido
    suma = sum([i for i in range(10000)])
    return suma

# Ejecutamos las funciones normalmente
#resultado_datos = procesar_extraccion_datos(5000)
#resultado_calculo = calcular_metricas()


# Capa 1: El configurador (Recibe tus parámetros personalizados)
def reintentar(intentos=3, espera=2):
    
    # Capa 2: El decorador real (Recibe la función a envolver)
    def decorador(funcion_original):
        
        # Capa 3: La envoltura (Atrapa todo con el comodín de args y kwargs)
        def envoltura(*args, **kwargs):
            for intento in range(1, intentos + 1):
                try:
                    # Intentamos ejecutar la función pasándole todo intacto
                    return funcion_original(*args, **kwargs)
                except Exception as e:
                    print(f"[Fallo] Intento {intento}/{intentos}. Reintentando en {espera}s... (Error: {e})")
                    if intento < intentos:
                        time.sleep(espera)
            
            # Si el ciclo for termina sin un 'return', se agotaron las oportunidades
            print("Operación abortada por fallos continuos.")
        
        return envoltura  # El decorador entrega la envoltura armada
    return decorador      # El configurador entrega el decorador listo

# Usamos el decorador pasándole los parámetros a la Capa 1
@reintentar(intentos=4, espera=1)
def evaluar_trigger_ruptura(simbolo, timeframe="1m"):
    print(f"Evaluando volumen para {simbolo} en {timeframe}...")
    # Simulamos un rechazo del servidor
    raise ConnectionError("Timeout de respuesta del exchange")

# Disparamos la función y vemos a *args y **kwargs hacer su trabajo
evaluar_trigger_ruptura("BTCUSDT", timeframe="5m")