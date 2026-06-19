"""
Módulo de operaciones CRUD (Create, Read, Update, Delete) para Apache Cassandra.
Implementa mutaciones atómicas y lecturas directas por clave primaria completa,
optimizando el rendimiento a través de sentencias precompiladas (Prepared Statements)
y minimizando la latencia de coordinación en el anillo distribuido.
"""
def crear_resultado_manual(session, race_id, finishing_position, horse_id, horse_number, horse_name, jockey, trainer, finish_time, finish_time_seconds):
    """
    Operación CREATE: Inserción directa en una fila ancha (Wide Row).
    Esto permite validar los tipos de datos en el cliente y serializar los parámetros de forma eficiente,
    evitando inyecciones y reduciendo el procesamiento sintáctico en escrituras consecutivas.
    """
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
    """
    Operación READ: Búsqueda puntual por Clave Primaria completa.
    Al incluir de manera exacta en el WHERE tanto la Partition Key (race_id) como las
    Clustering Keys (finishing_position, horse_id), la consulta se resuelve con complejidad O(1).
    El coordinador determina instantáneamente el nodo réplica exacto que almacena la fila,
    obteniendo el dato sin escanear ninguna otra partición del clúster.
    """
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
    """
    Operación UPDATE: Mutación de atributos no-clave
    En Cassandra, UPDATE e INSERT comparten la misma lógica interna. Si la clave primaria
    especificada en el WHERE ya existe, el motor pisa los campos indicados guardando un nuevo timestamp.
    Si la clave no existiera, crearía una nueva fila de forma automática sin lanzar errores.
    """
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
    """
    Operación DELETE: Eliminación lógica mediante Tombstones.
    Debido a que los archivos SSTables en disco son inmutables, Cassandra no sobreescribe ni borra
    físicamente el registro en caliente. En su lugar, esta operación escribe un marcador lógico (Tombstone)
    que oculta el registro en las lecturas. El dato se purgará definitivamente del disco durante el proceso
    posterior de compactación de archivos.
    """
    query = """
        DELETE FROM resultados_por_carrera
        WHERE race_id = %s AND finishing_position = %s AND horse_id = %s
    """
    try:
        session.execute(query, (str(race_id), int(finishing_position), str(horse_id)))
        print(f"CRUD: Registro eliminado correctamente.")
    except Exception as e:
        print(f"Error en CRUD (Eliminar): {e}")