def crearTablas(cassandra_db):
    crearTablaResultadosPorCarrera(cassandra_db)
    crearTablaHistorialPorCaballo(cassandra_db)
    crearTablaHistorialPorJockey(cassandra_db)
    crearTablaCarrerasPorFecha(cassandra_db)
    crearTablaCarrerasPorHipodromo(cassandra_db)
    crearTablaMejoresTiemposDistancia(cassandra_db)

    print("Tablas creadas correctamente en Cassandra.")


def crearTablaResultadosPorCarrera(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS resultados_por_carrera (
            id_carrera int,
            posicion_final int,
            id_caballo int,
            nombre_caballo text,
            id_jockey int,
            nombre_jockey text,
            fecha text,
            hipodromo text,
            distancia int,
            superficie text,
            tiempo_final double,
            PRIMARY KEY ((id_carrera), posicion_final, id_caballo)
        ) WITH CLUSTERING ORDER BY (posicion_final ASC)
    """)


def crearTablaHistorialPorCaballo(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS historial_por_caballo (
            id_caballo int,
            fecha text,
            id_carrera int,
            nombre_caballo text,
            posicion_final int,
            hipodromo text,
            distancia int,
            superficie text,
            tiempo_final double,
            PRIMARY KEY ((id_caballo), fecha, id_carrera)
        ) WITH CLUSTERING ORDER BY (fecha DESC)
    """)


def crearTablaHistorialPorJockey(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS historial_por_jockey (
            id_jockey int,
            fecha text,
            id_carrera int,
            nombre_jockey text,
            id_caballo int,
            nombre_caballo text,
            posicion_final int,
            hipodromo text,
            distancia int,
            superficie text,
            tiempo_final double,
            PRIMARY KEY ((id_jockey), fecha, id_carrera)
        ) WITH CLUSTERING ORDER BY (fecha DESC)
    """)


def crearTablaCarrerasPorFecha(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS carreras_por_fecha (
            fecha text,
            id_carrera int,
            hipodromo text,
            distancia int,
            superficie text,
            cantidad_participantes int,
            PRIMARY KEY ((fecha), id_carrera)
        )
    """)


def crearTablaCarrerasPorHipodromo(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS carreras_por_hipodromo (
            hipodromo text,
            fecha text,
            id_carrera int,
            distancia int,
            superficie text,
            cantidad_participantes int,
            PRIMARY KEY ((hipodromo), fecha, id_carrera)
        ) WITH CLUSTERING ORDER BY (fecha DESC)
    """)


def crearTablaMejoresTiemposDistancia(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS mejores_tiempos_distancia (
            distancia int,
            superficie text,
            tiempo_final double,
            id_carrera int,
            id_caballo int,
            nombre_caballo text,
            fecha text,
            hipodromo text,
            PRIMARY KEY ((distancia, superficie), tiempo_final, id_carrera, id_caballo)
        ) WITH CLUSTERING ORDER BY (tiempo_final ASC)
    """)