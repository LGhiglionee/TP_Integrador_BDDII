def finalizarCarreraSimultanea(redis_db, cassandra_session, idCarrera):
    """
    Sincronización simultánea autónoma.
    Decodifica internamente los datos de Redis sin depender de funciones auxiliares externas.
    """
    idCarrera = str(idCarrera).strip()
    carrera_key = f"carrera:{idCarrera}:info"
    participantes_key = f"carrera:{idCarrera}:participantes"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe en Redis.")
        return

    # 1. ACTUALIZACIÓN EN REDIS (RAM)
    redis_db.hset(carrera_key, "estado", "finalizada")
    print(f"(EN REDIS) Carrera {idCarrera} finalizada en RAM.")

    # Decodificamos la lista de participantes directamente aquí
    participantes_raw = redis_db.smembers(participantes_key)
    participantes = [p.decode("utf-8") if isinstance(p, bytes) else str(p) for p in participantes_raw]

    if not participantes:
        print("[REDIS] No hay participantes en memoria para transferir.")
        return

    print(f"\n(EN SIMULTÁNEO EN CASSANDRA) Insertando {len(participantes)} datos en Cassandra...")

    # 2. PERSISTENCIA EN CASSANDRA (DISCO)
    if cassandra_session is not None:
        query = """
            INSERT INTO resultados_por_carrera (
                race_id, finishing_position, horse_id, horse_number, horse_name, jockey, trainer, finish_time, finish_time_seconds
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        insert_preparado = cassandra_session.prepare(query)

        for horse_id in participantes:
            # Leemos el hash crudo de Redis
            caballo_raw = redis_db.hgetall(f"carrera:{idCarrera}:caballo:{horse_id}")

            # Lo normalizamos localmente (convierte bytes de Redis a strings de Python)
            caballo_redis = {
                (k.decode("utf-8") if isinstance(k, bytes) else str(k)): (v.decode("utf-8") if isinstance(v, bytes) else str(v))
                for k, v in caballo_raw.items()
            }

            # Extraemos los atributos reales
            c_name = caballo_redis.get("horse_name", "Desconocido")
            jockey = caballo_redis.get("jockey", "Desconocido")
            trainer = caballo_redis.get("trainer", "Desconocido")
            f_time = caballo_redis.get("finish_time", "1.10.00")

            try:
                posicion = int(caballo_redis.get("finishing_position", 0))
            except:
                posicion = 0

            try:
                c_number = int(caballo_redis.get("horse_number", 0))
            except:
                c_number = 0

            try:
                f_seconds = float(caballo_redis.get("finish_time_seconds", 70.0))
            except:
                f_seconds = 70.0

            cassandra_session.execute(insert_preparado, [
                idCarrera, posicion, horse_id, c_number, c_name, jockey, trainer, f_time, f_seconds
            ])
            print(f" El caballo {c_name} con ID: ({horse_id}) en posición {posicion}° fue insertado en Cassandra.")