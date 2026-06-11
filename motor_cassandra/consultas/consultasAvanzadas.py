def verTopTresCarrera(cassandra_db, idCarrera):
    filas = cassandra_db.execute("""
        SELECT *
        FROM resultados_por_carrera
        WHERE id_carrera = %s
        LIMIT 3
    """, (idCarrera,))

    resultados = list(filas)

    if not resultados:
        print("No se encontraron resultados para esa carrera.")
        return

    print(f"\n--- Top 3 de la carrera {idCarrera} ---")

    for fila in resultados:
        print(
            f"{fila.posicion_final}. "
            f"{fila.nombre_caballo} | "
            f"Jockey: {fila.nombre_jockey} | "
            f"Tiempo: {fila.tiempo_final}"
        )

def verMejoresTiempos(cassandra_db, distancia, superficie):
    filas = cassandra_db.execute("""
        SELECT *
        FROM mejores_tiempos_distancia
        WHERE distancia = %s
        AND superficie = %s
        LIMIT 10
    """, (distancia, superficie))

    resultados = list(filas)

    if not resultados:
        print("No se encontraron tiempos para esa distancia y superficie.")
        return

    print(f"\n--- Mejores tiempos en {distancia}m sobre {superficie} ---")

    for fila in resultados:
        print(
            f"Tiempo: {fila.tiempo_final} | "
            f"Caballo: {fila.nombre_caballo} | "
            f"Carrera: {fila.id_carrera} | "
            f"Fecha: {fila.fecha} | "
            f"Hipódromo: {fila.hipodromo}"
        )

def verUltimasCarrerasCaballo(cassandra_db, idCaballo, limite):
    consulta = f"""
        SELECT *
        FROM historial_por_caballo
        WHERE id_caballo = %s
        LIMIT {int(limite)}
    """

    filas = cassandra_db.execute(consulta, (idCaballo,))
    resultados = list(filas)

    if not resultados:
        print("No se encontraron carreras para ese caballo.")
        return

    print(f"\n--- Últimas {limite} carreras del caballo {idCaballo} ---")

    for fila in resultados:
        print(
            f"Fecha: {fila.fecha} | "
            f"Carrera: {fila.id_carrera} | "
            f"Posición: {fila.posicion_final} | "
            f"Hipódromo: {fila.hipodromo}"
        )