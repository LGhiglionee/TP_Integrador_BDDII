from neo4j import GraphDatabase

from motor_neo4j.importarDatasetNeo4j import ImportarDataset


uri = "bolt://127.0.0.1:7687"
user = "neo4j"
password = "cursusNeo4j"


def ConectarNeo4j(uri, user, password, base_datos="neo4j"):
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))

        driver.verify_connectivity()

        with driver.session(database=base_datos) as session:
            resultado = session.run("MATCH (n) RETURN count(n) AS total")
            record = resultado.single()
            total_nodos = record["total"] if record else 0

        if total_nodos == 0:
            print("Base de datos Neo4j vacía. Iniciando importación...")
            ImportarDataset(driver, base_datos)
        else:
            print(f"La base de datos '{base_datos}' ya contiene datos. Saltando importación.")

        return driver

    except Exception as e:
        print(f"Se produjo un error al conectar con Neo4j: {e}")
        return None