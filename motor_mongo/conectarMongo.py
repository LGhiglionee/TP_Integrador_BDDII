import csv
import os
from pymongo import MongoClient

def ConectarMongo(a, b):
    try:
        client = MongoClient('127.0.0.1', 27017)
        db = client[a] # Base de datos
        collection = db[b] # Colección

        # Le pasamos la colección como parámetro a la función
        if collection.count_documents({}) == 0:
            print("Base de datos vacía. Iniciando importación...")
            ImportarDataset(collection)
        else:
            print(f"La colección '{b}' ya contiene datos. Saltando importación.")

        return collection

    except Exception as e:
        print(f"Se produjo un error al conectar: {e}")


def ImportarDataset(collection):
    try:
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        
        path = os.path.join(ruta_script, "..", "datasets", "race-result-horse.csv")
        # Le cambiamos el alias a "archivo" para no pisar el nombre del módulo "csv"
        with open(path, 'r', encoding='UTF-8') as archivo:
            
            # Ahora sí detecta correctamente el módulo csv
            lector = csv.DictReader(archivo, delimiter=';')
            documentos = []
            for fila in lector:
                if fila.get('finish_time_seconds'): fila['finish_time_seconds'] = float(fila['finish_time_seconds'])
                if fila.get('finishing_position'): fila['finishing_position'] = int(fila['finishing_position'])
                if fila.get('actual_weight'): fila['actual_weight'] = int(fila['actual_weight'])
                if fila.get('horse_number'): fila['horse_number'] = int(fila['horse_number'])
                if fila.get('declared_horse_weight'): fila['declared_horse_weight'] = int(fila['declared_horse_weight'])
                if fila.get('running_position_1'): fila['running_position_1'] = int(fila['running_position_1'])
                if fila.get('running_position_2'): fila['running_position_2'] = int(fila['running_position_2'])
                if fila.get('running_position_3'): fila['running_position_3'] = int(fila['running_position_3'])
                documentos.append(fila)
            
            if documentos:
                # Usa la colección que le llegó por parámetro
                collection.insert_many(documentos)
                print(f"¡Éxito! Se insertaron {len(documentos)} documentos en MongoDB.")
            else:
                print("El archivo parece estar vacío.")

    except FileNotFoundError:
        print(f"No se encontró el archivo en la ruta: {path}")
    except Exception as e:
        print(f"Se produjo un error al importar: {e}")
