"""
Módulo de operaciones CRUD (Create, Read, Update, Delete) para Apache Cassandra.
Implementa mutaciones atómicas y lecturas directas por clave primaria completa,
optimizando el rendimiento a través de sentencias precompiladas
y minimizando la latencia de coordinación en el anillo distribuido.
"""
def crear_resultado_manual(session, race_id, finishing_position, horse_id, horse_number, horse_name, finish_time):
    """
    Operación CREATE: Inserción directa en una fila ancha (Wide Row).
    Esto permite validar los tipos de datos en el cliente y serializar los parámetros de forma eficiente,
    evitando inyecciones y reduciendo el procesamiento sintáctico en escrituras consecutivas.
    """
    query = """
        INSERT INTO caballos_por_carrera (
            race_id, finishing_position, horse_id, horse_number, horse_name, 
            finish_time
        ) VALUES (?, ?, ?, ?, ?, ?)
    """
    try:
        preparado = session.prepare(query)
        session.execute(preparado, [
            str(race_id), int(finishing_position), str(horse_id),
            int(horse_number), str(horse_name), 
            str(finish_time)
        ])
        print(f"Resultado creado para el caballo {horse_name} en la carrera {race_id}.")
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
        SELECT * FROM caballos_por_carrera 
        WHERE race_id = %s AND finishing_position = %s AND horse_id = %s ALLOW FILTERING
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
        print(f"Tiempo: {r.finish_time}")
        return r
    except Exception as e:
        print(f"Error en CRUD (Leer): {e}")
        return None

def actualizar_tiempo_resultado(session, race_id, finishing_position, horse_id, nuevo_time):
    """
    Operación UPDATE con validación a nivel de aplicación (Read-Before-Write).
    Como horse_id no es Clave Primaria, Cassandra no permite filtrarlo en el WHERE de un UPDATE.
    Primero validamos que el horse_id coincida, y luego ejecutamos la mutación.
    """
    try:
        query_verificar = "SELECT horse_id FROM caballos_por_carrera WHERE race_id = %s AND finishing_position = %s"
        resultado = session.execute(query_verificar, (str(race_id), int(finishing_position))).one()

        if not resultado:
            print(f"Error: No se encontró la carrera {race_id} con la posición {finishing_position}.")
            return
        
        if resultado.horse_id != str(horse_id):
            print(f"Error de seguridad: El caballo en la posición {finishing_position} es '{resultado.horse_id}', no '{horse_id}'. Actualización bloqueada.")
            return
        
        query_act = """
            UPDATE caballos_por_carrera
            SET finish_time = ?
            WHERE race_id = ? AND finishing_position = ?
        """
        preparado = session.prepare(query_act)
        session.execute(preparado, [str(nuevo_time), str(race_id), int(finishing_position)])
        print(f"Tiempo actualizado con éxito para el caballo {horse_id} en la carrera {race_id}.")

    except Exception as e:
        print(f"Error en CRUD (Actualizar): {e}")


def eliminar_resultado_especifico(session, race_id, finishing_position, horse_id):
    """
    Operación DELETE con validación a nivel de aplicación (Read-Before-Write).
    Misma lógica que el UPDATE: validamos el dato no-clave antes de generar el Tombstone.
    """
    try:
        query_verificar = "SELECT horse_id FROM caballos_por_carrera WHERE race_id = %s AND finishing_position = %s"
        resultado = session.execute(query_verificar, (str(race_id), int(finishing_position))).one()

        if not resultado:
            print(f"Error: No se encontró la carrera {race_id} con la posición {finishing_position}.")
            return
        
        if resultado.horse_id != str(horse_id):
            print(f"Error de seguridad: El caballo en la posición {finishing_position} es '{resultado.horse_id}', no '{horse_id}'. Borrado bloqueado.")
            return
        
        query_borrar = """
            DELETE FROM caballos_por_carrera
            WHERE race_id = %s AND finishing_position = %s
        """
        session.execute(query_borrar, (str(race_id), int(finishing_position)))
        print(f"CRUD: Registro del caballo {horse_id} eliminado correctamente.")

    except Exception as e:
        print(f"Error en CRUD (Eliminar): {e}")