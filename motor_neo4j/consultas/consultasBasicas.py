# 1. Listar todos los entrenadores únicos registrados
def listar_todos_entrenadores(session):
    try:
        query = """
        MATCH (e:Entrenador)
        WHERE e.nombre <> 'Desconocido'
        RETURN DISTINCT e.nombre AS entrenador
        ORDER BY entrenador ASC
        """
        resultados = list(session.run(query))
        
        if not resultados:
            print("No se encontraron entrenadores registrados.")
        else:
            print(f"Total de entrenadores únicos encontrados: {len(resultados)}")
            for entrenador in resultados:
                print(f"- {entrenador['entrenador']}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")


# 2. Mostrar todos los caballos ganadores (Posición 1)
def caballos_ganadores(session):
    try:
        query = """
        MATCH (c:Caballo)-[r:CORRIO]->(:Carrera)
        WHERE r.posicion = 1
        RETURN DISTINCT c.nombre AS nombre
        """
        resultados = list(session.run(query))
        
        if not resultados:
            print("No se encontraron caballos ganadores con posición 1.")
        else:
            print(f"El total de caballos ganadores en el grafo es: {len(resultados)}")
            for caballo in resultados:
                print(f"🏆 {caballo['nombre']}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")


# 3. Contar la cantidad total de caballos en el grafo
def cantidad_total_caballos(session):
    try:
        query = """
        MATCH (c:Caballo)
        RETURN count(c) AS total
        """
        resultados = list(session.run(query))
        
        if not resultados:
            print("No se pudieron contabilizar los caballos.")
        else:
            for registro in resultados:
                print(f"La cantidad total de caballos registrados en el grafo es: {registro['total']}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")


# 4. Mostrar entrenadores cuyo nombre empieza con P
def entrenadores_letra_p(session):
    try:
        query = """
        MATCH (e:Entrenador)
        WHERE e.nombre STARTS WITH 'P'
        RETURN DISTINCT e.nombre AS entrenador
        """
        resultados = list(session.run(query))
        
        if not resultados:
            print("No se encontraron entrenadores que comiencen con la letra P.")
        else:
            print(f"Los entrenadores que comienzan con la letra P son: {len(resultados)}")
            for entrenador in resultados:
                print(f"- {entrenador['entrenador']}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")


# 5. Mostrar caballos que contienen 'DRAGON' en su nombre
def caballos_con_dragon(session):
    try:
        query = """
        MATCH (c:Caballo)
        WHERE c.nombre CONTAINS 'DRAGON'
        RETURN DISTINCT c.nombre AS nombre
        """
        resultados = list(session.run(query))
        
        if not resultados:
            print("No se encontraron caballos con la palabra 'DRAGON' en su nombre.")
        else:
            print(f"Se encontraron {len(resultados)} caballos con 'DRAGON':")
            for caballo in resultados:
                print(f"- {caballo['nombre']}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")