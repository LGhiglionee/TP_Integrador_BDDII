"""
Módulo de ETL e ingesta masiva para Apache Cassandra.
Implementa pipelines de normalización, limpieza de datos tabulares y pre-agregación
en memoria de la aplicación, utilizando 'Prepared Statements' para maximizar
el rendimiento de escritura secuencial en el clúster distribuido.
"""
import csv
import os

# =======================================================
# AUXILIARES DE NORMALIZACIÓN Y TYPE CASTING
# =======================================================
def convertir_int(valor):
    """
    Sanea cadenas de texto a enteros. Previene excepciones de tipo en el engine
    de Cassandra al procesar números representados como floats con punto flotante ("12.0").
    """
    try:
        return int(float(valor)) if valor not in ("", None) else None
    except:
        return None

def convertir_float(valor):
    """
    Normaliza delimitadores decimales regionales (reemplaza comas por puntos)
    para castear cadenas de texto a tipos de datos numéricos 'double' nativos de CQL.
    """
    try:
        return float(str(valor).replace(",", ".")) if valor not in ("", None) else None
    except:
        return None

def convertir_texto(valor):
    """
    Sanea cadenas eliminando espacios en blanco innecesarios en los extremos,
    evitando discrepancias en el cálculo de hashes de las Partition Keys.
    """
    return str(valor).strip() if valor not in ("", None) else None

def armar_valores_base(fila):
    """
    Capa de abstracción de mapeo intermedio. Extrae el diccionario crudo del CSV
    y retorna un objeto fuertemente tipado listo para interactuar con las tablas.
    """
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
        "finish_time": convertir_texto(fila.get("finish_time")),
        "finish_time_seconds": convertir_float(fila.get("finish_time_seconds")),
        "race_id": convertir_texto(fila.get("race_id")),
    }

# =======================================================
# PIPELINE DE INGESTA GENERAL
# =======================================================
def ImportarDataset(session):
    """
    Controlador central del proceso ETL. Lee el archivo estructurado plano (CSV)
    y distribuye secuencialmente la carga en las 7 familias de columnas optimizadas.
    """
    try:
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(ruta_script, "..", "datasets", "race-result-horse.csv")

        if not os.path.exists(path):
            print(f"No se encontró el archivo CSV en la ruta: {path}")
            return

        with open(path, "r", encoding="UTF-8") as archivo:
            lector = csv.DictReader(archivo, delimiter=";")
            filas = list(lector)

        if not filas:
            print("El archivo CSV está vacío.")
            return

        print(f"Iniciando importación de {len(filas)} filas a las 7 tablas...")

        # Invocación estructurada a los pipelines individuales de carga desnormalizada
        importar_caballos_por_carrera(session, filas)
        importar_caballos(session, filas)
        importar_carreras_por_caballos(session, filas)
        importar_jockey_por_posicion(session, filas)
        importar_entrenador_por_jockey(session, filas)
        importar_tiempo_promedio_por_dupla(session, filas)
        importar_rendimiento_caballo(session, filas)

        print("¡Importación masiva completada en Cassandra!")
    except Exception as e:
        print(f"Se produjo un error al importar en Cassandra: {e}")

# =======================================================
# INGESTAS ESPECÍFICAS (DISEÑO ORIENTADO A CONSULTAS)
# =======================================================
def importar_caballos_por_carrera(session, filas):
    """
    Carga masiva sobre la estructura Wide Row indexada por evento.
    Utiliza session.prepare() para pre-compilar la query en los nodos del clúster,
    lo que reduce drásticamente el overhead de parsing sintáctico en cada iteración.
    """
    query = """INSERT INTO caballos_por_carrera 
               (race_id, finishing_position, horse_id, horse_number, horse_name, declared_horse_weight, draw, finish_time) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    insert_preparado = session.prepare(query)
    cant = 0
    for fila in filas:
        d = armar_valores_base(fila)
        # Validación de Clave Primaria Compuesta: Si falta algún componente, se ignora
        # para evitar corrupciones de registros huérfanos o nulos en las SSTables.
        if d["race_id"] is None or d["finishing_position"] is None or d["horse_id"] is None: continue
        session.execute(insert_preparado, [d["race_id"], d["finishing_position"], d["horse_id"], d["horse_number"], d["horse_name"], d["declared_horse_weight"], d["draw"], d["finish_time"]])
        cant += 1
    print(f"-> {cant} registros en caballos_por_carrera.")

def importar_caballos(session, filas):
    """
    Inyección sobre la tabla maestra dispersa de caballos.
    Saca provecho del particionamiento directo por 'horse_id' para lograr escrituras lineales.
    """
    query = "INSERT INTO caballos (horse_id, horse_number, horse_name, declared_horse_weight) VALUES (?, ?, ?, ?)"
    insert_preparado = session.prepare(query)
    cant = 0
    for fila in filas:
        d = armar_valores_base(fila)
        if d["horse_id"] is None: continue
        session.execute(insert_preparado, [d["horse_id"], d["horse_number"], d["horse_name"], d["declared_horse_weight"]])
        cant += 1
    print(f"-> {cant} registros procesados en caballos.")

def importar_carreras_por_caballos(session, filas):
    """
    Carga de la serie temporal cronológica para análisis por atleta hípico.
    Duplica deliberadamente la información cruzando 'horse_id' con 'race_id'.
    """
    query = """INSERT INTO carreras_por_caballos 
               (horse_id, race_id, horse_name, finishing_time, finishing_position, draw) 
               VALUES (?, ?, ?, ?, ?, ?)"""
    insert_preparado = session.prepare(query)
    cant = 0
    for fila in filas:
        d = armar_valores_base(fila)
        if d["horse_id"] is None or d["race_id"] is None: continue
        session.execute(insert_preparado, [d["horse_id"], d["race_id"], d["horse_name"], d["finish_time"], d["finishing_position"], d["draw"]])
        cant += 1
    print(f"-> {cant} registros en carreras_por_caballos.")

def importar_jockey_por_posicion(session, filas):
    """
    Carga orientada al análisis correlativo entre jockeys y posiciones.
    Calcula en caliente variables derivadas del negocio (diferencia entre gateras y puesto real)
    del lado del cliente para guardarla ya precalculada en la estructura física del disco.
    """
    query = """INSERT INTO jockey_por_posicion_final_del_caballo 
               (horse_id, finishing_position, finish_time_seconds, jockey, diferencia, draw) 
               VALUES (?, ?, ?, ?, ?, ?)"""
    insert_preparado = session.prepare(query)
    cant = 0
    for fila in filas:
        d = armar_valores_base(fila)
        if d["horse_id"] is None or d["finishing_position"] is None or d["finish_time_seconds"] is None: continue
        fts_int = int(d["finish_time_seconds"]) 

        posicion_final = d["finishing_position"]
        draw = d["draw"]
        
        if draw is not None:
            diferencia = draw - posicion_final
        else:
            diferencia = None

        session.execute(insert_preparado, [d["horse_id"], d["finishing_position"], fts_int, d["jockey"], diferencia, d["draw"]])
        cant += 1
    print(f"-> {cant} registros en jockey_por_posicion_final_del_caballo.")

def importar_entrenador_por_jockey(session, filas):
    """
    Pobla la estructura desnormalizada de duplas profesionales.
    Organiza el orden físico por tiempos internos utilizando clustering keys de velocidad.
    """
    query = """INSERT INTO entrenador_por_jockey 
               (jockey, finish_time_seconds, trainer) 
               VALUES (?, ?, ?)"""
    insert_preparado = session.prepare(query)
    cant = 0
    for fila in filas:
        d = armar_valores_base(fila)
        if d["jockey"] is None or d["finish_time_seconds"] is None: continue
        fts_int = int(d["finish_time_seconds"])
        session.execute(insert_preparado, [d["jockey"], fts_int, d["trainer"]])
        cant += 1
    print(f"-> {cant} registros en entrenador_por_jockey.")

def importar_tiempo_promedio_por_dupla(session, filas):
    """
    Dado que las bases de datos masivas distribuidas sufren penalizaciones críticas al calcular
    promedios globales en tiempo de consulta, este pipeline utiliza diccionarios de Python
    para calcular los promedios en la RAM de la aplicación, inyectando únicamente el valor consolidado
    en la Clave de Partición Compuesta ((jockey, trainer)).
    """
    duplas = {}
    for fila in filas:
        d = armar_valores_base(fila)
        j, t, fts = d["jockey"], d["trainer"], d["finish_time_seconds"]
        if j and t and fts is not None:
            clave = (j, t)
            if clave not in duplas:
                duplas[clave] = {'suma': 0, 'count': 0}
            duplas[clave]['suma'] += fts
            duplas[clave]['count'] += 1
            
    query = """INSERT INTO tiempo_promedio_por_dupla 
               (jockey, trainer, promedio_tiempo_final, finish_time_seconds) 
               VALUES (?, ?, ?, ?)"""
    insert_preparado = session.prepare(query)
    cant = 0
    
    for (j, t), stats in duplas.items():
        promedio = int(stats['suma'] / stats['count'])
        session.execute(insert_preparado, [j, t, promedio, promedio])
        cant += 1
    print(f"-> {cant} registros calculados y agrupados en tiempo_promedio_por_dupla.")

def importar_rendimiento_caballo(session, filas):
    """
    Pre-procesamiento analítico de KPIs del atleta hípico.
    Consolida totales, sumatorias de victorias y puestos promedio en memoria del cliente,
    guardando el resultado masticado en 'rendimiento_caballo' para el consumo directo del dashboard.
    """
    caballos = {}
    for fila in filas:
        d = armar_valores_base(fila)
        h, pos = d["horse_id"], d["finishing_position"]
        nombre = d["horse_name"]
        if h and pos is not None:
            if h not in caballos:
                caballos[h] = {'horse_name': nombre,'carreras': 0, 'victorias': 0, 'suma_pos': 0}
            caballos[h]['carreras'] += 1
            caballos[h]['suma_pos'] += pos
            if pos == 1:
                caballos[h]['victorias'] += 1
                
    query = """INSERT INTO rendimiento_caballo 
               (horse_id, horse_name, carreras_corridas, victorias, promedio_posicion) 
               VALUES (?, ?, ?, ?, ?)"""
    insert_preparado = session.prepare(query)
    cant = 0
    for h, stats in caballos.items():
        prom_pos = float(stats['suma_pos'] / stats['carreras'])
        session.execute(insert_preparado, [h, stats['horse_name'], stats['carreras'], stats['victorias'], prom_pos])
        cant += 1
    print(f"-> {cant} registros calculados y agrupados en rendimiento_caballo.")