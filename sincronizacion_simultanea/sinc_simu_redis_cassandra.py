def finalizarCarreraSimultanea(redis_db, cassandra_session, idCarrera):
    """
    Sincronización simultánea: Cambia el estado en la RAM (Redis) y
    consolida los resultados definitivos en el disco analítico (Cassandra).
    """
    idCarrera = str(idCarrera).strip()
    carrera_key = f"carrera:{idCarrera}:info"
    participantes_key = f"carrera:{idCarrera}:participantes"

    # Validamos que la carrera exista en Redis antes de cerrarla
    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe en Redis.")
        return

    # 1. IMPACTO EN REDIS (RAM): Cambiamos el estado a finalizada
    redis_db.hset(carrera_key, "estado", "finalizada")
    print(f"[REDIS] Estado de la carrera {idCarrera} actualizado a 'finalizada' en memoria RAM.")

    # Recuperamos los caballos que estaban participando desde el SET de Redis
    participantes = [p.decode('utf-8') if isinstance(p, bytes) else str(p) for p in redis_db.smembers(participantes_key)]

    if not participantes:
        print("[REDIS] No se encontraron participantes activos para trasladar.")
        return

    print(f"\n[SIMULTÁNEO] Transfiriendo competidores a Cassandra...")

    # 2. IMPACTO EN CASSANDRA (DISCO): Guardamos el resultado en las tablas de historiales
    if cassandra_session is not None:
        for posicion, horse_id in enumerate(participantes, start=1):
            # Traemos los datos crudos del caballo que estaban en el Hash de Redis
            caballo_redis = redis_db.hgetall(f"carrera:{idCarrera}:caballo:{horse_id}")

            # Decodificamos los bytes de Redis a strings limpios de Python
            def decodificar(campo, default=""):
                val = caballo_redis.get(campo)
                return val.decode("utf-8") if val else default

            c_name = decodificar(b"horse_name", "Caballo Ficticio")
            c_number = int(decodificar(b"horse_number", "0"))
            jockey = decodificar(b"jockey", "Jockey Ficticio")
            trainer = decodificar(b"trainer", "Entrenador Ficticio")

            # Insertamos simultáneamente en resultados_por_carrera de Cassandra
            query = """
                INSERT INTO resultados_por_carrera (
                    race_id, finishing_position, horse_id, horse_number, horse_name, jockey, trainer, finish_time, finish_time_seconds
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            insert_preparado = cassandra_session.prepare(query)
            cassandra_session.execute(insert_preparado, [
                idCarrera, int(posicion), horse_id, c_number, c_name, jockey, trainer, "1.14.05", 74.05
            ])
            print(f"   -> [CASSANDRA] Guardado definitivo: Puesto {posicion}° para {c_name} ({horse_id})")

        print(f"\nÉxito simultáneo: Carrera {idCarrera} cerrada en RAM y persistida en el histórico columnar.")
    else:
        print("Alerta: No se pudo replicar en Cassandra porque la sesión no está activa.")