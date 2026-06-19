"""
Módulo de conexión e ingesta de datos para MongoDB.
Gestiona la conexión con el cluster y la carga automatizada (ETL) desde CSV
al paradigma documental, asegurando la integridad del tipado de datos.
"""
import csv
import os
from pymongo import MongoClient

def ConectarMongo(nombre_base,nombre_coleccion):
    """
    Establece la conexión con la instancia local de MongoDB.
    Si la colección está vacía, dispara el proceso de carga de datos (ImportarDataset).
    """
    try:
        # Inicialización del cliente (Driver PyMongo)
        client = MongoClient('127.0.0.1', 27017)
        db = client[nombre_base] # Base de datos
        collection = db[nombre_coleccion] # Colección

        # Verificación de estado: si no hay documentos, iniciamos la ingesta
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
    """
    Proceso de Ingesta (ETL): Lee el CSV, normaliza el formato de datos
    mediante convertir_fila y realiza una inserción masiva.
    """
    try:
        # Obtención dinámica de la ruta del archivo mediante os.path
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        
        path = os.path.join(ruta_script,"..","datasets","race-result-horse.csv")

        with open(path, 'r', encoding='UTF-8') as archivo:
            # Lectura del CSV como diccionario para mapeo directo a documentos BSON
            lector = csv.DictReader(archivo, delimiter=';')
            documentos = []

            for fila in lector:
                # Normalización de tipos de datos antes de la persistencia
                convertir_fila(fila)
                documentos.append(fila)

            # Inserción masiva de registros: operación optimizada de escritura en MongoDB
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
    """
    Función de normalización y tipado (Type Casting).
    Convierte cadenas de texto del CSV a tipos numéricos (float/int)
    para permitir consultas y cálculos matemáticos (agregaciones) nativos.
    """
    # Conversión de tiempo a punto flotante (necesario para cálculos de promedio)
    if fila.get("finish_time_seconds"):
        fila["finish_time_seconds"] = float(fila["finish_time_seconds"].replace(",", "."))

    # Lista de campos que deben ser enteros para las consultas de posición y peso
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