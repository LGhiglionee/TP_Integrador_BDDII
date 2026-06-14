import random
from motor_redis.conectarRedis import leerDataset

# =========================
# AUXILIARES
# =========================

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

def _preparar_mapping(diccionario):
    return {
        str(k): "" if v is None else str(v)
        for k, v in diccionario.items()
    }

# =========================
# CREAR CARRERA + CARGAR CABALLOS
# =========================
def crearCarrera(redis_db, idCarrera):
    idCarrera = str(idCarrera).strip()

    carrera_key = f"carrera:{idCarrera}:info"
    participantes_key = f"carrera:{idCarrera}:participantes"
    ranking_key = f"carrera:{idCarrera}:ranking"

    if redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} ya existe.")
        return

    caballos = list(leerDataset(filtros={"race_id": idCarrera}))

    if not caballos:
        print(f"No se encontraron caballos para la carrera {idCarrera}.")
        return

    redis_db.hset(carrera_key, mapping={
        "race_id": idCarrera,
        "estado": "creada",
        "cantidad_participantes": len(caballos)
    })

    for caballo in caballos:
        horse_id = str(caballo["horse_id"]).strip()
        caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"

        redis_db.hset(caballo_key, mapping=_preparar_mapping(caballo))
        redis_db.sadd(participantes_key, horse_id)
        redis_db.zadd(ranking_key, {horse_id: 0})

    print(f"Carrera {idCarrera} creada con {len(caballos)} caballos.")


# =========================
# CREAR APUESTAS FICTICIAS
# =========================
# =========================
# CREAR APUESTAS FICTICIAS
# =========================

def generarApuestasFicticias(redis_db, idCarrera, cantidadApuestas):
    idCarrera = str(idCarrera).strip()

    try:
        cantidadApuestas = int(cantidadApuestas)
    except ValueError:
        print("La cantidad de apuestas debe ser un número entero.")
        return

    carrera_key = f"carrera:{idCarrera}:info"
    participantes_key = f"carrera:{idCarrera}:participantes"
    apuestas_key = f"carrera:{idCarrera}:apuestas"

    # Valida que la carrera exista antes de generar apuestas.
    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe.")
        print("Primero debe crear la carrera desde la opción 'Crear una carrera'.")
        return

    carrera = _normalizar_hash(redis_db.hgetall(carrera_key))
    estado = carrera.get("estado", "").lower()

    # No permite generar apuestas si la carrera ya terminó o fue cancelada.
    if estado in ["finalizada", "cancelada"]:
        print(f"No se pueden generar apuestas porque la carrera {idCarrera} está {estado}.")
        return

    participantes = _normalizar_lista(redis_db.smembers(participantes_key))

    if not participantes:
        print(f"No hay participantes cargados para la carrera {idCarrera}.")
        return

    for i in range(cantidadApuestas):
        apuesta_id = redis_db.incr(f"carrera:{idCarrera}:contador_apuestas")
        horse_id = random.choice(participantes)
        monto = random.randint(100, 5000)

        apuesta_key = f"carrera:{idCarrera}:apuesta:{apuesta_id}"

        redis_db.hset(apuesta_key, mapping={
            "apuesta_id": apuesta_id,
            "horse_id": horse_id,
            "monto": monto,
            "estado": "activa"
        })

        redis_db.sadd(apuestas_key, apuesta_id)

    print(f"Se generaron {cantidadApuestas} apuestas.")


# =========================
# VER ESTADO DE CARRERA
# =========================
def verEstadoCarrera(redis_db, idCarrera):
    idCarrera = str(idCarrera).strip()

    carrera_key = f"carrera:{idCarrera}:info"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe.")
        return

    carrera = _normalizar_hash(redis_db.hgetall(carrera_key))

    print(f"\n--- Estado de la Carrera {idCarrera} ---")
    print(f"Estado: {carrera.get('estado', 'desconocido')}")
    print(f"Cantidad de participantes: {carrera.get('cantidad_participantes', 0)}")

    if carrera.get("ganador"):
        print(f"Ganador: {carrera.get('nombre_ganador', carrera.get('ganador'))}")
        print(f"Puntaje ganador: {carrera.get('puntaje_ganador', 0)}")


# =========================
# VER PARTICIPANTES
# =========================
def verParticipantes(redis_db, idCarrera):
    idCarrera = str(idCarrera).strip()

    participantes_key = f"carrera:{idCarrera}:participantes"

    participantes = _normalizar_lista(redis_db.smembers(participantes_key))

    if not participantes:
        print(f"No hay participantes para la carrera {idCarrera}.")
        return

    print(f"\n--- Participantes de la carrera {idCarrera} ---")

    for horse_id in participantes:
        caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"
        caballo = _normalizar_hash(redis_db.hgetall(caballo_key))

        nombre = caballo.get("horse_name", "Desconocido")

        print(f"- {nombre} ({horse_id})")

    print(f"\nTotal de participantes: {len(participantes)}")


# =========================
# VER APUESTAS
# =========================
def verApuestasActivas(redis_db, idCarrera):
    idCarrera = str(idCarrera).strip()

    apuestas_key = f"carrera:{idCarrera}:apuestas"

    apuestas = _normalizar_lista(redis_db.smembers(apuestas_key))

    if not apuestas:
        print(f"No hay apuestas para la carrera {idCarrera}.")
        return

    print(f"\n--- Apuestas de la carrera {idCarrera} ---")

    for apuesta_id in apuestas:
        apuesta_key = f"carrera:{idCarrera}:apuesta:{apuesta_id}"
        apuesta = _normalizar_hash(redis_db.hgetall(apuesta_key))

        horse_id = apuesta.get("horse_id", "Desconocido")
        monto = apuesta.get("monto", 0)
        estado = apuesta.get("estado", "desconocido")

        caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"
        caballo = _normalizar_hash(redis_db.hgetall(caballo_key))

        nombre = caballo.get("horse_name", horse_id)

        print(f"Apuesta {apuesta_id}")
        print(f"Caballo: {nombre}")
        print(f"Monto: ${monto}")
        print(f"Estado: {estado}")
        print("-" * 30)