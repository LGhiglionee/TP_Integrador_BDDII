import csv

def convertir_valor(valor, tipo):
    if valor == "" or valor is None:
        return None

    if tipo == "int":
        return int(valor)

    if tipo == "float":
        return float(valor.replace(",", "."))

    return valor

def ImportarDatasetCassandra(session, path_csv, tabla, columnas, tipos_columnas):
    try:
        with open(path_csv, "r", encoding="UTF-8") as archivo:
            lector = csv.DictReader(archivo, delimiter=";")

            columnas_sql = ", ".join(columnas)
            placeholders = ", ".join(["?"] * len(columnas))

            query = f"""
                INSERT INTO {tabla} ({columnas_sql})
                VALUES ({placeholders})
            """

            insert_preparado = session.prepare(query)

            cantidad = 0

            for fila in lector:
                valores = []

                for columna in columnas:
                    tipo = tipos_columnas.get(columna, "text")
                    valor = convertir_valor(fila.get(columna), tipo)
                    valores.append(valor)

                session.execute(insert_preparado, valores)
                cantidad += 1

            print(f"Se insertaron {cantidad} registros en {tabla}.")

    except FileNotFoundError:
        print("No se encontró el archivo CSV.")

    except Exception as e:
        print(f"Error al importar dataset: {e}")