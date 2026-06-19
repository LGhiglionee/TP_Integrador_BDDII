"""
Módulo de conexión y lectura de datos para Redis.
Gestiona la persistencia de la conexión mediante el protocolo RESP y
proporciona un iterador eficiente para leer los datasets locales.
"""
import csv
import os

import redis

def conectarRedis():
    """
    Establece la conexión con el servidor Redis local.
    'decode_responses=True' es vital: permite que Redis devuelva strings
    en lugar de bytes, simplificando la manipulación de datos en Python.
    """
    try:
        # Inicialización del cliente Redis (pool de conexiones por defecto)
        redis_db = redis.Redis(host='localhost',port=6379,decode_responses=True)

        # Validación técnica: ping comprueba que el servidor esté activo
        redis_db.ping()
        print("Conexión exitosa con Redis.")
        return redis_db

    except Exception as e:
        print(f"Se produjo un error al conectar con Redis: {e}")

def leerDataset(filtros=None, campos=None):
    """
    Generador de datos (Lazy Loader): Lee el CSV línea a línea.
    El uso de 'yield' es una excelente práctica de memoria: en lugar de cargar
    todo el archivo en RAM, entrega un registro a la vez, lo cual es ideal
    para datasets grandes.
    """
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(ruta_script, "..", "datasets", "race-result-horse.csv")

    filtros = filtros or {}

    with open(path, "r", encoding="UTF-8") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")

        for fila in lector:
            # Filtrado dinámico en tiempo de lectura
            cumple_filtros = all(
                fila.get(campo) == str(valor)
                for campo, valor in filtros.items()
            )

            if cumple_filtros:
                if campos is None:
                    yield fila
                else:
                    # Proyección: retorna solo los campos solicitados
                    yield {campo: fila.get(campo, "")
                           for campo in campos}