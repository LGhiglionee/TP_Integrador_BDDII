"""
Módulo de consultas operacionales y de visualización para Apache Cassandra.
Proporciona métodos optimizados para la extracción de resultados en tiempo real
y el seguimiento de historiales, consolidando el paradigma de tablas anchas
(Wide Rows) orientadas estrictamente a los patrones de acceso de la interfaz.
"""
def verResultadoCarrera(cassandra_db, idCarrera):
    """
    Recupera la partición completa de una carrera específica.
    La consulta utiliza la Partition Key 'race_id' sobre la tabla 'caballos_por_carrera',
    lo que permite al nodo coordinador localizar la fila ancha en disco de manera directa
    y transmitir secuencialmente los datos de los participantes.
    """
    filas = cassandra_db.execute("""
        SELECT * FROM caballos_por_carrera WHERE race_id = %s
    """, (str(idCarrera),))
    resultados = list(filas)
    if not resultados:
        print("No se encontraron resultados para esa carrera.")
        return

    print(f"\n--- Resultado de la carrera {idCarrera} ---")
    for fila in resultados:
        print(f"Posición (Draw): {fila.draw} | Caballo: {fila.horse_name} | Tiempo: {fila.finish_time} | Posición final: {fila.finishing_position}")

def verGanadorCarrera(cassandra_db, idCarrera):
    """
    Extracción optimizada del primer puesto.
    Filtra por la Partition Key ('race_id') y la Clustering Key ('finishing_position').
    Al estar indexada y ordenada físicamente en disco de forma ascendente, esta búsqueda
    no escanea la partición, sino que accede directamente al primer registro de la SSTable.
    """
    filas = cassandra_db.execute("""
        SELECT * FROM caballos_por_carrera WHERE race_id = %s AND finishing_position = 1
    """, (str(idCarrera),))
    resultado = filas.one()

    if not resultado:
        print("No se encontró ganador para esa carrera.")
        return

    print(f"\n--- Ganador de la carrera {idCarrera} ---")
    print(f"Caballo: {resultado.horse_name} | Tiempo final: {resultado.finish_time}")

def verTopTresCarrera(cassandra_db, idCarrera):
    """
    Acotación nativa del flujo de datos en disco.
    Aprovecha la ordenación por clúster nativa de 'caballos_por_carrera'. Al aplicar
    la directiva 'LIMIT 3', Cassandra interrumpe la lectura secuencial en la SSTable
    apenas procesa los primeros tres registros, minimizando el I/O de disco y el tráfico de red.
    """
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
    """
    Consulta de serie temporal sobre la tabla materializada 'carreras_por_caballos'.
    En lugar de realizar costosos filtrados secundarios, se utiliza una tabla desnormalizada
    donde 'horse_id' es la Partition Key, garantizando que el historial cronológico completo
    del ejemplar se recupere en una sola operación atómica de lectura.
    """
    filas = cassandra_db.execute("""
        SELECT * FROM carreras_por_caballos WHERE horse_id = %s
    """, (str(idCaballo),))
    resultados = list(filas)
    if not resultados:
        print("No se encontró historial para ese caballo.")
        return

    print(f"\n--- Historial del caballo {idCaballo} ---")
    for fila in resultados:
        print(f"Caballo: {fila.horse_name} | Carrera: {fila.race_id} | Posición: {fila.finishing_position} | Tiempo: {fila.finishing_time}")

def verHistorialJockey(cassandra_db, nombreJockey):
    """
    Recuperación de perfiles profesionales por clave de fila.
    Mapea el patrón de acceso sobre la estructura desnormalizada 'entrenador_por_jockey'.
    Resuelve la consulta de manera local en el nodo réplica correspondiente al hash
    del nombre del jockey provisto.
    """
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