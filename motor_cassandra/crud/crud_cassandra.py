def crear_resultado_manual(session, race_id, finishing_position, horse_id, horse_number, horse_name, jockey, trainer, finish_time, finish_time_seconds):
    query = """
        INSERT INTO resultados_por_carrera (
            race_id, finishing_position, horse_id, horse_number, horse_name, 
            jockey, trainer, finish_time, finish_time_seconds
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        preparado = session.prepare(query)
        session.execute(preparado, [
            str(race_id), int(finishing_position), str(horse_id),
            int(horse_number), str(horse_name), str(jockey),
            str(trainer), str(finish_time), float(finish_time_seconds)
        ])
        print(f"CRUD: Resultado creado para el caballo {horse_name} en la carrera {race_id}.")
    except Exception as e:
        print(f"Error en CRUD (Crear): {e}")

def leer_resultado_especifico(session, race_id, finishing_position, horse_id):
    query = """
        SELECT * FROM resultados_por_carrera 
        WHERE race_id = %s AND finishing_position = %s AND horse_id = %s
    """
    try:
        filas = session.execute(query, (str(race_id), int(finishing_position), str(horse_id)))
        resultados = list(filas)
        if not resultados:
            print("CRUD: No se encontró ningún registro con esa Clave Primaria.")
            return None

        r = resultados[0]
        print(f"\n--- Registro Encontrado ---")
        print(f"Carrera: {r.race_id} | Puesto: {r.finishing_position} | Caballo: {r.horse_name}")
        print(f"Jockey: {r.jockey} | Tiempo: {r.finish_time}")
        return r
    except Exception as e:
        print(f"Error en CRUD (Leer): {e}")
        return None

def actualizar_tiempo_resultado(session, race_id, finishing_position, horse_id, nuevo_time, nuevo_time_seconds):
    query = """
        UPDATE resultados_por_carrera
        SET finish_time = ?, finish_time_seconds = ?
        WHERE race_id = ? AND finishing_position = ? AND horse_id = ?
    """
    try:
        preparado = session.prepare(query)
        session.execute(preparado, [str(nuevo_time), float(nuevo_time_seconds), str(race_id), int(finishing_position), str(horse_id)])
        print(f"CRUD: Tiempo actualizado con éxito para la carrera {race_id}.")
    except Exception as e:
        print(f"Error en CRUD (Actualizar): {e}")

def eliminar_resultado_especifico(session, race_id, finishing_position, horse_id):
    query = """
        DELETE FROM resultados_por_carrera
        WHERE race_id = %s AND finishing_position = %s AND horse_id = %s
    """
    try:
        session.execute(query, (str(race_id), int(finishing_position), str(horse_id)))
        print(f"CRUD: Registro eliminado correctamente.")
    except Exception as e:
        print(f"Error en CRUD (Eliminar): {e}")