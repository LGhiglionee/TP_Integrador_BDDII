#Simular carrera en tiempo real.
#Ver ranking actual de una carrera
#Obtener caballo ganador.
#Finalizar carrera
#Actualizar apuestas ganadas/perdidas
#Expirar datos temporales de una carrera
import time
import random

def simularCarrera(redis_db, idCarrera):
    idCarrera = str(idCarrera).strip()

    participantes_key = f"carrera:{idCarrera}:participantes"
    ranking_key = f"carrera:{idCarrera}:ranking"

    participantes = redis_db.smembers(participantes_key)

    if not participantes:
        print("No hay participantes para simular la carrera.")
        return

    for vuelta in range(5):
        print(f"\nVuelta {vuelta + 1}")

        for horse_id in participantes:
            avance = random.randint(1, 10)
            redis_db.zincrby(ranking_key, avance, horse_id)

            caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"
            caballo = redis_db.hgetall(caballo_key)

            print(f"{caballo['horse_name']} avanzo {avance} puntos")

        time.sleep(1)

    print("\nSimulacion finalizada.")

def verRanking(redis_db, idCarrera):
    idCarrera = str(idCarrera).strip()

    ranking_key = f"carrera:{idCarrera}:ranking"
    ranking = redis_db.zrevrange(ranking_key, 0, -1, withscores=True)

    if not ranking:
        print("No hay ranking para esta carrera.")
        return

    print(f"\nRanking de la carrera {idCarrera}:")

    posicion = 1

    for horse_id, puntaje in ranking:
        caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"
        caballo = redis_db.hgetall(caballo_key)

        nombre = caballo.get("horse_name", horse_id)

        print(f"{posicion}. {nombre} - {int(puntaje)} puntos")

        posicion += 1

def obtenerGanador(redis_db, idCarrera):
    idCarrera = str(idCarrera).strip()
    
    ranking_key = f"carrera:{idCarrera}:ranking"
    ganador = redis_db.zrevrange(ranking_key, 0, 0, withscores=True)

    if not ganador:
        print("No hay ganador para esta carrera.")
        return

    horse_id = ganador[0][0]
    puntaje = ganador[0][1]

    caballo_key = f"carrera:{idCarrera}:caballo:{horse_id}"
    caballo = redis_db.hgetall(caballo_key)

    nombre = caballo.get("horse_name", horse_id)

    print(f"Ganador: {nombre} con {int(puntaje)} puntos")
