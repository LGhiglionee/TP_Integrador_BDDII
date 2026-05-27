from consultasBasicas import *
from consultasAvanzadas import *
from simulacionCarrera import *

def mostrarMenuRedis(redis_db):

    print("\nRedis conectado correctamente.")
    opcion = 0

    while opcion != 3:
        print("\n--- Consultas en Redis ---")
        print("1. Realizar consultas simples.")
        print("2. Realizar consultas avanzadas.")
        print("3. Salir.")

        try:
            opcion = int(input("\nSeleccione una opción: "))

            if opcion == 1:
                mostrarMenuBasicasRedis(redis_db)

            if opcion == 2:
                mostrarMenuAvanzadasRedis(redis_db)

        except ValueError:
            print("Debe ingresar un número.")


def mostrarMenuBasicasRedis(redis_db):
    opcion = 0

    while opcion != 7:
        print("\n--- Consultas Simples Redis ---")
        print("1. Crear carrera.")
        print("2. Cargar caballos de prueba.")
        print("3. Generar apuestas ficticias.")
        print("4. Ver estado de una carrera.")
        print("5. Ver participantes de una carrera.")
        print("6. Ver apuestas activas de una carrera.")
        print("7. Salir.")

        try:
            opcion = int(input("\nSeleccione una opción: "))

            if opcion == 1:
                idCarrera = int(input("Ingrese ID de carrera: "))
                crearCarrera(redis_db, idCarrera)

            if opcion == 2:
                idCarrera = int(input("Ingrese ID de carrera: "))
                cargarCaballosPrueba(redis_db, idCarrera)

            if opcion == 3:
                idCarrera = int(input("Ingrese ID de carrera: "))
                cantidadApuestas = int(input("Ingrese cantidad de apuestas ficticias: "))
                generarApuestasFicticias(redis_db, idCarrera, cantidadApuestas)

            if opcion == 4:
                idCarrera = int(input("Ingrese ID de carrera: "))
                verEstadoCarrera(redis_db, idCarrera)

            if opcion == 5:
                idCarrera = int(input("Ingrese ID de carrera: "))
                verParticipantes(redis_db, idCarrera)

            if opcion == 6:
                idCarrera = int(input("Ingrese ID de carrera: "))
                verApuestasActivas(redis_db, idCarrera)

        except ValueError:
            print("Debe ingresar un número.")


def mostrarMenuAvanzadasRedis(redis_db):
    opcion = 0

    while opcion != 7:
        print("\n--- Consultas Avanzadas Redis ---")
        print("1. Simular carrera en tiempo real.")
        print("2. Ver ranking actual de una carrera.")
        print("3. Obtener caballo ganador.")
        print("4. Finalizar carrera.")
        print("5. Actualizar apuestas ganadas/perdidas.")
        print("6. Expirar datos temporales de una carrera.")
        print("7. Salir.")

        try:
            opcion = int(input("\nSeleccione una opción: "))

            if opcion == 1:
                idCarrera = int(input("Ingrese ID de carrera: "))
                simularCarrera(redis_db, idCarrera)

            if opcion == 2:
                idCarrera = int(input("Ingrese ID de carrera: "))
                verRanking(redis_db, idCarrera)

            if opcion == 3:
                idCarrera = int(input("Ingrese ID de carrera: "))
                obtenerGanador(redis_db, idCarrera)

            if opcion == 4:
                idCarrera = int(input("Ingrese ID de carrera: "))
                finalizarCarrera(redis_db, idCarrera)

            if opcion == 5:
                idCarrera = int(input("Ingrese ID de carrera: "))
                actualizarApuestas(redis_db, idCarrera)

            if opcion == 6:
                idCarrera = int(input("Ingrese ID de carrera: "))
                expirarDatosCarrera(redis_db, idCarrera)

        except ValueError:
            print("Debe ingresar un número.")