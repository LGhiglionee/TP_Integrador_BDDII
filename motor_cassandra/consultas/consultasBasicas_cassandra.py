def verResultadoCarrera(cassandra_db, idCarrera):
    filas = cassandra_db.execute("""
        SELECT * FROM resultados_por_carrera WHERE race_id = %s
    """, (str(idCarrera),))
    resultados = list(filas)
    if not resultados:
        print("No se encontraron resultados para esa carrera.")
        return

    print(f"\n--- Resultado de la carrera {idCarrera} ---")
    for fila in resultados:
        print(f"Posición: {fila.finishing_position} | Caballo: {fila.horse_name} | Jockey: {fila.jockey} | Tiempo: {fila.finish_time}")

def verGanadorCarrera(cassandra_db, idCarrera):
    filas = cassandra_db.execute("""
        SELECT * FROM resultados_por_carrera WHERE race_id = %s AND finishing_position = 1
    """, (str(idCarrera),))
    resultados = list(filas)
    if not resultados:
        print("No se encontró ganador para esa carrera.")
        return

    ganador = resultados[0]
    print(f"\n--- Ganador de la carrera {idCarrera} ---")
    print(f"Caballo: {ganador.horse_name} | Jockey: {ganador.jockey} | Tiempo final: {ganador.finish_time}")

def verTopTresCarrera(cassandra_db, idCarrera):
    filas = cassandra_db.execute("""
        SELECT * FROM resultados_por_carrera WHERE race_id = %s LIMIT 3
    """, (str(idCarrera),))
    resultados = list(filas)
    if not resultados:
        print("No se encontraron resultados para esa carrera.")
        return

    print(f"\n--- Top 3 de la carrera {idCarrera} ---")
    for fila in resultados:
        print(f"{fila.finishing_position}. {fila.horse_name} | Jockey: {fila.jockey} | Tiempo: {fila.finish_time}")

def verHistorialCaballo(cassandra_db, idCaballo):
    filas = cassandra_db.execute("""
        SELECT * FROM historial_por_caballo WHERE horse_id = %s
    """, (str(idCaballo),))
    resultados = list(filas)
    if not resultados:
        print("No se encontró historial para ese caballo.")
        return

    print(f"\n--- Historial del caballo {idCaballo} ---")
    for fila in resultados:
        print(f"Carrera: {fila.race_id} | Posición: {fila.finishing_position} | Tiempo: {fila.finish_time}")

def verHistorialJockey(cassandra_db, nombreJockey):
    filas = cassandra_db.execute("""
        SELECT * FROM historial_por_jockey WHERE jockey = %s
    """, (str(nombreJockey),))
    resultados = list(filas)
    if not resultados:
        print("No se encontró historial para ese jockey.")
        return

    print(f"\n--- Historial del jockey {nombreJockey} ---")
    for fila in resultados:
        print(f"Carrera: {fila.race_id} | Caballo: {fila.horse_name} | Posición: {fila.finishing_position}")