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

def _obtener_estado_carrera(redis_db, idCarrera):
    carrera_key = f"carrera:{idCarrera}:info"

    if not redis_db.exists(carrera_key):
        return None

    carrera = _normalizar_hash(redis_db.hgetall(carrera_key))
    return carrera.get("estado", "").lower()


def _carrera_bloqueada_para_apuestas(redis_db, idCarrera):
    estado = _obtener_estado_carrera(redis_db, idCarrera)
    return estado in ["finalizada", "cancelada"]

# =========================
# CREATE
# =========================
def crearApuestaManual(redis_db, idCarrera, horse_id, monto):
    idCarrera = str(idCarrera).strip()
    horse_id = str(horse_id).strip()
    monto = str(monto).strip()

    carrera_key = f"carrera:{idCarrera}:info"
    participantes_key = f"carrera:{idCarrera}:participantes"
    apuestas_key = f"carrera:{idCarrera}:apuestas"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe.")
        return

    if _carrera_bloqueada_para_apuestas(redis_db, idCarrera):
        estado = _obtener_estado_carrera(redis_db, idCarrera)
        print(f"No se puede crear una apuesta porque la carrera {idCarrera} está {estado}.")
        return

    participantes = _normalizar_lista(redis_db.smembers(participantes_key))

    if not participantes:
        print(f"No hay participantes cargados para la carrera {idCarrera}.")
        return

    if horse_id not in participantes:
        print(f"El caballo {horse_id} no participa en la carrera {idCarrera}.")
        return

    try:
        monto = float(monto)
    except ValueError:
        print("El monto ingresado no es válido.")
        return

    apuesta_id = redis_db.incr(f"carrera:{idCarrera}:contador_apuestas")
    apuesta_key = f"carrera:{idCarrera}:apuesta:{apuesta_id}"

    redis_db.hset(apuesta_key, mapping={
        "apuesta_id": apuesta_id,
        "horse_id": horse_id,
        "monto": monto,
        "estado": "activa"
    })

    redis_db.sadd(apuestas_key, apuesta_id)

    print(f"Apuesta {apuesta_id} creada correctamente.")
    print(f"Carrera: {idCarrera}")
    print(f"Caballo apostado: {horse_id}")
    print(f"Monto: ${monto}")


# =========================
# READ
# =========================
def buscarApuesta(redis_db, idCarrera, apuesta_id):
    idCarrera = str(idCarrera).strip()
    apuesta_id = str(apuesta_id).strip()

    apuesta_key = f"carrera:{idCarrera}:apuesta:{apuesta_id}"

    if not redis_db.exists(apuesta_key):
        print(f"No existe la apuesta {apuesta_id} para la carrera {idCarrera}.")
        return

    apuesta = _normalizar_hash(redis_db.hgetall(apuesta_key))

    horse_id = apuesta.get("horse_id", "Desconocido")

    caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"
    caballo = _normalizar_hash(redis_db.hgetall(caballo_key))

    nombre_caballo = caballo.get("horse_name", horse_id)

    print(f"\n--- Apuesta {apuesta_id} ---")
    print(f"Carrera: {idCarrera}")
    print(f"Caballo: {nombre_caballo} ({horse_id})")
    print(f"Monto: ${apuesta.get('monto', 0)}")
    print(f"Estado: {apuesta.get('estado', 'desconocido')}")

def buscarCarrera(redis_db, idCarrera):
    idCarrera = str(idCarrera).strip()

    carrera_key = f"carrera:{idCarrera}:info"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe.")
        return

    carrera = _normalizar_hash(redis_db.hgetall(carrera_key))

    print(f"\n--- Carrera {idCarrera} ---")
    print(f"Race ID: {carrera.get('race_id', idCarrera)}")
    print(f"Estado: {carrera.get('estado', 'desconocido')}")
    print(f"Participantes: {carrera.get('cantidad_participantes', 0)}")

    if carrera.get("ganador"):
        print(f"Ganador: {carrera.get('nombre_ganador', carrera.get('ganador'))}")
        print(f"Puntaje ganador: {carrera.get('puntaje_ganador', 0)}")

# =========================
# UPDATE
# =========================
def actualizarEstadoCarrera(redis_db, idCarrera, nuevoEstado):
    idCarrera = str(idCarrera).strip()
    nuevoEstado = str(nuevoEstado).strip().lower()

    carrera_key = f"carrera:{idCarrera}:info"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe.")
        return

    estados_validos = ["creada", "en curso", "finalizada", "cancelada"]

    if nuevoEstado not in estados_validos:
        print("Estado inválido.")
        print(f"Estados permitidos: {', '.join(estados_validos)}")
        return

    redis_db.hset(carrera_key, "estado", nuevoEstado)

    print(f"Estado de la carrera {idCarrera} actualizado correctamente.")
    print(f"Nuevo estado: {nuevoEstado}")

def actualizarApuesta(redis_db, idCarrera, apuesta_id, nuevoMonto=None, nuevoEstado=None):
    idCarrera = str(idCarrera).strip()
    apuesta_id = str(apuesta_id).strip()

    apuesta_key = f"carrera:{idCarrera}:apuesta:{apuesta_id}"

    if not redis_db.exists(apuesta_key):
        print(f"No existe la apuesta {apuesta_id} para la carrera {idCarrera}.")
        return

    if _carrera_bloqueada_para_apuestas(redis_db, idCarrera):
        estado = _obtener_estado_carrera(redis_db, idCarrera)
        print(f"No se puede actualizar la apuesta {apuesta_id} porque la carrera {idCarrera} está {estado}.")
        return

    cambios = {}

    if nuevoMonto is not None and str(nuevoMonto).strip() != "":
        try:
            cambios["monto"] = float(nuevoMonto)
        except ValueError:
            print("El monto ingresado no es válido.")
            return

    if nuevoEstado is not None and str(nuevoEstado).strip() != "":
        nuevoEstado = str(nuevoEstado).strip().lower()

        estados_validos = ["activa", "ganada", "perdida", "cancelada"]

        if nuevoEstado not in estados_validos:
            print("Estado inválido.")
            print(f"Estados permitidos: {', '.join(estados_validos)}")
            return

        cambios["estado"] = nuevoEstado

    if not cambios:
        print("No se ingresaron cambios para actualizar.")
        return

    redis_db.hset(apuesta_key, mapping=cambios)

    print(f"Apuesta {apuesta_id} actualizada correctamente.")

    for campo, valor in cambios.items():
        print(f"{campo}: {valor}")

# =========================
# DELETE
# =========================
def borrarApuesta(redis_db, idCarrera, apuesta_id):
    idCarrera = str(idCarrera).strip()
    apuesta_id = str(apuesta_id).strip()

    apuesta_key = f"carrera:{idCarrera}:apuesta:{apuesta_id}"
    apuestas_key = f"carrera:{idCarrera}:apuestas"

    if not redis_db.exists(apuesta_key):
        print(f"No existe la apuesta {apuesta_id} para la carrera {idCarrera}.")
        return

    redis_db.delete(apuesta_key)
    redis_db.srem(apuestas_key, apuesta_id)

    print(f"Apuesta {apuesta_id} eliminada correctamente de la carrera {idCarrera}.")

def borrarCarrera(redis_db, idCarrera):
    idCarrera = str(idCarrera).strip()

    carrera_key = f"carrera:{idCarrera}:info"
    participantes_key = f"carrera:{idCarrera}:participantes"
    ranking_key = f"carrera:{idCarrera}:ranking"
    apuestas_key = f"carrera:{idCarrera}:apuestas"
    contador_apuestas_key = f"carrera:{idCarrera}:contador_apuestas"

    if not redis_db.exists(carrera_key):
        print(f"La carrera {idCarrera} no existe.")
        return

    participantes = _normalizar_lista(redis_db.smembers(participantes_key))
    apuestas = _normalizar_lista(redis_db.smembers(apuestas_key))

    claves_a_borrar = [
        carrera_key,
        participantes_key,
        ranking_key,
        apuestas_key,
        contador_apuestas_key
    ]

    for horse_id in participantes:
        claves_a_borrar.append(f"carrera:{idCarrera}:caballo:{horse_id}")

    for apuesta_id in apuestas:
        claves_a_borrar.append(f"carrera:{idCarrera}:apuesta:{apuesta_id}")

    redis_db.delete(*claves_a_borrar)

    print(f"Carrera {idCarrera} eliminada correctamente.")
    print(f"Caballos eliminados: {len(participantes)}")
    print(f"Apuestas eliminadas: {len(apuestas)}")