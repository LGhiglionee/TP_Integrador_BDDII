"""
Módulo de operaciones CRUD para Neo4j.
Gestiona la creación, lectura y borrado de nodos y relaciones, asegurando que
el grafo mantenga su coherencia estructural mediante el uso de MERGE y DETACH DELETE.
"""
def buscar_participacion_caballo(session, horse_id, race_id):
    """
    Lee un patrón específico en el grafo: la existencia de una relación
    [:CORRIO] entre un nodo Caballo y un nodo Carrera.
    """
    query = """
    MATCH (c:Caballo {id: $horse_id})-[r:CORRIO]->(race:Carrera {id: $race_id})
    RETURN c.nombre AS nombre, race.id AS carrera_id
    """
    return session.run(query, horse_id=horse_id, race_id=race_id).single()

def insertar_registro_carrera(session, datos):
    """
    Operación 'Upsert' (Update o Insert):
    Crea o actualiza nodos y relaciones de forma atómica. Si el caballo, entrenador o jockey no existen, los crea.
    """
    datos_limpios = preparar_datos(datos)

    query = """
    MERGE (c:Caballo {id: $horse_id})
    SET c.nombre = $horse_name,
        c.numero = $horse_number

    MERGE (race:Carrera {id: $race_id})
    MERGE (e:Entrenador {nombre: $trainer})
    MERGE (j:Jockey {nombre: $jockey})

    // Creación de la arista (relación) principal con sus propiedades de métrica
    MERGE (c)-[r:CORRIO]->(race)
    SET r.posicion = $finishing_position,
        r.peso_actual = $actual_weight,
        r.peso_declarado = $declared_horse_weight,
        r.sorteo = $draw,
        r.posicion_1 = $running_position_1,
        r.posicion_2 = $running_position_2,
        r.posicion_3 = $running_position_3,
        r.tiempo = $finish_time,
        r.tiempo_segundos = $finish_time_seconds
    
    // Creación de relaciones de linaje (genealogía)
    MERGE (p:Caballo {nombre: $father})
    MERGE (c)-[:HIJO_DE]->(p)

    MERGE (m:Caballo {nombre: $mother})
    MERGE (c)-[:HIJO_DE]->(m)

    MERGE (ab:Caballo {nombre: $gfather})
    MERGE (c)-[:NIETO_DE]->(ab)

    MERGE (c)-[:ENTRENADO_POR]->(e)
    MERGE (c)-[:MONTADO_POR]->(j)

    RETURN c.id AS horse_id, c.nombre AS horse_name, race.id AS race_id
    """

    return session.run(query, **datos_limpios).single()

def borrar_caballo_carrera_especifica(session, horse_id, race_id):
    """
    Borrado específico: Elimina únicamente la arista [:CORRIO] entre un caballo
    y una carrera, preservando la existencia de ambos nodos.
    """
    query = """
    MATCH (c:Caballo {id: $horse_id})-[r:CORRIO]->(race:Carrera {id: $race_id})
    WITH c, race, r, c.nombre AS nombre_caballo
    DELETE r
    RETURN count(r) AS deleted_count, nombre_caballo AS nombre, race.id AS carrera_id
    """

    return session.run(query, horse_id=horse_id, race_id=race_id).single()

def borrar_caballo_completo(session, horse_id):
    """
    Borrado en cascada: Usa 'DETACH DELETE' para eliminar el nodo Caballo
    junto con todas sus relaciones asociadas (si no se usa DETACH,
    Neo4j arrojaría error al intentar borrar nodos con relaciones).
    """
    query = """
    MATCH (c:Caballo {id: $horse_id})
    WITH c, c.nombre AS nombre_caballo
    DETACH DELETE c
    RETURN count(c) AS deleted_count, nombre_caballo AS nombre
    """

    return session.run(query, horse_id=horse_id).single()

def preparar_datos(datos):
    """
    Capa de abstracción: Normaliza los inputs del usuario (limpieza de espacios,
    tipado de números) antes de enviarlos al motor.
    """
    return {
        "horse_id": limpiar_texto(datos.get("horse_id")),
        "horse_name": limpiar_texto(datos.get("horse_name")),
        "race_id": limpiar_texto(datos.get("race_id")),

        "jockey": limpiar_texto(datos.get("jockey")) or "Desconocido",
        "trainer": limpiar_texto(datos.get("trainer")) or "Desconocido",

        "father": limpiar_texto(datos.get("father")) or "Desconocido",
        "mother": limpiar_texto(datos.get("mother")) or "Desconocida",
        "gfather": limpiar_texto(datos.get("gfather")) or "Desconocido",

        "finishing_position": convertir_int(datos.get("finishing_position")),
        "horse_number": convertir_int(datos.get("horse_number")),
        "actual_weight": convertir_int(datos.get("actual_weight")),
        "declared_horse_weight": convertir_int(datos.get("declared_horse_weight")),
        "draw": convertir_int(datos.get("draw")),
        "running_position_1": convertir_int(datos.get("running_position_1")),
        "running_position_2": convertir_int(datos.get("running_position_2")),
        "running_position_3": convertir_int(datos.get("running_position_3")),

        "finish_time": limpiar_texto(datos.get("finish_time")),
        "finish_time_seconds": convertir_float(datos.get("finish_time_seconds")),
    }


def limpiar_texto(valor):
    if valor is None:
        return None
    valor = str(valor).strip()

    if valor == "":
        return None

    return valor

def convertir_int(valor):
    try:
        if valor is None or str(valor).strip() == "":
            return None
        return int(valor)

    except:
        return None

def convertir_float(valor):
    try:
        if valor is None or str(valor).strip() == "":
            return None
        return float(str(valor).replace(",", "."))

    except:
        return None