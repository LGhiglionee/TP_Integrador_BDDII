from consultasBasicas import *
from consultasAvanzadas import *

def mostrarMenu(collection):
        opcion = 0
        while opcion != 2:
            print("\n --- Consultas en MongoDB ---")
            print("1.Realizar consultas simples.")
            print("2.Realizar consultas complejas.")
            try:
                opcion = int(input("\nSeleccione una opción: "))
                if opcion == 1: mostrarMenuBasicas (collection)
                if opcion == 2: mostrarMenuComplejas (collection)
            except ValueError:
                print ("Debe ingresar un numero.")

def mostrarMenuBasicas (collection):
    opcion = 0
    while opcion != 6:
        print("\n --- Consultas Simples ---")
        print("1.Obtener todos los caballos que sean entrenados P F YIU.")
        print("2.Todos los caballos que ganaron alguna carrera.")
        print("3.Caballos que pesan menos de 1000.")
        print("4.Cantidad de carreras que se corrieron.")
        print("5.Caballos con tiempos menores a 1.23.00.")
        print("6.Buscar historial por caballo.")
        print("7.Volver al menu")
        
        try :        
            opcion = int(input("\nSeleccione una opción: "))    
            if opcion == 1: caballosEntrenadosP_F_YIU(collection)
            if opcion == 2: caballosGanadores (collection)
            if opcion == 3: caballosMenoresDeMil (collection)
            if opcion == 4: cantCarreras (collection)
            if opcion == 5: caballosVeloces(collection)
            if opcion == 6: buscarHistorialCaballo (collection)
            if opcion == 7: mostrarMenu(collection)
            
        except ValueError:
            print ("Debe ingresar un numero.")

def mostrarMenuComplejas (collection):
    opcion = 0
    while opcion != 6:
        print("\n --- Consultas Complejas ---")
        print("1.Tiempo promedio de todos los caballos")
        print("2.Tiempo promedio de carrera de los caballos entrenados por P F YIU")
        print("3.Todos los caballos con numero 10 y que el tiempo de carrera es menor a 1.22.70")
        print("4.Listar todos los caballos que su nombre comience con la letra A")
        print("5.TOP 10 de tiempos")
        print("6.Volver al menu")

        try :
            opcion = int(input("\nSeleccione una opción: "))
            if opcion == 1: promedio_tiempo_todos(collection)
            if opcion == 2: promedio_tiempo_entrenador(collection)
            if opcion == 3: caballos_diez_tiempo(collection)
            if opcion == 4: caballosConA (collection)
            if opcion == 5: top_10_tiempos(collection)
            if opcion == 6: mostrarMenu(collection)

        except ValueError:
            print ("Debe ingresar un numero.")