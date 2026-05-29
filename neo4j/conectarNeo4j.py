import csv
import os
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = 'neo4j'
password = 'cursusNeo4j'

# Cambiamos el valor por defecto de nuevo a "neo4j"
def ConectarNeo4j(uri, user, password, base_datos="neo4j"):
    try:
        # Inicializamos el driver de Neo4j
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        # Verificamos si la base de datos está vacía
        with driver.session(database=base_datos) as session:
            resultado = session.run("MATCH (n) RETURN count(n) AS total")
            record = resultado.single()
            total_nodos = record["total"] if record else 0

        if total_nodos == 0:
            print("Base de datos vacía. Iniciando importación...")
            ImportarDataset(driver, base_datos)
        else:
            print(f"La base de datos '{base_datos}' ya contiene datos. Saltando importación.")

        return driver

    except Exception as e:
        print(f"Se produjo un error al conectar: {e}")


def ImportarDataset(driver, base_datos):
    try:
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(ruta_script, "..", "datasets", "horses_2020.csv")
        
        with open(path, 'r', encoding='utf-8-sig') as archivo:
            lector = csv.DictReader(archivo, delimiter=',')
            documentos = []
            
            for fila in lector:
                # 1. Si la fila no tiene nombre de caballo (ej. línea en blanco al final del CSV), la ignoramos
                if not fila.get('horseName') or str(fila['horseName']).strip() == "":
                    continue
                
                # 2. Casteo de posición seguro
                if fila.get('position') and str(fila['position']).isdigit():
                    fila['position'] = int(fila['position'])
                else:
                    fila['position'] = 0 # Valor por si la posición viene vacía o no es un número

                # 3. Limpieza de relaciones para evitar los 'null'
                # Si viene vacío, le asignamos "Desconocido"
                fila['father'] = fila.get('father', '').strip() or "Desconocido"
                fila['mother'] = fila.get('mother', '').strip() or "Desconocida"
                fila['trainerName'] = fila.get('trainerName', '').strip() or "Desconocido"
                
                documentos.append(fila)

            if documentos:
                # Consulta Cypher parametrizada corregida
                query = """
                UNWIND $batch AS fila

                MERGE (caballo:Caballo {nombre: fila.horseName})
                SET caballo.posicion = fila.position

                MERGE (padre:Caballo {nombre: fila.father})
                MERGE (caballo)-[:HIJO_DE]->(padre)

                MERGE (madre:Caballo {nombre: fila.mother})
                MERGE (caballo)-[:HIJO_DE]->(madre)

                MERGE (abuelo:Caballo {nombre: fila.gfather})
                MERGE (caballo)-[:NIETO_DE]->(abuelo)

                MERGE (entrenador:Entrenador {nombre: fila.trainerName})
                MERGE (caballo)-[:ENTRENADO_POR]->(entrenador)
                """
                tamaño_lote = 5000
                total_procesados = 0
                total_documentos = len(documentos)
                
                print(f"Comenzando inserción de {total_documentos} registros en lotes de {tamaño_lote}...")

                with driver.session(database=base_datos) as session:
                    # Recorremos la lista de documentos saltando de a 5000
                    for i in range(0, total_documentos, tamaño_lote):
                        # Cortamos un pedacito de la lista
                        lote_actual = documentos[i : i + tamaño_lote] 
                        
                        # Mandamos solo ese pedacito a Neo4j
                        session.run(query, batch=lote_actual)
                        
                        # Actualizamos el contador e imprimimos en pantalla
                        total_procesados += len(lote_actual)
                        print(f"Progreso: {total_procesados} / {total_documentos} insertados...")

    except FileNotFoundError:
        print(f"No se encontró el archivo en la ruta: {path}")
    except Exception as e:
        print(f"Se produjo un error al importar: {e}")

# Ejecutamos el programa
if __name__ == "__main__":
    app_driver = ConectarNeo4j(uri, user, password)