"""
Módulo de conexión e inicialización para Neo4j.
Gestiona el driver de conexión, valida la integridad de la instancia
y dispara la ingesta de datos si el grafo se encuentra vacío.
"""
from neo4j import GraphDatabase
from motor_neo4j.importarDatasetNeo4j import ImportarDataset

# Configuración de credenciales y endpoint de conexión (Bolt protocol)
uri = "bolt://127.0.0.1:7687"
user = "neo4j"
password = "cursusNeo4j"

def ConectarNeo4j(uri, user, password, base_datos="neo4j"):
    """
    Establece la conexión con la base de datos de grafos.
    Utiliza el driver de Neo4j para verificar la conectividad antes de operar.
    """
    try:
        # Creación del objeto driver: mantiene el pool de conexiones abiertas
        driver = GraphDatabase.driver(uri, auth=(user, password))

        # Validación técnica: asegura que el servidor esté levantado y respondiendo
        driver.verify_connectivity()

        # Auditoría inicial del grafo: consulta cuántos nodos existen
        with driver.session(database=base_datos) as session:
            resultado = session.run("MATCH (n) RETURN count(n) AS total")
            record = resultado.single()
            total_nodos = record["total"] if record else 0

        # Carga los datos si el grafo no tiene entidades
        if total_nodos == 0:
            print("Base de datos Neo4j vacía. Iniciando importación...")
            ImportarDataset(driver, base_datos)
        else:
            print(f"La base de datos '{base_datos}' ya contiene datos. Saltando importación.")

        return driver

    except Exception as e:
        print(f"Se produjo un error al conectar con Neo4j: {e}")
        return None