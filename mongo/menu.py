from consultasBasicas import *

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
        
        try :        
            opcion = int(input("\nSeleccione una opción: "))    
            if opcion == 1: caballosEntrenadosP_F_YIU(collection)
            if opcion == 2: caballosGanadores (collection)
            if opcion == 3: caballosMenoresDeMil (collection)
            if opcion == 4: cantCarreras (collection)
            if opcion == 5: caballosVeloces(collection)
            if opcion == 6: buscarHistorialCaballo (collection)
        except ValueError:
            print ("Debe ingresar un numero.")

def mostrarMenuComplejas (collection):
        opcion = 0
        while opcion != 6:
            print("\n --- Consultas Complejas ---")
        
    
#Tiempo promedio de carrera de todos los caballos

#Tiempo promedio de carrera de los caballos entrenados por P F YIU

#Todos los caballos con numero 1o y que el tiempo de carrera es menor a 1.22.70

#Listar todos los caballos que su nombre comience con la letra A

