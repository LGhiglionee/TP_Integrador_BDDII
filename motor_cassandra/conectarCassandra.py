import csv
import os
from cassandra.cluster import Cluster


def conectarCassandra():
    try:
        cluster = Cluster(['127.0.0.1'], port=9042)
        session = cluster.connect()

        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS cursus
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """)

        session.set_keyspace('cursus')

        print("Conexión exitosa con Cassandra.")

        return session

    except Exception as e:
        print(f"Se produjo un error al conectar con Cassandra: {e}")


def leerDataset(filtros=None, campos=None):
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(ruta_script, "..", "datasets", "race-result-horse.csv")

    filtros = filtros or {}

    with open(path, "r", encoding="UTF-8") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")

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


if __name__ == "__main__":
    conectarCassandra()