import csv
import os
from pymongo import MongoClient

def ConectarMongo(nombre_base,nombre_coleccion):
    try:
        client = MongoClient('127.0.0.1', 27017)
        db = client[nombre_base] # Base de datos
        collection = db[nombre_coleccion] # Colección

        if collection.count_documents({}) == 0:
            print("Base de datos vacía. Iniciando importación...")
            ImportarDataset(collection)
        else:
            print(f"La colección '{nombre_coleccion}' ya contiene datos. Saltando importación.")

        return collection

    except Exception as e:
        print(f"Se produjo un error al conectar con MongoDB: {e}")
        return None


def ImportarDataset(collection):
    try:
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        
        path = os.path.join(
            ruta_script,
            "..",
            "datasets",
            "race-result-horse.csv"
        )

        with open(path, 'r', encoding='UTF-8') as archivo:
            lector = csv.DictReader(archivo, delimiter=';')
            documentos = []

            for fila in lector:
                convertir_fila(fila)
                documentos.append(fila)
            
            if documentos:
                collection.insert_many(documentos)
                print(f"¡Éxito! Se insertaron {len(documentos)} documentos en MongoDB.")
            else:
                print("El archivo parece estar vacío.")

    except FileNotFoundError:
        print(f"No se encontró el archivo en la ruta: {path}")
    except Exception as e:
        print(f"Se produjo un error al importar el dataset en MongoDB: {e}")

def convertir_fila(fila):
    if fila.get("finish_time_seconds"):
        fila["finish_time_seconds"] = float(fila["finish_time_seconds"].replace(",", "."))

    campos_enteros = [
        "finishing_position",
        "actual_weight",
        "horse_number",
        "declared_horse_weight",
        "running_position_1",
        "running_position_2",
        "running_position_3",
        "draw"
    ]

    for campo in campos_enteros:
        if fila.get(campo):
            fila[campo] = int(fila[campo])