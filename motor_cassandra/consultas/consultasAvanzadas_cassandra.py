def verRendimientoCaballo(cassandra_db, idCaballo):
    filas = cassandra_db.execute("""
        SELECT * FROM historial_por_caballo WHERE horse_id = %s
    """, (str(idCaballo),))
    resultados = list(filas)
    if not resultados:
        print("No se encontró historial para ese caballo.")
        return

    total = len(resultados)
    victorias = sum(1 for fila in resultados if fila.finishing_position == 1)
    promedio_posicion = sum(fila.finishing_position for fila in resultados) / total

    print(f"\n--- Rendimiento del caballo {idCaballo} ---")
    print(f"Carreras corridas: {total}")
    print(f"Victorias: {victorias}")
    print(f"Promedio de posición final: {promedio_posicion:.2f}")

def verRendimientoJockey(cassandra_db, nombreJockey):
    filas = cassandra_db.execute("""
        SELECT * FROM historial_por_jockey WHERE jockey = %s
    """, (str(nombreJockey),))
    resultados = list(filas)
    if not resultados:
        print("No se encontró historial para ese jockey.")
        return

    total = len(resultados)
    victorias = sum(1 for fila in resultados if fila.finishing_position == 1)
    promedio_posicion = sum(fila.finishing_position for fila in resultados) / total

    print(f"\n--- Rendimiento del jockey {nombreJockey} ---")
    print(f"Carreras corridas: {total}")
    print(f"Victorias: {victorias}")
    print(f"Promedio de posición final: {promedio_posicion:.2f}")

def verUltimasCarrerasCaballo(cassandra_db, idCaballo, limite):
    consulta = "SELECT * FROM historial_por_caballo WHERE horse_id = %s LIMIT %s"
    filas = cassandra_db.execute(consulta, (str(idCaballo), int(limite)))
    resultados = list(filas)
    if not resultados:
        print("No se encontraron carreras para ese caballo.")
        return

    print(f"\n--- Últimas {limite} carreras del caballo {idCaballo} ---")
    for fila in resultados:
        print(f"Carrera: {fila.race_id} | Posición: {fila.finishing_position} | Tiempo: {fila.finish_time}")

def verUltimasCarrerasJockey(cassandra_db, nombreJockey, limite):
    consulta = "SELECT * FROM historial_por_jockey WHERE jockey = %s LIMIT %s"
    filas = cassandra_db.execute(consulta, (str(nombreJockey), int(limite)))
    resultados = list(filas)
    if not resultados:
        print("No se encontraron carreras para ese jockey.")
        return

    print(f"\n--- Últimas {limite} carreras del jockey {nombreJockey} ---")
    for fila in resultados:
        print(f"Carrera: {fila.race_id} | Caballo: {fila.horse_name} | Posición: {fila.finishing_position}")

def verMejoresTiemposPorCarrera(cassandra_db, idCarrera):
    """Reemplaza la consulta rota original mapeando a la tabla real de mejores tiempos."""
    filas = cassandra_db.execute("""
        SELECT * FROM mejores_tiempos_por_carrera WHERE race_id = %s LIMIT 10
    """, (str(idCarrera),))
    resultados = list(filas)
    if not resultados:
        print("No se encontraron tiempos para esa carrera.")
        return

    print(f"\n--- Mejores tiempos en la carrera {idCarrera} ---")
    for fila in resultados:
        print(f"Segundos: {fila.finish_time_seconds}s | Tiempo: {fila.finish_time} | Caballo: {fila.horse_name} | Puesto: {fila.finishing_position}")