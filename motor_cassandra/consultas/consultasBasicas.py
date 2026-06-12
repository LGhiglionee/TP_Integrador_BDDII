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

def verHistorialJockey(cassandra_db, idJockey):
    filas = cassandra_db.execute("""
        SELECT *
        FROM historial_por_jockey
        WHERE id_jockey = %s
    """, (idJockey,))

    resultados = list(filas)

    if not resultados:
        print("No se encontró historial para ese jockey.")
        return

    print(f"\n--- Historial del jockey {idJockey} ---")

    for fila in resultados:
        print(
            f"Fecha: {fila.fecha} | "
            f"Carrera: {fila.id_carrera} | "
            f"Caballo: {fila.nombre_caballo} | "
            f"Posición: {fila.posicion_final} | "
            f"Hipódromo: {fila.hipodromo}"
        )
        

def verCarrerasPorFecha(cassandra_db, fecha):
    filas = cassandra_db.execute("""
        SELECT *
        FROM carreras_por_fecha
        WHERE fecha = %s
    """, (fecha,))

    resultados = list(filas)

    if not resultados:
        print("No se encontraron carreras para esa fecha.")
        return

    print(f"\n--- Carreras del día {fecha} ---")

    for fila in resultados:
        print(
            f"Carrera: {fila.id_carrera} | "
            f"Hipódromo: {fila.hipodromo} | "
            f"Distancia: {fila.distancia} | "
            f"Superficie: {fila.superficie} | "
            f"Participantes: {fila.cantidad_participantes}"
        )
        
        
def verCarrerasPorHipodromo(cassandra_db, hipodromo):
    filas = cassandra_db.execute("""
        SELECT *
        FROM carreras_por_hipodromo
        WHERE hipodromo = %s
    """, (hipodromo,))

    resultados = list(filas)

    if not resultados:
        print("No se encontraron carreras para ese hipódromo.")
        return

    print(f"\n--- Carreras en {hipodromo} ---")

    for fila in resultados:
        print(
            f"Fecha: {fila.fecha} | "
            f"Carrera: {fila.id_carrera} | "
            f"Distancia: {fila.distancia} | "
            f"Superficie: {fila.superficie} | "
            f"Participantes: {fila.cantidad_participantes}"
        )