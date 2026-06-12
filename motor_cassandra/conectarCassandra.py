from cassandra.cluster import Cluster

from motor_cassandra.crearTablasCassandra import crearTablas
from motor_cassandra.importarDatasetCassandra import ImportarDataset


def ConectarCassandra():
    try:
        cluster = Cluster(["127.0.0.1"])
        session = cluster.connect()

        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS equidata
            WITH replication = {
                'class': 'SimpleStrategy',
                'replication_factor': 1
            }
        """)

        session.set_keyspace("equidata")

        crearTablas(session)

        cantidad = contar_registros(session, "resultados_por_carrera")

        if cantidad == 0:
            print("Base de datos Cassandra vacía. Iniciando importación...")
            ImportarDataset(session)
        else:
            print("Cassandra ya contiene datos. Saltando importación.")

        return session

    except Exception as e:
        print(f"Se produjo un error al conectar con Cassandra: {e}")
        return None


def contar_registros(session, tabla):
    try:
        resultado = session.execute(f"SELECT COUNT(*) FROM {tabla}")
        fila = resultado.one()
        return fila[0]

    except Exception as e:
        print(f"No se pudo contar registros en {tabla}: {e}")
        return 0