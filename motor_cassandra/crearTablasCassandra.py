def crearTablas(cassandra_db):
    crearTablaResultadosPorCarrera(cassandra_db)
    crearTablaHistorialPorCaballo(cassandra_db)
    crearTablaHistorialPorJockey(cassandra_db)
    crearTablaCaballosPorEntrenador(cassandra_db)
    crearTablaCaballosPorPadre(cassandra_db)
    crearTablaMejoresTiemposPorCarrera(cassandra_db)

    print("Tablas creadas correctamente en Cassandra.")

def crearTablaResultadosPorCarrera(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS resultados_por_carrera (
            race_id text,
            finishing_position int,
            horse_id text,
            horse_number int,
            horse_name text,
            jockey text,
            trainer text,
            actual_weight int,
            declared_horse_weight int,
            draw int,
            running_position_1 int,
            running_position_2 int,
            running_position_3 int,
            finish_time text,
            finish_time_seconds double,
            father text,
            mother text,
            gfather text,
            PRIMARY KEY ((race_id), finishing_position, horse_id)
        ) WITH CLUSTERING ORDER BY (finishing_position ASC)
    """)


def crearTablaHistorialPorCaballo(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS historial_por_caballo (
            horse_id text,
            race_id text,
            finishing_position int,
            horse_number int,
            horse_name text,
            jockey text,
            trainer text,
            actual_weight int,
            declared_horse_weight int,
            draw int,
            running_position_1 int,
            running_position_2 int,
            running_position_3 int,
            finish_time text,
            finish_time_seconds double,
            father text,
            mother text,
            gfather text,
            PRIMARY KEY ((horse_id), race_id)
        ) WITH CLUSTERING ORDER BY (race_id DESC)
    """)


def crearTablaHistorialPorJockey(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS historial_por_jockey (
            jockey text,
            race_id text,
            horse_id text,
            finishing_position int,
            horse_number int,
            horse_name text,
            trainer text,
            actual_weight int,
            declared_horse_weight int,
            draw int,
            running_position_1 int,
            running_position_2 int,
            running_position_3 int,
            finish_time text,
            finish_time_seconds double,
            father text,
            mother text,
            gfather text,
            PRIMARY KEY ((jockey), race_id, horse_id)
        ) WITH CLUSTERING ORDER BY (race_id DESC, horse_id ASC)
    """)


def crearTablaCaballosPorEntrenador(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS caballos_por_entrenador (
            trainer text,
            horse_name text,
            horse_id text,
            race_id text,
            finishing_position int,
            jockey text,
            horse_number int,
            actual_weight int,
            declared_horse_weight int,
            draw int,
            running_position_1 int,
            running_position_2 int,
            running_position_3 int,
            finish_time text,
            finish_time_seconds double,
            father text,
            mother text,
            gfather text,
            PRIMARY KEY ((trainer), horse_name, horse_id, race_id)
        ) WITH CLUSTERING ORDER BY (horse_name ASC, horse_id ASC, race_id DESC)
    """)


def crearTablaCaballosPorPadre(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS caballos_por_padre (
            father text,
            horse_name text,
            horse_id text,
            race_id text,
            finishing_position int,
            jockey text,
            trainer text,
            horse_number int,
            actual_weight int,
            declared_horse_weight int,
            draw int,
            running_position_1 int,
            running_position_2 int,
            running_position_3 int,
            finish_time text,
            finish_time_seconds double,
            mother text,
            gfather text,
            PRIMARY KEY ((father), horse_name, horse_id, race_id)
        ) WITH CLUSTERING ORDER BY (horse_name ASC, horse_id ASC, race_id DESC)
    """)


def crearTablaMejoresTiemposPorCarrera(cassandra_db):
    cassandra_db.execute("""
        CREATE TABLE IF NOT EXISTS mejores_tiempos_por_carrera (
            race_id text,
            finish_time_seconds double,
            horse_id text,
            horse_name text,
            finishing_position int,
            horse_number int,
            jockey text,
            trainer text,
            actual_weight int,
            declared_horse_weight int,
            draw int,
            running_position_1 int,
            running_position_2 int,
            running_position_3 int,
            finish_time text,
            father text,
            mother text,
            gfather text,
            PRIMARY KEY ((race_id), finish_time_seconds, horse_id)
        ) WITH CLUSTERING ORDER BY (finish_time_seconds ASC, horse_id ASC)
    """)