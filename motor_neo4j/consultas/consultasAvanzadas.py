# 1. Buscar posición de un caballo específico
def buscar_caballo_nombre(session, nombre):
    try:
        nombre = nombre.upper().strip()

        query = """
        MATCH (c:Caballo {nombre: $nombre_caballo})-[r:CORRIO]->(race:Carrera)
        RETURN c.nombre AS nombre, r.posicion AS posicion, race.id AS carrera_id
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


# 2. Recomendación de Entrenador (Matchmaking por hermanos)
def recomendacion_entrenador_matchmaking(session, nombre):
    try:
        nombre = nombre.upper().strip()

        query = """
        MATCH (c:Caballo {nombre: $nombre_caballo})-[:HIJO_DE]->(padre:Caballo)
        MATCH (padre)<-[:HIJO_DE]-(hermano:Caballo)-[:ENTRENADO_POR]->(e:Entrenador)
        WHERE e.nombre <> 'Desconocido' 
          AND hermano <> c
        WITH e, count(hermano) AS hermanos_entrenados
        RETURN e.nombre AS entrenador, hermanos_entrenados
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
                print(f"Razón: Ya entrenó a {r['hermanos_entrenados']} hermanos de la misma familia genética.")

    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")


# 3. Buscar Caballos Similares (Patrón de Diamante)
def caballos_similares_diamante(session, nombre):
    try:
        nombre = nombre.upper().strip()

        query = """
        MATCH (c1:Caballo {nombre: $nombre_caballo})-[:NIETO_DE]->(abuelo:Caballo)
        MATCH (c1)-[:ENTRENADO_POR]->(e:Entrenador)
        WHERE abuelo.nombre <> 'Desconocido' 
          AND e.nombre <> 'Desconocido'

        MATCH (c2:Caballo)-[:NIETO_DE]->(abuelo)
        MATCH (c2)-[:ENTRENADO_POR]->(e)
        WHERE c1 <> c2 
          AND c2.nombre <> 'Desconocido'

        RETURN DISTINCT c2.nombre AS similar, abuelo.nombre AS abuelo, e.nombre AS entrenador
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
                print(f"- Caballo: {r['similar']}")
                print(f"  * Comparten el abuelo: {r['abuelo']}")
                print(f"  * Comparten el mismo entrenador: {r['entrenador']}\n")

    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")


# 4. Recomendación de Apuestas por Éxito Genético
def recomendacion_apuestas_linaje(session, nombre):
    try:
        nombre = nombre.upper().strip()

        query = """
        MATCH (c:Caballo {nombre: $nombre_caballo})-[:HIJO_DE]->(padre:Caballo)
        WHERE padre.nombre <> 'Desconocido'

        MATCH (padre)<-[:HIJO_DE]-(hijo_ganador:Caballo)-[r:CORRIO]->(:Carrera)
        WHERE r.posicion = 1
        WITH padre, count(DISTINCT hijo_ganador) AS victorias, c

        MATCH (padre)<-[:HIJO_DE]-(caballo_sugerido:Caballo)
        WHERE caballo_sugerido <> c 
          AND caballo_sugerido.nombre <> 'Desconocido'
          AND EXISTS {
              MATCH (caballo_sugerido)-[r2:CORRIO]->(:Carrera)
              WHERE r2.posicion <> 1
          }

        RETURN DISTINCT caballo_sugerido.nombre AS sugerido, padre.nombre AS padre, victorias
        ORDER BY victorias DESC, caballo_sugerido.nombre
        LIMIT 3
        """

        resultados = list(session.run(query, nombre_caballo=nombre))

        if not resultados:
            print(f"La familia directa de {nombre} no registra un linaje estadísticamente ganador para apuestas.")
        else:
            print("=== MOTOR DE RECOMENDACIÓN DE APUESTAS GENÉTICAS ===")
            print(f"Analizando la sangre de '{nombre}', se encontraron las siguientes apuestas sugeridas:")
            for r in resultados:
                print(f"- Caballo Sugerido: {r['sugerido']}")
                print(f"  * Pertenece al linaje exitoso de: {r['padre']}")
                print(f"  * Victorias de la familia en carreras: {r['victorias']}\n")

    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")


# 5. Ficha Genealógica Estructurada (Línea de Sangre)
def linea_sangre_caballo(session, nombre):
    try:
        nombre = nombre.upper().strip()

        query = """
        MATCH (c:Caballo {nombre: $nombre_caballo})
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
                padres = [p for p in r["padres"] if p is not None]
                abuelos = [a for a in r["abuelos"] if a is not None]

                print(f"Ficha Técnica: {r['analizado']}")
                print(f"Posiciones obtenidas: {', '.join(posiciones) if posiciones else 'Sin posiciones cargadas'}")
                print(f"Padres: {', '.join(padres) if padres else 'Sin padres cargados'}")
                print(f"Abuelos: {', '.join(abuelos) if abuelos else 'Sin abuelos cargados'}")

    except Exception as e:
        print(f"Error en la consulta: {e}")


# 6. Promedio de posiciones por entrenadores de hijos de un caballo padre dado
def ranking_entrenadores_por_linaje(session, nombre_padre):
    try:
        nombre_padre = nombre_padre.upper().strip()

        query = """
        MATCH (padre:Caballo {nombre: $nombre_padre})<-[:HIJO_DE]-(hijo:Caballo)
        MATCH (hijo)-[r:CORRIO]->(:Carrera)
        MATCH (hijo)-[:ENTRENADO_POR]->(e:Entrenador)
        WHERE e.nombre <> 'Desconocido'
        WITH 
            e, 
            avg(r.posicion) AS promedio_posicion, 
            count(DISTINCT hijo) AS cantidad_caballos
        RETURN 
            e.nombre AS entrenador, 
            promedio_posicion, 
            cantidad_caballos
        ORDER BY promedio_posicion ASC
        """

        resultados = list(session.run(query, nombre_padre=nombre_padre))

        if not resultados:
            print(f"No hay registros suficientes para '{nombre_padre}'.")
        else:
            print(f"=== RANKING: ¿Quién entrena mejor a los hijos de '{nombre_padre}'? ===")
            for r in resultados:
                print(
                    f"Entrenador: {r['entrenador']} | "
                    f"Promedio de llegada: {r['promedio_posicion']:.2f} | "
                    f"Caballos analizados: {r['cantidad_caballos']}"
                )

    except Exception as e:
        print(f"Error: {e}")