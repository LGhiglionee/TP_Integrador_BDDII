def verRendimientoCaballo(cassandra_db, idCaballo):
    filas = cassandra_db.execute("""
        SELECT * FROM rendimiento_caballo WHERE horse_id = %s
    """, (str(idCaballo),))
    resultados = list(filas)
    
    if not resultados:
        print(f"No se encontraron registros en 'rendimiento_caballo' para el ID: {idCaballo}")
        return

    print(f"\n--- Datos de la tabla rendimiento_caballo (ID: {idCaballo}) ---")
    for fila in resultados:
        print(f"Horse ID: {fila.horse_id} | Carreras Corridas: {fila.carreras_corridas} | Victorias: {fila.victorias} | Promedio Posición: {fila.promedio_posicion}")


def verJockeyPorPosicionFinalDelCaballo(cassandra_db, idCaballo):
    # Hace SELECT a la tabla jockey_por_posicion_final_del_caballo
    filas = cassandra_db.execute("""
        SELECT * FROM jockey_por_posicion_final_del_caballo WHERE horse_id = %s
    """, (str(idCaballo),))
    resultados = list(filas)
    
    if not resultados:
        print(f"No se encontraron registros en 'jockey_por_posicion_final_del_caballo' para el ID de caballo: {idCaballo}")
        return

    print(f"\n--- Datos de la tabla jockey_por_posicion_final_del_caballo (Caballo: {idCaballo}) ---")
    for fila in resultados:
        print(f"Horse ID: {fila.horse_id} | Position: {fila.finishing_position} | Time Seconds: {fila.finish_time_seconds}s | Jockey: {fila.jockey} | Diferencia: {fila.diferencia} | Draw: {fila.draw}")


def verEntrenadorPorJockey(cassandra_db, nombreJockey):
    # Hace SELECT a la tabla entrenador_por_jockey
    filas = cassandra_db.execute("""
        SELECT * FROM entrenador_por_jockey WHERE jockey = %s
    """, (str(nombreJockey),))
    resultados = list(filas)
    
    if not resultados:
        print(f"No se encontraron registros en 'entrenador_por_jockey' para el jockey: {nombreJockey}")
        return

    print(f"\n--- Datos de la tabla entrenador_por_jockey (Jockey: {nombreJockey}) ---")
    for fila in resultados:
        print(f"Jockey: {fila.jockey} | Time Seconds: {fila.finish_time_seconds}s | Trainer: {fila.trainer}")


def verTiempoPromedioPorDupla(cassandra_db, nombreJockey, nombreTrainer):
    # Hace SELECT a la tabla tiempo_promedio_por_dupla usando la llave primaria compuesta (jockey, trainer)
    filas = cassandra_db.execute("""
        SELECT * FROM tiempo_promedio_por_dupla WHERE jockey = %s AND trainer = %s
    """, (str(nombreJockey), str(nombreTrainer)))
    resultados = list(filas)
    
    if not resultados:
        print(f"No se encontraron registros en 'tiempo_promedio_por_dupla' para la dupla: {nombreJockey} - {nombreTrainer}")
        return

    print(f"\n--- Datos de la tabla tiempo_promedio_por_dupla (Dupla: {nombreJockey} / {nombreTrainer}) ---")
    for fila in resultados:
        print(f"Jockey: {fila.jockey} | Trainer: {fila.trainer} | Promedio Tiempo: {fila.promedio_tiempo_final} | Time Seconds: {fila.finish_time_seconds}s")