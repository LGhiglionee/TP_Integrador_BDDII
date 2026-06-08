# 1. Buscar posición de un caballo específico
def buscar_caballo_nombre(session):
    try:
        nombre = input("Ingresar nombre del caballo: ").upper().strip()
        
        query = """
        MATCH (c:Caballo {nombre: $nombre_caballo})-[r:CORRIO]->(race:Carrera)
        RETURN c.nombre AS nombre, r.posicion AS posicion, race.id AS carrera_id
        """
        resultados = list(session.run(query, nombre_caballo=nombre))
        
        if not resultados:
            print(f"No se encontraron registros para el caballo: {nombre}")
        else:
            print(f"=== HISTORIAL DE POSICIÓN ===")
            for r in resultados:
                print(f"Caballo: {r['nombre']} | Carrera: {r['carrera_id']} | Posición: {r['posicion']}")
                
    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")


# 2. Recomendación de Entrenador (Matchmaking por hermanos)
def recomendacion_entrenador_matchmaking(session):
    try:
        nombre = input("Ingresar nombre del caballo para matchmaking: ").upper().strip()
        
        # Buscamos el padre del caballo ingresado, luego a sus medio hermanos, y vemos qué entrenador se repite más
        query = """
        MATCH (c:Caballo {nombre: $nombre_caballo})-[:HIJO_DE]->(padre:Caballo)
        MATCH (padre)<-[:HIJO_DE]-(hermano:Caballo)-[:ENTRENADO_POR]->(e:Entrenador)
        WHERE e.nombre <> 'Desconocido' AND hermano <> c
        WITH e, count(hermano) AS hermanos_entrenados
        RETURN e.nombre AS entrenador, hermanos_entrenados
        ORDER BY hermanos_entrenados DESC
        LIMIT 1
        """
        resultados = list(session.run(query, nombre_caballo=nombre))
        
        if not resultados:
            print(f"No hay suficiente historial familiar o linaje cargado para recomendar un entrenador a {nombre}.")
        else:
            print(f"=== SISTEMA DE RECOMENDACIÓN DE ENTRENADORES ===")
            for r in resultados:
                print(f"Para el caballo '{nombre}':")
                print(f"Te recomendamos al entrenador: {r['entrenador']}")
                print(f"Razón: Ya entrenó a {r['hermanos_entrenados']} hermanos de la misma familia genética.")
                
    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")


# 3. Buscar Caballos Similares (Patrón de Diamante)
def caballos_similares_diamante(session):
    try:
        nombre = input("Ingresar nombre del caballo para buscar similares: ").upper().strip()
        
        # Un caballo es similar a otro si comparten el mismo abuelo e indicador de entrenador (Cierra el Diamante)
        query = """
        MATCH (c1:Caballo {nombre: $nombre_caballo})-[:NIETO_DE]->(abuelo:Caballo),
              (c1)-[:ENTRENADO_POR]->(e:Entrenador),
              (c2:Caballo)-[:NIETO_DE]->(abuelo),
              (c2)-[:ENTRENADO_POR]->(e)
        WHERE c1 <> c2 AND c2.nombre <> 'Desconocido'
        RETURN DISTINCT c2.nombre AS similar, abuelo.nombre AS abuelo, e.nombre AS entrenador
        """
        resultados = list(session.run(query, nombre_caballo=nombre))
        
        if not resultados:
            print(f"No se encontraron patrones de diamante o caballos similares para: {nombre}")
        else:
            print(f"=== PATRÓN DE DIAMANTE (CABALLOS SIMILARES DE LINAJE) ===")
            print(f"Caballos con características similares a '{nombre}':")
            for r in resultados:
                print(f"- Caballo: {r['similar']}")
                print(f"  * Comparten el abuelo: {r['abuelo']}")
                print(f"  * Comparten el mismo entrenador: {r['entrenador']}\n")
                
    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")


# 4. Recomendación de Apuestas por Éxito Genético
def recomendacion_apuestas_linaje(session):
    try:
        nombre = input("Ingresar nombre de un caballo para validar linaje: ").upper().strip()
        
        # Buscamos el padre del caballo, cuántas victorias (posicion = 1) tienen sus hijos, y sugerimos otros parientes no ganadores
        query = """
        MATCH (c:Caballo {nombre: $nombre_caballo})-[:HIJO_DE]->(padre:Caballo)
        MATCH (padre)<-[:HIJO_DE]-(hijo_ganador:Caballo)-[r:CORRIO]->(:Carrera)
        WHERE r.posicion = 1
        WITH padre, count(hijo_ganador) AS victorias
        MATCH (padre)<-[:HIJO_DE]-(caballo_sugerido:Caballo)-[r2:CORRIO]->(:Carrera)
        WHERE r2.posicion <> 1
        RETURN DISTINCT caballo_sugerido.nombre AS sugerido, padre.nombre AS padre, victorias
        LIMIT 3
        """
        resultados = list(session.run(query, nombre_caballo=nombre))
        
        if not resultados:
            print(f"La familia directa de {nombre} no registra un linaje estadísticamente ganador para apuestas.")
        else:
            print(f"=== MOTOR DE RECOMENDACIÓN DE APUESTAS GENÉTICAS ===")
            print(f"Analizando la sangre de '{nombre}', se encontraron las siguientes apuestas sugeridas:")
            for r in resultados:
                print(f"- Caballo Sugerido: {r['sugerido']}")
                print(f"  * Pertenece al linaje exitoso de: {r['padre']}")
                print(f"  * Victorias de la familia en carreras: {r['victorias']}\n")
                
    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")


# 5. Ficha Genealógica Estructurada (Línea de Sangre)
def linea_sangre_caballo(session):
    try:

        nombre = input("Ingresar nombre de un caballo: ").upper().strip()

        query = """
        MATCH (c:Caballo {nombre: $nombre_caballo})
        OPTIONAL MATCH (c)-[:HIJO_DE]->(progenitor:Caballo)
        OPTIONAL MATCH (c)-[:NIETO_DE]->(abuelo:Caballo)
        OPTIONAL MATCH (c)-[r:CORRIO]->(:Carrera)
        RETURN c.nombre AS analizado, collect(DISTINCT r.posicion) AS posiciones, collect(DISTINCT progenitor.nombre) AS padres, collect(DISTINCT abuelo.nombre) AS abuelos
        """
        resultados = list(session.run(query, nombre_caballo=nombre))
        
        if not resultados:
            print(f"No se encontró información para: {nombre}")
        else:
            print(f"=== ANÁLISIS DE ÁRBOL GENEALÓGICO ===")
            for r in resultados:
                print(f"Ficha Técnica: {r['analizado']}")
                # Mostramos la lista de posiciones recolectadas
                print(f"Posiciones obtenidas: {', '.join(map(str, r['posiciones']))}")
                print(f"Padres: {', '.join(r['padres'])}")
                print(f"Abuelos: {', '.join(r['abuelos'])}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")

#6. Promedio de posiciones por entrenadores de hijos de un caballo padre dado

def ranking_entrenadores_por_linaje(session):
    try:
        nombre_padre = input("Ingresar nombre del padre para el ranking: ").upper().strip()
        
        query = """
        MATCH (padre:Caballo {nombre: $nombre_padre})<-[:HIJO_DE]-(hijo:Caballo)
        MATCH (hijo)-[r:CORRIO]->(:Carrera)
        MATCH (hijo)-[:ENTRENADO_POR]->(e:Entrenador)
        WHERE e.nombre <> 'Desconocido'
        WITH e, avg(r.posicion) AS promedio_posicion, count(DISTINCT(hijo)) AS cantidad_caballos
        RETURN e.nombre AS entrenador, promedio_posicion, cantidad_caballos
        ORDER BY promedio_posicion ASC
        """
        
        resultados = list(session.run(query, nombre_padre=nombre_padre))
        
        if not resultados:
            print(f"No hay registros suficientes para '{nombre_padre}'.")
        else:
            print(f"=== RANKING: ¿Quién entrena mejor a los hijos de '{nombre_padre}'? ===")
            for r in resultados:
                print(f"Entrenador: {r['entrenador']} | Promedio de llegada: {r['promedio_posicion']:.2f} | Caballos analizados: {r['cantidad_caballos']}")
                
    except Exception as e:
        print(f"Error: {e}")