"""
Módulo de lógica de simulación y gestión de estado en tiempo real para Redis.
Utiliza estructuras de datos avanzadas como Sorted Sets y Hashes,
permitiendo una latencia mínima en la simulación.
"""
import time
import random

# =========================
# AUXILIARES DE NORMALIZACIÓN
# =========================
# Redis devuelve bytes; estas funciones aseguran que los datos sean legibles como strings
def _normalizar_valor(valor):
    if isinstance(valor, bytes):
        return valor.decode("utf-8")
    return str(valor)

def _normalizar_hash(hash_redis):
    return {
        _normalizar_valor(k): _normalizar_valor(v)
        for k, v in hash_redis.items()
    }

def _normalizar_lista(valores):
    return [_normalizar_valor(v) for v in valores]

# =========================
# LÓGICA DE SIMULACIÓN
# =========================
def simularCarrera(redis_db, idCarrera):
    """
    Simulación de alta concurrencia: utiliza ZINCRBY sobre un Sorted Set (ranking)
    para actualizar puntajes atómicamente en memoria conforme los caballos avanzan.
    """
    idCarrera = str(idCarrera).strip()

    carrera_key = f"carrera:{idCarrera}:info"
    participantes_key = f"carrera:{idCarrera}:participantes"
    ranking_key = f"carrera:{idCarrera}:ranking"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe.")
        return

    participantes = _normalizar_lista(redis_db.smembers(participantes_key))
    if not participantes:
        print("No hay participantes para simular la carrera.")
        return

    redis_db.hset(carrera_key, "estado", "en curso")

    for vuelta in range(5):
        print(f"\nVuelta {vuelta + 1}")

        for horse_id in participantes:
            avance = random.randint(1, 10)
            # ZINCRBY: Incrementa el puntaje del caballo en el ranking de forma atómica y ultra rápida
            redis_db.zincrby(ranking_key, avance, horse_id)

            caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"
            caballo = _normalizar_hash(redis_db.hgetall(caballo_key))
            nombre = caballo.get("horse_name", horse_id)

            print(f"{nombre} avanzó {avance} puntos")

        time.sleep(1)

    print("\nSimulación finalizada.")

def verRanking(redis_db, idCarrera):
    """
    Consulta de ranking en tiempo real: usa ZREVRANGE para obtener a los caballos
    ordenados por puntaje (descendente) de manera inmediata.
    """
    idCarrera = str(idCarrera).strip()

    ranking_key = f"carrera:{idCarrera}:ranking"
    # ZREVRANGE: Permite obtener el top N de la tabla de posiciones con complejidad O(log(N))
    ranking = redis_db.zrevrange(ranking_key, 0, -1, withscores=True)

    if not ranking:
        print("No hay ranking para esta carrera.")
        return

    print(f"\nRanking de la carrera {idCarrera}:")

    posicion = 1
    for horse_id, puntaje in ranking:
        horse_id = _normalizar_valor(horse_id)

        caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"
        caballo = _normalizar_hash(redis_db.hgetall(caballo_key))
        nombre = caballo.get("horse_name", horse_id)

        print(f"{posicion}. {nombre} - {int(puntaje)} puntos")
        posicion += 1


def obtenerGanador(redis_db, idCarrera):
    """
    Identifica al ganador de la carrera mediante un acceso directo al índice superior
    del Sorted Set. Es una operación de tiempo constante para la recuperación del
    líder.
    """
    idCarrera = str(idCarrera).strip()

    ranking_key = f"carrera:{idCarrera}:ranking"

    # ZREVRANGE permite obtener el elemento con el puntaje más alto (índice 0) sin tener que ordenar todo el conjunto manualmente.
    ganador = redis_db.zrevrange(ranking_key, 0, 0, withscores=True)

    if not ganador:
        print("No hay ganador para esta carrera.")
        return

    # Extracción del ID y puntaje desde la estructura de datos
    horse_id = _normalizar_valor(ganador[0][0])
    puntaje = ganador[0][1]

    # HGETALL recupera todos los campos del caballo ganador como un hash/diccionario
    caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"
    caballo = _normalizar_hash(redis_db.hgetall(caballo_key))
    nombre = caballo.get("horse_name", horse_id)

    print(f"Ganador: {nombre} con {int(puntaje)} puntos")


def finalizarCarrera(redis_db, idCarrera):
    """
    Persistencia de estado: Cambia el hash de info de la carrera a 'finalizada'
    y guarda los datos del ganador permanentemente en la estructura HASH.
    """
    idCarrera = str(idCarrera).strip()

    carrera_key = f"carrera:{idCarrera}:info"
    ranking_key = f"carrera:{idCarrera}:ranking"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe.")
        return

    ganador = redis_db.zrevrange(ranking_key, 0, 0, withscores=True)

    if not ganador:
        print(f"No hay ranking cargado para la carrera {idCarrera}.")
        return

    horse_id_ganador = _normalizar_valor(ganador[0][0])
    puntaje = ganador[0][1]

    caballo_key = f"carrera:{idCarrera}:caballo:{horse_id_ganador}"
    caballo = _normalizar_hash(redis_db.hgetall(caballo_key))

    nombre_ganador = caballo.get("horse_name", horse_id_ganador)

    redis_db.hset(carrera_key, "estado", "finalizada")
    redis_db.hset(carrera_key, "ganador", horse_id_ganador)
    redis_db.hset(carrera_key, "nombre_ganador", nombre_ganador)
    redis_db.hset(carrera_key, "puntaje_ganador", int(puntaje))

    print(f"\nCarrera {idCarrera} finalizada.")
    print(f"Ganador: {nombre_ganador} con {int(puntaje)} puntos.")


def actualizarApuestas(redis_db, idCarrera):
    """
    Gestión de estado de apuestas: Itera sobre los miembros de un SET (apuestas),
    compara el caballo apostado contra el ganador, y actualiza el estado de cada apuesta.
    """
    idCarrera = str(idCarrera).strip()

    carrera_key = f"carrera:{idCarrera}:info"
    apuestas_key = f"carrera:{idCarrera}:apuestas"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe.")
        return

    carrera = _normalizar_hash(redis_db.hgetall(carrera_key))
    horse_id_ganador = carrera.get("ganador")

    estado = carrera.get("estado", "").lower()

    if estado != "finalizada":
        print(f"No se pueden actualizar las apuestas porque la carrera {idCarrera} no está finalizada.")
        print(f"Estado actual: {estado}")
        return

    if not horse_id_ganador:
        print("La carrera todavía no tiene ganador. Primero debe finalizarse.")
        return

    # SMEMBERS: Extrae todos los IDs de apuestas rápidamente para procesamiento posterior
    apuestas = _normalizar_lista(redis_db.smembers(apuestas_key))

    if not apuestas:
        print(f"No hay apuestas para actualizar en la carrera {idCarrera}.")
        return

    ganadas = 0
    perdidas = 0

    for apuesta_id in apuestas:
        apuesta_key = f"carrera:{idCarrera}:apuesta:{apuesta_id}"
        apuesta = _normalizar_hash(redis_db.hgetall(apuesta_key))

        horse_id_apostado = apuesta.get("horse_id")

        if horse_id_apostado == horse_id_ganador:
            redis_db.hset(apuesta_key, "estado", "ganada")
            ganadas += 1
        else:
            redis_db.hset(apuesta_key, "estado", "perdida")
            perdidas += 1

    print(f"\nApuestas actualizadas para la carrera {idCarrera}.")
    print(f"Apuestas ganadas: {ganadas}")
    print(f"Apuestas perdidas: {perdidas}")

def expirarDatosCarrera(redis_db, idCarrera):
    """
    Gestión de memoria eficiente: Implementa el ciclo de vida de los datos (TTL).
    Marca todas las claves relacionadas para su eliminación automática tras 20s,
    evitando que la memoria RAM de Redis se sature con datos de carreras pasadas.
    """
    idCarrera = str(idCarrera).strip()

    segundos_expiracion = 20

    participantes_key = f"carrera:{idCarrera}:participantes"
    ranking_key = f"carrera:{idCarrera}:ranking"
    carrera_key = f"carrera:{idCarrera}:info"
    apuestas_key = f"carrera:{idCarrera}:apuestas"
    contador_apuestas_key = f"carrera:{idCarrera}:contador_apuestas"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe.")
        return

    # EXPIRE: Comando fundamental de Redis para delegar la limpieza de basura al motor
    redis_db.expire(carrera_key, segundos_expiracion)
    redis_db.expire(participantes_key, segundos_expiracion)
    redis_db.expire(ranking_key, segundos_expiracion)
    redis_db.expire(apuestas_key, segundos_expiracion)
    redis_db.expire(contador_apuestas_key, segundos_expiracion)

    participantes = _normalizar_lista(redis_db.smembers(participantes_key))

    for horse_id in participantes:
        caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"
        redis_db.expire(caballo_key, segundos_expiracion)

    apuestas = _normalizar_lista(redis_db.smembers(apuestas_key))

    for apuesta_id in apuestas:
        apuesta_key = f"carrera:{idCarrera}:apuesta:{apuesta_id}"
        redis_db.expire(apuesta_key, segundos_expiracion)

    print(f"Los datos de la carrera {idCarrera} expirarán en {segundos_expiracion} segundos.")