import csv
import os

import redis

def conectarRedis():

    try:

        redis_db = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )

        redis_db.ping()

        print("Conexión exitosa con Redis.")

        return redis_db

    except Exception as e:

        print(f"Se produjo un error al conectar con Redis: {e}")

def leerDataset(filtros=None, campos=None):
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(ruta_script, "..", "datasets", "race-result-horse.csv")

    filtros = filtros or {}

    with open(path, "r", encoding="UTF-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            cumple_filtros = all(
                fila.get(campo) == str(valor)
                for campo, valor in filtros.items()
            )

            if cumple_filtros:
                if campos is None:
                    yield fila
                else:
                    yield {
                        campo: fila.get(campo, "")
                        for campo in campos
                    }
