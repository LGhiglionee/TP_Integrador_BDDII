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
            print(f"Total de entrenadores encontrados: {len(resultados)}")
            for entrenador in resultados:
                print(f"- {entrenador['entrenador']}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")


def caballos_ganadores(session):
    try:
        query = """
        MATCH (c:Caballo)-[r:CORRIO]->(:Carrera)
        WHERE r.posicion = 1
        RETURN DISTINCT c.nombre AS nombre
        ORDER BY nombre ASC
        """

        resultados = list(session.run(query))
        
        if not resultados:
            print("No se encontraron caballos ganadores.")
        else:
            print(f"Total de caballos ganadores encontrados: {len(resultados)}")
            for caballo in resultados:
                print(f"- {caballo['nombre']}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")

def cantidad_total_caballos(session):
    try:
        query = """
        MATCH (c:Caballo)-[:CORRIO]->(:Carrera)
        RETURN count(DISTINCT c) AS total
        """

        resultados = list(session.run(query))
        
        if not resultados:
            print("No se pudieron contar el total de caballos.")
        else:
            for registro in resultados:
                print(f"Total de caballos que corrieron carreras encontrados: {registro['total']}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")


def entrenadores_letra_p(session):
    try:
        query = """
        MATCH (e:Entrenador)
        WHERE toUpper (e.nombre) STARTS WITH 'P'
        RETURN DISTINCT e.nombre AS entrenador
        ORDER BY entrenador
        """

        resultados = list(session.run(query))
        
        if not resultados:
            print("No se encontraron entrenadores que comiencen con la letra P.")
        else:
            print(f"Total de entrenadores que su nombre comienza con P es: {len(resultados)}")
            for entrenador in resultados:
                print(f"- {entrenador['entrenador']}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")


def caballos_con_dragon(session):
    try:
        query = """
        MATCH (c:Caballo)-[:CORRIO]->(:Carrera)
        WHERE toUpper (c.nombre) CONTAINS 'DRAGON'
        RETURN DISTINCT c.nombre AS nombre
        ORDER BY nombre
        """
        resultados = list(session.run(query))
        
        if not resultados:
            print("No se encontraron caballos con la palabra 'DRAGON' en su nombre.")
        else:
            print(f"Total de caballos con ´DRAGON´ en su nombre es:{len(resultados)}")
            for caballo in resultados:
                print(f"- {caballo['nombre']}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")