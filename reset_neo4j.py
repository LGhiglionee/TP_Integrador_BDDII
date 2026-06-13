from neo4j import GraphDatabase

uri = "bolt://127.0.0.1:7687"
user = "neo4j"
password = "cursusNeo4j"

driver = GraphDatabase.driver(uri, auth=(user, password))

try:
    with driver.session(database="neo4j") as session:
        session.run("""
            MATCH (n)
            DETACH DELETE n
        """)

    print("Base Neo4j limpiada correctamente.")

except Exception as e:
    print(f"Error al limpiar Neo4j: {e}")

finally:
    driver.close()