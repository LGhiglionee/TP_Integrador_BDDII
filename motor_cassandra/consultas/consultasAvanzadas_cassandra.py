"""
Módulo de consultas analíticas e históricas para Apache Cassandra.
Implementa el acceso a datos bajo la metodología de Diseño Orientado a Consultas
, ejecutando búsquedas directas sobre claves de partición
para garantizar lecturas optimizadas de tiempo constante O(1).
"""
def verRendimientoCaballo(cassandra_db, idCaballo):
    """
    Recupera métricas consolidadas de rendimiento.
    Realiza un Key-Lookup exacto sobre la Partition Key (horse_id), lo que permite
    al coordinador redirigir la query al nodo específico del anillo sin escaneos distribuidos.
    """
    filas = cassandra_db.execute("""
        SELECT * FROM rendimiento_caballo WHERE horse_id = %s
    """, (str(idCaballo),))
    resultados = list(filas)
    
    if not resultados:
        print(f"No se encontraron registros en 'rendimiento_caballo' para el ID: {idCaballo}")
        return

    print(f"\n--- Datos de la tabla rendimiento_caballo (ID: {idCaballo}) ---")
    for fila in resultados:
        print(f"Caballo: {fila.horse_name} | Carreras corridas: {fila.carreras_corridas} | Victorias: {fila.victorias} | Posición promedio: {fila.promedio_posicion}")


def verJockeyPorPosicionFinalDelCaballo(cassandra_db, idCaballo):
    """
    Consulta sobre filas anchas (Wide Rows).
    Busca por la Partition Key (horse_id). Los registros devueltos se leen de forma
    secuencial directa desde la SSTable en disco, aprovechando la ordenación física predefinida.
    """
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
    """
    Búsqueda desnormalizada por actor.
    Esta tabla fue creada específicamente para responder este patrón de acceso,
    utilizando al 'jockey' como la Partition Key obligatoria para la cláusula WHERE.
    """
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
    """
    Consulta compuesta sobre Clave Primaria.
    Para que Cassandra responda sin lanzar una excepción de rendimiento, la query provista
    incluye todos los componentes lógicos de la clave de partición (jockey Y trainer).
    """
    filas = cassandra_db.execute("""
        SELECT * FROM tiempo_promedio_por_dupla WHERE jockey = %s AND trainer = %s
    """, (str(nombreJockey), str(nombreTrainer)))
    resultados = list(filas)
    
    if not resultados:
        print(f"No se encontraron registros en 'tiempo_promedio_por_dupla' para la dupla: {nombreJockey} - {nombreTrainer}")
        return

    print(f"\n--- Datos de la tabla tiempo_promedio_por_dupla (Dupla: {nombreJockey} / {nombreTrainer}) ---")
    for fila in resultados:
        print(f"Jockey: {fila.jockey} | Trainer: {fila.trainer} | Tiempo Promedio: {fila.promedio_tiempo_final} | Time Seconds: {fila.finish_time_seconds}s")

def verCaballos(cassandra_db, idCaballo):
    """
    Escaneo de Tabla Dispersa (Sparse Table).
    Recupera el conjunto global de entidades. Nota de rendimiento: En entornos de producción masivos,
    un SELECT sin WHERE (Full Cluster Scan) debe ser evitado o controlado mediante paginación.
    """
    filas = cassandra_db.execute("""
        SELECT * FROM caballos
    """)
    resultados = list(filas)

    if not resultados:
        print(f"No se encontraron registros en 'caballos'")
        return

    print(f"\n--- Datos de la tabla caballos ---")
    for fila in resultados:
        print(f"Nombre: {fila.horse_name} | Numero: {fila.horse_number} | Peso: {fila.declared_horse_weight} | Id: {fila.horse_id}")