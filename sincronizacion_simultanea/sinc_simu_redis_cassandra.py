"""
Módulo de sincronización interestructural optimizado.
Vuelca los resultados calculados en tiempo real en Redis hacia el almacenamiento físico de Cassandra.
"""

def finalizarCarreraSimultanea(redis_db, cassandra_session, idCarrera):
    """
    Sincronización simultánea autónoma.
    Toma el ranking generado en el Sorted Set de Redis y persiste las posiciones
    reales simuladas en la tabla 'caballos_por_carrera' de Apache Cassandra.
    """
    idCarrera = str(idCarrera).strip()
    carrera_key = f"carrera:{idCarrera}:info"
    ranking_key = f"carrera:{idCarrera}:ranking"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe en Redis.")
        return

    redis_db.hset(carrera_key, "estado", "finalizada")
    print(f"Carrera {idCarrera} marcada como 'finalizada' en RAM.")

    ranking_simulado = redis_db.zrevrange(ranking_key, 0, -1)

    if not ranking_simulado:
        print("No se encontró un ranking simulado en memoria para esta carrera.")
        return

    print(f"\nRealizando la sincronización. "
          f"\nTransfiriendo {len(ranking_simulado)} competidores a Cassandra...")

    if cassandra_session is None:
        print("Error: La sesión de Cassandra es nula. No se pudo guardar en disco.")
        return

    query = """
        INSERT INTO caballos_por_carrera (
            race_id, finishing_position, horse_id, horse_number, horse_name, declared_horse_weight, draw, finish_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    insert_preparado = cassandra_session.prepare(query)

    for posicion_final, horse_id in enumerate(ranking_simulado, start=1):
        caballo_redis = redis_db.hgetall(f"carrera:{idCarrera}:caballo:{horse_id}")

        if not caballo_redis:
            continue

        c_name = caballo_redis.get("horse_name", "Desconocido")
        f_time = caballo_redis.get("finish_time", "1.00.00")

        try:
            c_number = int(caballo_redis.get("horse_number", 0))
        except ValueError:
            c_number = 0

        try:
            c_weight = int(caballo_redis.get("declared_horse_weight", 0))
        except ValueError:
            c_weight = 0

        try:
            draw_val = int(caballo_redis.get("draw", 0))
        except ValueError:
            draw_val = 0

        cassandra_session.execute(insert_preparado, [
            idCarrera, int(posicion_final), str(horse_id), c_number, c_name, c_weight, draw_val, f_time
        ])