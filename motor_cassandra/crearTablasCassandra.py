def crearTablas(cassandra_db):
    crearTablaCaballosPorCarreras(cassandra_db)
    crearTablaCaballos(cassandra_db)
    crearTablaCarrerasPorCaballos(cassandra_db)
    crearTablaEntrenadorPorJockey(cassandra_db)
    crearTablaJockeyPorPosicionFinalDelCaballo(cassandra_db)
    crearTablaTiempoPromedioPorDupla(cassandra_db)
    crearTablaRendimientoCaballo(cassandra_db)

    print("Tablas creadas correctamente en Cassandra.")

def crearTablaCaballosPorCarreras(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS caballos_por_carrera (
            race_id text,
            horse_id text,
            horse_number int,
            horse_name text,
            declared_horse_weight int,
            draw int,
            finish_time text,
            draw int,
            PRIMARY KEY (race_id)
        ) WITH CLUSTERING ORDER BY (finishing_position ASC)
    """)


def crearTablaCaballos(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS caballos (
            horse_id text,
            horse_number int,
            horse_name text,
            declared_horse_weight int,
            PRIMARY KEY (horse_id)
        ) 
    """)


def crearTablaRendimientoCaballo(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS rendimiento_caballo (
           horse_id text,
           carreras_corridas int,
           victorias int,
           promedio_posicion double,
            PRIMARY KEY (horse_id)
        ) 
    """)


def crearTablaCarrerasPorCaballos(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS carreras_por_caballos (
            horse_id text,
            race_id text,
            horse_name text,
            finishing_time text,
            finishing_position int,
            draw int,
            PRIMARY KEY (horse_id)
        ) WITH CLUSTERING ORDER BY (race_id ASC)
    """)


def crearTablaJockeyPorPosicionFinalDelCaballo(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS jockey_por_posicion_final_del_caballo (
            horse_id text,
            finishing_position int,
            finish_time_seconds int,
            jockey text,
            diferencia int,
            draw int,
            PRIMARY KEY (horse_id)
        ) WITH CLUSTERING ORDER BY (finishing_position ASC, finish_time_seconds ASC)
    """)


def crearTablaEntrenadorPorJockey(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS entrenador_por_jockey (
            jockey text,
            finish_time_seconds int,
            trainer text,
            PRIMARY KEY (jockey)
        ) WITH CLUSTERING ORDER BY (finish_time_seconds ASC)
    """)

def crearTablaTiempoPromedioPorDupla(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS tiempo_promedio_por_dupla (
            jockey text,
            trainer text,
            promedio_tiempo_final int,
            finish_time_seconds int,
            PRIMARY KEY (jockey, trainer)
        ) WITH CLUSTERING ORDER BY (promedio_tiempo_final ASC)
    """)