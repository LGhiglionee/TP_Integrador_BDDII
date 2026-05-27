#ver estado de carrera
#ver participantes
#ver apuesta puntual
import random
from conectarRedis import leerDataset

#crear carrera + cargar caballos
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
        horse_id = caballo["horse_id"]
        caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"

        redis_db.hset(caballo_key, mapping=caballo)
        redis_db.sadd(participantes_key, horse_id)
        redis_db.zadd(ranking_key, {horse_id: 0})

    print(f"Carrera {idCarrera} creada con {len(caballos)} caballos.")

#crear apuestas
def generarApuestasFicticias(redis_db, idCarrera, cantidadApuestas):
    idCarrera = str(idCarrera).strip()

    participantes_key = f"carrera:{idCarrera}:participantes"
    apuestas_key = f"carrera:{idCarrera}:apuestas"

    participantes = list(redis_db.smembers(participantes_key))

    if not participantes:
        print("No hay participantes para generar apuestas.")
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
