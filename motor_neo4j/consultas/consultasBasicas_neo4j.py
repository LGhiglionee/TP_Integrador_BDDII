"""
Módulo de consultas básicas para Neo4j (Cypher).
Ejecuta operaciones de recuperación de nodos y filtrado por patrones de texto,
demostrando la eficiencia de las búsquedas en estructuras de grafos.
"""
def listar_todos_entrenadores(session):
    """
    Recupera el listado único de nodos :Entrenador, excluyendo registros
    con etiquetas de datos incompletos ('Desconocido').
    """
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
    """
    Filtra caballos mediante un patrón de relación (c:Caballo)-[:CORRIO]->(:Carrera)
    y una condición sobre la propiedad 'posicion' de la arista.
    """
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
    """
    Utiliza la función de agregación 'count' para obtener la cardinalidad
    de caballos participantes, asegurando unicidad con DISTINCT.
    """
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
    """
    Demuestra el uso de operadores de cadena 'STARTS WITH' en Cypher
    para búsquedas por prefijos de manera nativa y rápida.
    """
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
    """
    Uso del operador 'CONTAINS' para búsqueda de sub-cadenas (patrones de texto)
    dentro de las propiedades de los nodos Caballo.
    """
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