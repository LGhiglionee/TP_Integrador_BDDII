def verResultadoCarrera(cassandra_db, idCarrera):
    filas = cassandra_db.execute("""
        SELECT *
        FROM resultados_por_carrera
        WHERE id_carrera = %s
    """, (idCarrera,))

    resultados = list(filas)

    if not resultados:
        print("No se encontraron resultados para esa carrera.")
        return

    print(f"\n--- Resultado de la carrera {idCarrera} ---")

    for fila in resultados:
        print(
            f"Posición: {fila.posicion_final} | "
            f"Caballo: {fila.nombre_caballo} | "
            f"Jockey: {fila.nombre_jockey} | "
            f"Tiempo: {fila.tiempo_final} | "
            f"Hipódromo: {fila.hipodromo}"
        )

def verGanadorCarrera(cassandra_db, idCarrera):
    filas = cassandra_db.execute("""
        SELECT *
        FROM resultados_por_carrera
        WHERE id_carrera = %s
        AND posicion_final = 1
    """, (idCarrera,))

    resultados = list(filas)

    if not resultados:
        print("No se encontró ganador para esa carrera.")
        return

    ganador = resultados[0]

    print(f"\n--- Ganador de la carrera {idCarrera} ---")
    print(f"Caballo: {ganador.nombre_caballo}")
    print(f"Jockey: {ganador.nombre_jockey}")
    print(f"Tiempo final: {ganador.tiempo_final}")

def verHistorialCaballo(cassandra_db, idCaballo):
    filas = cassandra_db.execute("""
        SELECT *
        FROM historial_por_caballo
        WHERE id_caballo = %s
    """, (idCaballo,))

    resultados = list(filas)

    if not resultados:
        print("No se encontró historial para ese caballo.")
        return

    print(f"\n--- Historial del caballo {idCaballo} ---")

    for fila in resultados:
        print(
            f"Fecha: {fila.fecha} | "
            f"Carrera: {fila.id_carrera} | "
            f"Caballo: {fila.nombre_caballo} | "
            f"Posición: {fila.posicion_final} | "
            f"Hipódromo: {fila.hipodromo}"
        )
