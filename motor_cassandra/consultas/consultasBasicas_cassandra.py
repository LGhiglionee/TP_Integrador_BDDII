def verResultadoCarrera(cassandra_db, idCarrera):
    # Adaptado a la tabla real: caballos_por_carrera
    filas = cassandra_db.execute("""
        SELECT * FROM caballos_por_carrera WHERE race_id = %s
    """, (str(idCarrera),))
    resultados = list(filas)
    if not resultados:
        print("No se encontraron resultados para esa carrera.")
        return

    print(f"\n--- Resultado de la carrera {idCarrera} ---")
    for fila in resultados:
        # Nota: Tu tabla no tiene la columna 'jockey', se asumen las columnas existentes
        print(f"Posición (Draw): {fila.draw} | Caballo: {fila.horse_name} | Tiempo: {fila.finish_time}")

def verGanadorCarrera(cassandra_db, idCarrera):
    filas = cassandra_db.execute("""
        CREATE INDEX IF NOT EXISTS index_finishing_position ON caballos_por_carrera (finishing_position);
        SELECT * FROM caballos_por_carrera WHERE race_id = %s AND finishing_position = 1
    """, (str(idCarrera),))
    if not filas:
        print("No se encontró ganador para esa carrera.")
        return

    print(f"\n--- Ganador de la carrera {idCarrera} ---")
    print(f"Caballo: {filas.horse_name} | Tiempo final: {filas.finish_time}")

def verTopTresCarrera(cassandra_db, idCarrera):
    # Adaptado a caballos_por_carrera con un LIMIT 3
    filas = cassandra_db.execute("""
        SELECT * FROM caballos_por_carrera WHERE race_id = %s LIMIT 3
    """, (str(idCarrera),))
    resultados = list(filas)
    if not resultados:
        print("No se encontraron resultados para esa carrera.")
        return

    print(f"\n--- Top 3 de la carrera {idCarrera} ---")
    for i, fila in enumerate(resultados, 1):
        print(f"{i}. {fila.horse_name} | Tiempo: {fila.finish_time}")

def verHistorialCaballo(cassandra_db, idCaballo):
    # Adaptado a tu tabla real: carreras_por_caballos
    filas = cassandra_db.execute("""
        SELECT * FROM carreras_por_caballos WHERE horse_id = %s
    """, (str(idCaballo),))
    resultados = list(filas)
    if not resultados:
        print("No se encontró historial para ese caballo.")
        return

    print(f"\n--- Historial del caballo {idCaballo} ---")
    for fila in resultados:
        print(f"Carrera: {fila.race_id} | Posición: {fila.finishing_position} | Tiempo: {fila.finishing_time}")

def verHistorialJockey(cassandra_db, nombreJockey):
    # Adaptado a la tabla que tiene a 'jockey' como llame primaria: entrenador_por_jockey
    # Ojo: Esta tabla en tu script no guarda el 'horse_name' ni 'race_id', solo guarda 'trainer' y 'finish_time_seconds'
    filas = cassandra_db.execute("""
        SELECT * FROM entrenador_por_jockey WHERE jockey = %s
    """, (str(nombreJockey),))
    resultados = list(filas)
    if not resultados:
        print("No se encontró historial para ese jockey.")
        return

    print(f"\n--- Historial del jockey {nombreJockey} ---")
    for fila in resultados:
        print(f"Entrenador: {fila.trainer} | Tiempo (segundos): {fila.finish_time_seconds}s")