"""
Módulo de consultas analíticas para Neo4j (Cypher).
Utiliza el motor de grafos para navegar linaje, patrones de entrenamiento y
comportamiento genealógico mediante recorridos profundos.
"""
def buscar_caballo_nombre(session, nombre):
    """
    Navega la relación direccional [:CORRIO] entre nodos Caballo y Carrera.
    """
    try:
        nombre = nombre.upper().strip()
        query = """
        MATCH (c:Caballo)-[r:CORRIO]->(race:Carrera)
        WHERE toUpper(c.nombre) = $nombre_caballo
        RETURN 
            c.nombre AS nombre, r.posicion AS posicion, race.id AS carrera_id
        ORDER BY race.id
        """

        resultados = list(session.run(query, nombre_caballo=nombre))
        if not resultados:
            print(f"No se encontraron registros para el caballo: {nombre}")
        else:
            print("=== HISTORIAL DE POSICIÓN ===")
            for r in resultados:
                print(f"Caballo: {r['nombre']} | Carrera: {r['carrera_id']} | Posición: {r['posicion']}")

    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")

def recomendacion_entrenador_matchmaking(session, nombre):
    """
    Análisis de Linaje: Utiliza recorridos multihop para encontrar hermanos (mismo progenitor)
    y evaluar la eficiencia del entrenador ([:ENTRENADO_POR]) en ese grupo familiar.
    """
    try:
        nombre = nombre.upper().strip()
        query = """
        MATCH (c:Caballo)-[:HIJO_DE]->(progenitor:Caballo)
        WHERE toUpper(c.nombre) = $nombre_caballoAND progenitor.nombre IS NOT NULLAND progenitor.nombre <> 'Desconocido'AND progenitor.nombre <> 'Desconocida'

        MATCH (progenitor)<-[:HIJO_DE]-(hermano:Caballo)-[:ENTRENADO_POR]->(e:Entrenador)
        WHERE e.nombre <> 'Desconocido'
          AND hermano <> c
          AND EXISTS {
              MATCH (hermano)-[:CORRIO]->(:Carrera)
          }

        WITH e, count(DISTINCT hermano) AS hermanos_entrenados

        RETURN 
            e.nombre AS entrenador, hermanos_entrenados
        ORDER BY hermanos_entrenados DESC
        LIMIT 1
        """

        resultados = list(session.run(query, nombre_caballo=nombre))
        if not resultados:
            print(f"No hay suficiente historial familiar o linaje cargado para recomendar un entrenador a {nombre}.")
        else:
            print("=== SISTEMA DE RECOMENDACIÓN DE ENTRENADORES ===")
            for r in resultados:
                print(f"Para el caballo '{nombre}':")
                print(f"Te recomendamos al entrenador: {r['entrenador']}")
                print(f"Debido a que ya entrenó a {r['hermanos_entrenados']} hermanos de la misma familia genética.")

    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")

def caballos_similares_diamante(session, nombre):
    """
    Patrón de Diamante: Identifica sub-grafos donde dos caballos comparten
    un ancestro común (abuelo) y un mismo entrenador.
    """
    try:
        nombre = nombre.upper().strip()

        query = """
        MATCH (c1:Caballo)-[:NIETO_DE]->(abuelo:Caballo)
        MATCH (c1)-[:ENTRENADO_POR]->(e:Entrenador)
        WHERE toUpper(c1.nombre) = $nombre_caballoAND abuelo.nombre IS NOT NULLAND abuelo.nombre <> 'Desconocido'AND abuelo.nombre <> 'Desconocida'AND e.nombre <> 'Desconocido'

        MATCH (c2:Caballo)-[:NIETO_DE]->(abuelo)
        MATCH (c2)-[:ENTRENADO_POR]->(e)
        MATCH (c2)-[:CORRIO]->(:Carrera)
        WHERE c1 <> c2
          AND c2.nombre IS NOT NULL
          AND c2.nombre <> 'Desconocido'
          AND c2.nombre <> 'Desconocida'

        RETURN DISTINCT 
            c2.nombre AS similar, abuelo.nombre AS abuelo, e.nombre AS entrenador
        ORDER BY c2.nombre
        LIMIT 30
        """

        resultados = list(session.run(query, nombre_caballo=nombre))
        if not resultados:
            print(f"No se encontraron patrones de diamante o caballos similares para: {nombre}")
        else:
            print("=== PATRÓN DE DIAMANTE (CABALLOS SIMILARES DE LINAJE) ===")
            print(f"Caballos con características similares a '{nombre}':")
            for r in resultados:
                print(f" Caballo: {r['similar']}")
                print(f" Comparten el abuelo: {r['abuelo']}")
                print(f" Comparten el mismo entrenador: {r['entrenador']}\n")

    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")

def recomendacion_apuestas_linaje(session, nombre):
    """
    Análisis estadístico sobre grafos: Calcula el éxito de un linaje
    directo para predecir probabilidades de nuevos ejemplares.
    """
    try:
        nombre = nombre.upper().strip()

        query = """
        MATCH (c:Caballo)-[:HIJO_DE]->(padre:Caballo)
        WHERE toUpper(c.nombre) = $nombre_caballo
          AND padre.nombre IS NOT NULL
          AND padre.nombre <> 'Desconocido'
          AND padre.nombre <> 'Desconocida'

        MATCH (padre)<-[:HIJO_DE]-(hijo_ganador:Caballo)-[r:CORRIO]->(:Carrera)
        WHERE r.posicion = 1

        WITH padre, count(r) AS victorias_familiares, c

        MATCH (padre)<-[:HIJO_DE]-(caballo_sugerido:Caballo)-[r2:CORRIO]->(:Carrera)
        WHERE caballo_sugerido <> c
          AND caballo_sugerido.nombre IS NOT NULL
          AND caballo_sugerido.nombre <> 'Desconocido'
          AND caballo_sugerido.nombre <> 'Desconocida'
          AND r2.posicion <> 1

        RETURN DISTINCT 
            caballo_sugerido.nombre AS sugerido, padre.nombre AS padre, victorias_familiares
        ORDER BY victorias_familiares DESC, caballo_sugerido.nombre
        LIMIT 3
        """

        resultados = list(session.run(query, nombre_caballo=nombre))
        if not resultados:
            print(f"La familia directa de {nombre} no registra un linaje estadísticamente ganador para apuestas.")
        else:
            print("=== MOTOR DE RECOMENDACIÓN DE APUESTAS GENÉTICAS ===")
            print(f"Analizando la sangre de '{nombre}'")

            padre = resultados[0]["padre"]
            victorias = resultados[0]["victorias_familiares"]

            print("")
            print(f"Linaje exitoso detectado: {padre}")
            print(f"Victorias de la familia en carreras: {victorias}")

            print("")
            print("Apuestas sugeridas:")

            for r in resultados:
                print(f"- {r['sugerido']}")

    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")

def linea_sangre_caballo(session, nombre):
    """
    Consulta de profundidad: Utiliza OPTIONAL MATCH para extraer una ficha
    genealógica completa, navegando nodos de padres y abuelos.
    """
    try:
        nombre = nombre.upper().strip()

        query = """
        MATCH (c:Caballo)
        WHERE toUpper(c.nombre) = $nombre_caballo

        OPTIONAL MATCH (c)-[:HIJO_DE]->(progenitor:Caballo)
        OPTIONAL MATCH (c)-[:NIETO_DE]->(abuelo:Caballo)
        OPTIONAL MATCH (c)-[r:CORRIO]->(:Carrera)

        RETURN 
            c.nombre AS analizado, 
            collect(DISTINCT r.posicion) AS posiciones, 
            collect(DISTINCT progenitor.nombre) AS padres, 
            collect(DISTINCT abuelo.nombre) AS abuelos
        """

        resultados = list(session.run(query, nombre_caballo=nombre))
        if not resultados:
            print(f"No se encontró información para: {nombre}")
        else:
            print("=== ANÁLISIS DE ÁRBOL GENEALÓGICO ===")
            for r in resultados:
                posiciones = [str(p) for p in r["posiciones"] if p is not None]

                padres = [
                    p for p in r["padres"]
                    if p is not None and p not in ["Desconocido", "Desconocida"]
                ]

                abuelos = [
                    a for a in r["abuelos"]
                    if a is not None and a not in ["Desconocido", "Desconocida"]
                ]

                print(f"Ficha Técnica: {r['analizado']}")
                print(f"Posiciones obtenidas: {', '.join(posiciones) if posiciones else 'Sin posiciones cargadas'}")
                print(f"Padres: {', '.join(padres) if padres else 'Sin padres cargados'}")
                print(f"Abuelos: {', '.join(abuelos) if abuelos else 'Sin abuelos cargados'}")

    except Exception as e:
        print(f"Error en la consulta: {e}")

def ranking_entrenadores_por_linaje(session, nombre_padre):
    """
    Agregación sobre relaciones: Calcula promedios matemáticos (avg)
    sobre las propiedades de las aristas (r.posicion) agrupadas por un nodo entidad (Entrenador).
    """
    try:
        nombre_padre = nombre_padre.upper().strip()

        query = """
        MATCH (progenitor:Caballo)<-[:HIJO_DE]-(hijo:Caballo)
        WHERE toUpper(progenitor.nombre) = $nombre_padre

        MATCH (hijo)-[r:CORRIO]->(:Carrera)
        MATCH (hijo)-[:ENTRENADO_POR]->(e:Entrenador)

        WHERE e.nombre <> 'Desconocido'

        WITH 
            e, 
            avg(r.posicion) AS promedio_posicion, 
            count(DISTINCT hijo) AS cantidad_caballos,
            count(r) AS cantidad_carreras

        RETURN 
            e.nombre AS entrenador, promedio_posicion, cantidad_caballos,cantidad_carreras

        ORDER BY promedio_posicion ASC
        """

        resultados = list(session.run(query, nombre_padre=nombre_padre))
        if not resultados:
            print(f"No hay registros suficientes para '{nombre_padre}'.")
        else:
            print(f"RANKING: ¿Quién entrena mejor a los hijos de '{nombre_padre}'? ===")
            for r in resultados:
                print(
                    f"Entrenador: {r['entrenador']} | "
                    f"Promedio de llegada (Posicion): {r['promedio_posicion']:.2f} | "
                    f"Caballos analizados: {r['cantidad_caballos']}"
                )

    except Exception as e:
        print(f"Error: {e}")