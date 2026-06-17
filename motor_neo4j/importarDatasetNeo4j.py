import csv
import os


def ImportarDataset(driver, base_datos):
    try:
        ruta_script = os.path.dirname(os.path.abspath(__file__))

        path = os.path.join(
            ruta_script,
            "..",
            "datasets",
            "race-result-horse.csv"
        )

        with open(path, "r", encoding="UTF-8") as archivo:
            lector = csv.DictReader(archivo, delimiter=";")
            documentos = []

            for fila in lector:
                horse_id = limpiar_texto(fila.get("horse_id"))
                horse_name = limpiar_texto(fila.get("horse_name"))
                race_id = limpiar_texto(fila.get("race_id"))

                if not horse_id or not horse_name or not race_id:
                    continue

                fila_limpia = {
                    "horse_id": horse_id,
                    "horse_name": horse_name,
                    "race_id": race_id,

                    "jockey": limpiar_texto(fila.get("jockey")) or "Desconocido",
                    "trainer": limpiar_texto(fila.get("trainer")) or "Desconocido",

                    "father": limpiar_texto(fila.get("father")) or "Desconocido",
                    "mother": limpiar_texto(fila.get("mother")) or "Desconocida",
                    "gfather": limpiar_texto(fila.get("gfather")) or "Desconocido",

                    "finishing_position": convertir_int(fila.get("finishing_position")),
                    "horse_number": convertir_int(fila.get("horse_number")),
                    "actual_weight": convertir_int(fila.get("actual_weight")),
                    "declared_horse_weight": convertir_int(fila.get("declared_horse_weight")),
                    "draw": convertir_int(fila.get("draw")),
                    "running_position_1": convertir_int(fila.get("running_position_1")),
                    "running_position_2": convertir_int(fila.get("running_position_2")),
                    "running_position_3": convertir_int(fila.get("running_position_3")),

                    "finish_time": limpiar_texto(fila.get("finish_time")),
                    "finish_time_seconds": convertir_float(fila.get("finish_time_seconds")),
                }

                documentos.append(fila_limpia)

        if not documentos:
            print("El archivo CSV parece estar vacío o no contiene filas válidas.")
            return

        print(f"Comenzando inserción de {len(documentos)} registros en Neo4j...")

        tamaño_lote = 5000

        with driver.session(database=base_datos) as session:
            insertar_nodos_principales(session, documentos, tamaño_lote)
            insertar_relaciones(session, documentos, tamaño_lote)
            
            print("Calculando el total de entidades y relaciones importadas...")
            resultado_entidades = session.run("MATCH (n) RETURN count(n) AS TotalEntidades").single()
            resultado_relaciones = session.run("MATCH ()-[r]->() RETURN count(r) AS TotalRelaciones").single()
            
            if resultado_entidades:
                print(f"Total de Entidades: {resultado_entidades['TotalEntidades']}")
            if resultado_relaciones:
                print(f"Total de Relaciones: {resultado_relaciones['TotalRelaciones']}")

        print("Importación completa en Neo4j.")

    except FileNotFoundError:
        print(f"No se encontró el archivo en la ruta: {path}")

    except Exception as e:
        print(f"Se produjo un error al importar en Neo4j: {e}")


def insertar_nodos_principales(session, documentos, tamaño_lote):
    query = """
        UNWIND $batch AS fila

        MERGE (c:Caballo {id: fila.horse_id})
        SET c.nombre = fila.horse_name,
            c.numero = fila.horse_number

        MERGE (race:Carrera {id: fila.race_id})

        MERGE (e:Entrenador {nombre: fila.trainer})

        MERGE (j:Jockey {nombre: fila.jockey})
    """

    total_documentos = len(documentos)

    for i in range(0, total_documentos, tamaño_lote):
        lote_actual = documentos[i:i + tamaño_lote]
        session.run(query, batch=lote_actual)


def insertar_relaciones(session, documentos, tamaño_lote):
    query = """
        UNWIND $batch AS fila

        MERGE (c:Caballo {id: fila.horse_id})
        SET c.nombre = fila.horse_name,
            c.numero = fila.horse_number

        MERGE (race:Carrera {id: fila.race_id})

        MERGE (e:Entrenador {nombre: fila.trainer})

        MERGE (j:Jockey {nombre: fila.jockey})

        MERGE (c)-[r:CORRIO]->(race)
        SET r.posicion = fila.finishing_position,
            r.peso_actual = fila.actual_weight,
            r.peso_declarado = fila.declared_horse_weight,
            r.sorteo = fila.draw,
            r.posicion_1 = fila.running_position_1,
            r.posicion_2 = fila.running_position_2,
            r.posicion_3 = fila.running_position_3,
            r.tiempo = fila.finish_time,
            r.tiempo_segundos = fila.finish_time_seconds

        MERGE (p:Caballo {nombre: fila.father})
        MERGE (c)-[:HIJO_DE]->(p)

        MERGE (m:Caballo {nombre: fila.mother})
        MERGE (c)-[:HIJO_DE]->(m)

        MERGE (ab:Caballo {nombre: fila.gfather})
        MERGE (c)-[:NIETO_DE]->(ab)

        MERGE (c)-[:ENTRENADO_POR]->(e)

        MERGE (c)-[:MONTADO_POR]->(j)
    """

    total_documentos = len(documentos)

    for i in range(0, total_documentos, tamaño_lote):
        lote_actual = documentos[i:i + tamaño_lote]
        session.run(query, batch=lote_actual)


def limpiar_texto(valor):
    if valor is None:
        return None

    valor = str(valor).strip()

    if valor == "":
        return None

    return valor


def convertir_int(valor):
    try:
        if valor is None or str(valor).strip() == "":
            return None

        return int(valor)

    except:
        return None


def convertir_float(valor):
    try:
        if valor is None or str(valor).strip() == "":
            return None

        return float(str(valor).replace(",", "."))

    except:
        return None