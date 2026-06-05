### 1. Sistema de Recomendación de Entrenadores (Matchmaking)

'''La lógica: Imaginate que comprás un caballo nuevo que es hijo de "Padre_X". No sabés con quién mandarlo a entrenar. El sistema podría buscar a todos los demás caballos que también sean hijos de "Padre_X" y ver qué entrenador se repite más entre ellos.
El resultado: "Te recomendamos el entrenador Y, porque tiene mucha experiencia entrenando a otros hijos de la misma familia de tu caballo".'''


### 2. Sistema de "Caballos Similares" (Para apuestas o compra)

'''La lógica: Si a un usuario le gusta mucho un caballo en particular por su rendimiento, el sistema de recomendación podría sugerirle caballos "similares".
¿Cómo se define "similar" en grafos?: Un caballo es similar a otro si, por ejemplo, comparten el mismo abuelo Y además tienen el mismo entrenador. En un grafo, esto es simplemente buscar un patrón de "forma de diamante" entre los nodos.'''


### 3. Recomendación basada en "Éxito" Genético

'''La lógica: Como en los nodos de caballos guardaste la propiedad posicion (la posición final en la que salieron), podrías armar un motor de recomendación de apuestas.
El resultado: El sistema busca aquellos linajes (padres o abuelos) donde la mayoría de sus hijos terminaron en posicion = 1. Luego, te recomienda apostar por otros caballos de esa misma familia, asumiendo que "la velocidad viene de familia".'''

# 1. Buscar posición de un caballo específico
def buscar_caballo_nombre(session):
    try:
        nombre = input("Ingresar nombre del caballo: ").upper().strip()
        
        query = """
        MATCH (c:Caballo {nombre: $nombre_caballo})
        RETURN c.nombre AS nombre, c.posicion AS posicion
        """
        resultados = list(session.run(query, nombre_caballo=nombre))
        
        if not resultados:
            print(f"No se encontraron registros para el caballo: {nombre}")
        else:
            print(f"=== HISTORIAL DE POSICIÓN ===")
            for caballo in resultados:
                print(f"Caballo: {caballo['nombre']} | Última Posición registrada: {caballo['posicion']}")
                
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
        MATCH (padre)<-[:HIJO_DE]-(hijo_ganador:Caballo {posicion: 1})
        WITH padre, count(hijo_ganador) AS victorias
        WHERE victorias >= 1
        MATCH (padre)<-[:HIJO_DE]-(caballo_sugerido:Caballo)
        WHERE caballo_sugerido.posicion <> 1
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
        nombre = input("Ingresar nombre del caballo para su árbol genealógico: ").upper().strip()
        
        query = """
        MATCH (c:Caballo {nombre: $nombre_caballo})-[:HIJO_DE]->(progenitor:Caballo)
        MATCH (c)-[:NIETO_DE]->(abuelo:Caballo)
        WHERE progenitor.nombre <> 'Desconocido' AND abuelo.nombre <> 'Desconocido'
        RETURN c.nombre AS analizado, c.posicion AS pos, collect(DISTINCT progenitor.nombre) AS padres, abuelo.nombre AS abuelo
        """
        resultados = list(session.run(query, nombre_caballo=nombre))
        
        if not resultados:
            print(f"No se pudo estructurar el árbol genealógico completo para: {nombre}")
        else:
            print(f"=== ANÁLISIS DE ÁRBOL GENEALÓGICO DE GRAFOS ===")
            for r in resultados:
                print(f"Ficha Técnica: {r['analizado']}")
                print(f"Último puesto en competencia: {r['pos']}")
                print(f"Padres Directos (Relación HIJO_DE): {', '.join(r['padres'])}")
                print(f"Abuelo Registrado (Relación NIETO_DE): {r['abuelo']}")
                
    except Exception as e:
        print(f"Error en la consulta avanzada: {e}")