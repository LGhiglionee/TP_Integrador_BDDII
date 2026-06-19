"""
Módulo de definición de esquema de datos (DDL) para Apache Cassandra.
Contiene las declaraciones físicas de las tablas diseñadas
bajo la metodología Chebotko, estableciendo estrategias de
particionamiento distribuido y ordenación física en disco (SSTables).
"""
def crearTablas(cassandra_db):
    """
    Orquestador de creación de tablas. Ejecuta de manera secuencial e imperativa
    las directivas DDL en la sesión activa del Keyspace.
    """
    crearTablaCaballosPorCarreras(cassandra_db)
    crearTablaCaballos(cassandra_db)
    crearTablaCarrerasPorCaballos(cassandra_db)
    crearTablaEntrenadorPorJockey(cassandra_db)
    crearTablaJockeyPorPosicionFinalDelCaballo(cassandra_db)
    crearTablaTiempoPromedioPorDupla(cassandra_db)
    crearTablaRendimientoCaballo(cassandra_db)

    print("Tablas creadas correctamente en Cassandra.")

def crearTablaCaballosPorCarreras(cassandra_db):
    """
    Estructura Wide Row para resultados de un evento.
    - Partition Key: race_id (consolida la carrera en un único nodo).
    - Clustering Key: finishing_position (ordena físicamente a los competidores por puesto).
    """
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS caballos_por_carrera (
            race_id text,
            finishing_position int,
            horse_id text,
            horse_number int,
            horse_name text,
            declared_horse_weight int,
            draw int,
            finish_time text,
            PRIMARY KEY (race_id, finishing_position)
        ) WITH CLUSTERING ORDER BY (finishing_position ASC)
    """)

def crearTablaCaballos(cassandra_db):
    """
    Tabla estática de entidades.
    - Partition Key: horse_id (distribución uniforme por Hashing en el clúster).
    Permite búsquedas puntuales del perfil del caballo con complejidad O(1).
    """
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS caballos (
            horse_id text,horse_number int,horse_name text,declared_horse_weight int,PRIMARY KEY (horse_id)
            ) 
    """)

def crearTablaRendimientoCaballo(cassandra_db):
    """
    Tabla de KPIs agregados de negocio.
    Almacena métricas consolidadas listas para el consumo del frontend, evitando
    cálculos masivos de agregación (como COUNT o AVG) en tiempo de ejecución.
    """
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS rendimiento_caballo (
           horse_id text,horse_name text,carreras_corridas int,victorias int,promedio_posicion double,PRIMARY KEY (horse_id)
            ) 
    """)

def crearTablaCarrerasPorCaballos(cassandra_db):
    """
    Modelado de Serie Temporal.
    Permite consultar la historia cronológica de un caballo de forma óptima.
    - Partition Key: horse_id
    - Clustering Key: race_id (mantiene el histórico ordenado).
    """
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS carreras_por_caballos (
            horse_id text,
            race_id text,
            horse_name text,
            finishing_time text,
            finishing_position int,
            draw int,
            PRIMARY KEY (horse_id, race_id)
        ) WITH CLUSTERING ORDER BY (race_id ASC)
    """)

def crearTablaJockeyPorPosicionFinalDelCaballo(cassandra_db):
    """
    Estructura compuesta para filtrado analítico multivariable.
    - Partition Key: horse_id
    - Clustering Keys: finishing_position y finish_time_seconds.
    Garantiza unicidad de la fila y establece un orden de clúster jerárquico doble.
    """
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS jockey_por_posicion_final_del_caballo (
            horse_id text,
            finishing_position int,
            finish_time_seconds int,
            jockey text,
            diferencia int,
            draw int,
            PRIMARY KEY (horse_id, finishing_position, finish_time_seconds)
        ) WITH CLUSTERING ORDER BY (finishing_position ASC, finish_time_seconds ASC)
    """)

def crearTablaEntrenadorPorJockey(cassandra_db):
    """
    Tabla desnormalizada de relaciones profesionales secundarias.
    Permite mapear el rendimiento técnico de los jockeys y sus preparadores.
    - Partition Key: jockey
    - Clustering Key: finish_time_seconds (organiza los registros por velocidad).
    """
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS entrenador_por_jockey (
            jockey text,
            finish_time_seconds int,
            trainer text,
            PRIMARY KEY (jockey, finish_time_seconds)
        ) WITH CLUSTERING ORDER BY (finish_time_seconds ASC)
    """)

def crearTablaTiempoPromedioPorDupla(cassandra_db):
    """
    Calcula el hash combinando AMBOS strings (jockey y trainer).
    Los datos de la dupla se guardan juntos
    y se ordenan en el disco local mediante la Clustering Key 'promedio_tiempo_final'.
    """
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS tiempo_promedio_por_dupla (
            jockey text,
            trainer text,
            promedio_tiempo_final int,
            finish_time_seconds int,
            PRIMARY KEY ((jockey, trainer), promedio_tiempo_final)
        ) WITH CLUSTERING ORDER BY (promedio_tiempo_final ASC)
    """)