"""
Módulo de infraestructura, conexión y orquestación para Apache Cassandra.
Gestiona el pool de conexiones nativas mediante el protocolo binario de Cassandra,
automatiza la provisión de topologías de replicación (Keyspaces) y orquesta el
proceso de bootstrapping o del dataset histórico.
"""
from cassandra.cluster import Cluster

from motor_cassandra.crearTablasCassandra import crearTablas
from motor_cassandra.importarDatasetCassandra import ImportarDataset


def ConectarCassandra():
    """
    Establece la conexión con la instancia o clúster local de Apache Cassandra.
    Provisiona el Keyspace base si no existe, configura la estrategia de replicación
    y valida el volumen de datos para disparar la ingesta asíncrona del dataset.
    """
    try:
        # Inicialización del objeto Cluster: Administra de manera interna
        # el pooling de conexiones y las políticas de reconexión/balanceo.
        cluster = Cluster(["127.0.0.1"])
        session = cluster.connect()

        # Creación imperativa del Keyspace
        # SimpleStrategy: Ideal para despliegues en un único centro de datos.
        # replication_factor: 1 define cuántas copias del dato vivirán en el anillo.
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS equidata
            WITH replication = {
                'class': 'SimpleStrategy',
                'replication_factor': 1
            }
        """)

        # Modificación del contexto de sesión para apuntar al Keyspace operativo
        session.set_keyspace("equidata")

        crearTablas(session)

        cantidad = contar_registros(session, "caballos_por_carrera")

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
    """
    Ejecuta una consulta de agregación global sobre una familia de columnas (tabla).
    Utiliza el método .one() del driver para extraer de manera directa el registro escalar
    único devuelto por el nodo coordinador que consolidó el conteo del anillo.
    """
    try:
        resultado = session.execute(f"SELECT COUNT(*) FROM {tabla}")
        fila = resultado.one() # Recupera la única tupla de respuesta con el conteo
        return fila[0]

    except Exception as e:
        print(f"No se pudo contar registros en {tabla}: {e}")
        return 0