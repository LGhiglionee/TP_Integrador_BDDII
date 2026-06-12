import csv
import os


def ImportarDataset(session):
    try:
        ruta_script = os.path.dirname(os.path.abspath(__file__))

        path = os.path.join(
            ruta_script,
            "..",
            "datasets",
            "race-result-horse.csv"
        )

        if not os.path.exists(path):
            print(f"No se encontró el archivo CSV en la ruta: {path}")
            return

        with open(path, "r", encoding="UTF-8") as archivo:
            lector = csv.DictReader(archivo, delimiter=";")
            filas = list(lector)

        if not filas:
            print("El archivo CSV está vacío.")
            return

        print(f"Cantidad de filas leídas del CSV: {len(filas)}")
        print(f"Columnas detectadas: {list(filas[0].keys())}")

        importar_resultados_por_carrera(session, filas)
        importar_historial_por_caballo(session, filas)
        importar_historial_por_jockey(session, filas)
        importar_caballos_por_entrenador(session, filas)
        importar_caballos_por_padre(session, filas)
        importar_mejores_tiempos_por_carrera(session, filas)

        print("Importación completa en Cassandra.")

    except FileNotFoundError:
        print(f"No se encontró el archivo CSV en la ruta: {path}")

    except Exception as e:
        print(f"Se produjo un error al importar en Cassandra: {e}")


def convertir_int(valor):
    try:
        if valor == "" or valor is None:
            return None
        return int(valor)
    except:
        return None


def convertir_float(valor):
    try:
        if valor == "" or valor is None:
            return None
        return float(str(valor).replace(",", "."))
    except:
        return None


def convertir_texto(valor):
    if valor == "" or valor is None:
        return None
    return str(valor).strip()


def armar_valores_base(fila):
    return {
        "finishing_position": convertir_int(fila.get("finishing_position")),
        "horse_number": convertir_int(fila.get("horse_number")),
        "horse_name": convertir_texto(fila.get("horse_name")),
        "horse_id": convertir_texto(fila.get("horse_id")),
        "jockey": convertir_texto(fila.get("jockey")),
        "trainer": convertir_texto(fila.get("trainer")),
        "actual_weight": convertir_int(fila.get("actual_weight")),
        "declared_horse_weight": convertir_int(fila.get("declared_horse_weight")),
        "draw": convertir_int(fila.get("draw")),
        "running_position_1": convertir_int(fila.get("running_position_1")),
        "running_position_2": convertir_int(fila.get("running_position_2")),
        "running_position_3": convertir_int(fila.get("running_position_3")),
        "finish_time": convertir_texto(fila.get("finish_time")),
        "finish_time_seconds": convertir_float(fila.get("finish_time_seconds")),
        "race_id": convertir_texto(fila.get("race_id")),
        "father": convertir_texto(fila.get("father")),
        "mother": convertir_texto(fila.get("mother")),
        "gfather": convertir_texto(fila.get("gfather")),
    }


def importar_resultados_por_carrera(session, filas):
    query = """
        INSERT INTO resultados_por_carrera (
            race_id,
            finishing_position,
            horse_id,
            horse_number,
            horse_name,
            jockey,
            trainer,
            actual_weight,
            declared_horse_weight,
            draw,
            running_position_1,
            running_position_2,
            running_position_3,
            finish_time,
            finish_time_seconds,
            father,
            mother,
            gfather
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    insert_preparado = session.prepare(query)
    cantidad = 0

    for fila in filas:
        datos = armar_valores_base(fila)

        if (
                datos["race_id"] is None
                or datos["finishing_position"] is None
                or datos["horse_id"] is None
        ):
            continue

        valores = [
            datos["race_id"],
            datos["finishing_position"],
            datos["horse_id"],
            datos["horse_number"],
            datos["horse_name"],
            datos["jockey"],
            datos["trainer"],
            datos["actual_weight"],
            datos["declared_horse_weight"],
            datos["draw"],
            datos["running_position_1"],
            datos["running_position_2"],
            datos["running_position_3"],
            datos["finish_time"],
            datos["finish_time_seconds"],
            datos["father"],
            datos["mother"],
            datos["gfather"],
        ]

        session.execute(insert_preparado, valores)
        cantidad += 1

    print(f"Se insertaron {cantidad} registros en resultados_por_carrera.")


def importar_historial_por_caballo(session, filas):
    query = """
        INSERT INTO historial_por_caballo (
            horse_id,
            race_id,
            finishing_position,
            horse_number,
            horse_name,
            jockey,
            trainer,
            actual_weight,
            declared_horse_weight,
            draw,
            running_position_1,
            running_position_2,
            running_position_3,
            finish_time,
            finish_time_seconds,
            father,
            mother,
            gfather
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    insert_preparado = session.prepare(query)
    cantidad = 0

    for fila in filas:
        datos = armar_valores_base(fila)

        if datos["horse_id"] is None or datos["race_id"] is None:
            continue

        valores = [
            datos["horse_id"],
            datos["race_id"],
            datos["finishing_position"],
            datos["horse_number"],
            datos["horse_name"],
            datos["jockey"],
            datos["trainer"],
            datos["actual_weight"],
            datos["declared_horse_weight"],
            datos["draw"],
            datos["running_position_1"],
            datos["running_position_2"],
            datos["running_position_3"],
            datos["finish_time"],
            datos["finish_time_seconds"],
            datos["father"],
            datos["mother"],
            datos["gfather"],
        ]

        session.execute(insert_preparado, valores)
        cantidad += 1

    print(f"Se insertaron {cantidad} registros en historial_por_caballo.")


def importar_historial_por_jockey(session, filas):
    query = """
        INSERT INTO historial_por_jockey (
            jockey,
            race_id,
            horse_id,
            finishing_position,
            horse_number,
            horse_name,
            trainer,
            actual_weight,
            declared_horse_weight,
            draw,
            running_position_1,
            running_position_2,
            running_position_3,
            finish_time,
            finish_time_seconds,
            father,
            mother,
            gfather
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    insert_preparado = session.prepare(query)
    cantidad = 0

    for fila in filas:
        datos = armar_valores_base(fila)

        if datos["jockey"] is None or datos["race_id"] is None or datos["horse_id"] is None:
            continue

        valores = [
            datos["jockey"],
            datos["race_id"],
            datos["horse_id"],
            datos["finishing_position"],
            datos["horse_number"],
            datos["horse_name"],
            datos["trainer"],
            datos["actual_weight"],
            datos["declared_horse_weight"],
            datos["draw"],
            datos["running_position_1"],
            datos["running_position_2"],
            datos["running_position_3"],
            datos["finish_time"],
            datos["finish_time_seconds"],
            datos["father"],
            datos["mother"],
            datos["gfather"],
        ]

        session.execute(insert_preparado, valores)
        cantidad += 1

    print(f"Se insertaron {cantidad} registros en historial_por_jockey.")


def importar_caballos_por_entrenador(session, filas):
    query = """
        INSERT INTO caballos_por_entrenador (
            trainer,
            horse_name,
            horse_id,
            race_id,
            finishing_position,
            jockey,
            horse_number,
            actual_weight,
            declared_horse_weight,
            draw,
            running_position_1,
            running_position_2,
            running_position_3,
            finish_time,
            finish_time_seconds,
            father,
            mother,
            gfather
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    insert_preparado = session.prepare(query)
    cantidad = 0

    for fila in filas:
        datos = armar_valores_base(fila)

        if (
                datos["trainer"] is None
                or datos["horse_name"] is None
                or datos["horse_id"] is None
                or datos["race_id"] is None
        ):
            continue

        valores = [
            datos["trainer"],
            datos["horse_name"],
            datos["horse_id"],
            datos["race_id"],
            datos["finishing_position"],
            datos["jockey"],
            datos["horse_number"],
            datos["actual_weight"],
            datos["declared_horse_weight"],
            datos["draw"],
            datos["running_position_1"],
            datos["running_position_2"],
            datos["running_position_3"],
            datos["finish_time"],
            datos["finish_time_seconds"],
            datos["father"],
            datos["mother"],
            datos["gfather"],
        ]

        session.execute(insert_preparado, valores)
        cantidad += 1

    print(f"Se insertaron {cantidad} registros en caballos_por_entrenador.")


def importar_caballos_por_padre(session, filas):
    query = """
        INSERT INTO caballos_por_padre (
            father,
            horse_name,
            horse_id,
            race_id,
            finishing_position,
            jockey,
            trainer,
            horse_number,
            actual_weight,
            declared_horse_weight,
            draw,
            running_position_1,
            running_position_2,
            running_position_3,
            finish_time,
            finish_time_seconds,
            mother,
            gfather
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    insert_preparado = session.prepare(query)
    cantidad = 0

    for fila in filas:
        datos = armar_valores_base(fila)

        if (
                datos["father"] is None
                or datos["horse_name"] is None
                or datos["horse_id"] is None
                or datos["race_id"] is None
        ):
            continue

        valores = [
            datos["father"],
            datos["horse_name"],
            datos["horse_id"],
            datos["race_id"],
            datos["finishing_position"],
            datos["jockey"],
            datos["trainer"],
            datos["horse_number"],
            datos["actual_weight"],
            datos["declared_horse_weight"],
            datos["draw"],
            datos["running_position_1"],
            datos["running_position_2"],
            datos["running_position_3"],
            datos["finish_time"],
            datos["finish_time_seconds"],
            datos["mother"],
            datos["gfather"],
        ]

        session.execute(insert_preparado, valores)
        cantidad += 1

    print(f"Se insertaron {cantidad} registros en caballos_por_padre.")


def importar_mejores_tiempos_por_carrera(session, filas):
    query = """
        INSERT INTO mejores_tiempos_por_carrera (
            race_id,
            finish_time_seconds,
            horse_id,
            horse_name,
            finishing_position,
            horse_number,
            jockey,
            trainer,
            actual_weight,
            declared_horse_weight,
            draw,
            running_position_1,
            running_position_2,
            running_position_3,
            finish_time,
            father,
            mother,
            gfather
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    insert_preparado = session.prepare(query)
    cantidad = 0

    for fila in filas:
        datos = armar_valores_base(fila)

        if (
                datos["race_id"] is None
                or datos["finish_time_seconds"] is None
                or datos["horse_id"] is None
        ):
            continue

        valores = [
            datos["race_id"],
            datos["finish_time_seconds"],
            datos["horse_id"],
            datos["horse_name"],
            datos["finishing_position"],
            datos["horse_number"],
            datos["jockey"],
            datos["trainer"],
            datos["actual_weight"],
            datos["declared_horse_weight"],
            datos["draw"],
            datos["running_position_1"],
            datos["running_position_2"],
            datos["running_position_3"],
            datos["finish_time"],
            datos["father"],
            datos["mother"],
            datos["gfather"],
        ]

        session.execute(insert_preparado, valores)
        cantidad += 1

    print(f"Se insertaron {cantidad} registros en mejores_tiempos_por_carrera.")