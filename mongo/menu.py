from consultasBasicas import *

def mostrarMenu(collection):

    opcion = 0
    while opcion != 9:
        print("\n --- Consultas Simples ---")
        print("1.Obtener todos los caballos que sean entrenados P F YIU")
        print("2.Todos los caballos que ganaron alguna carrera")
        print("3.Caballos que pesan menos de 1000 ")
        print("4.Cantidad de carreras que se corrieron")
        print("5.Caballos con tiempos menores a 1.23.000 ")
        print("6.Listar todos los codigos de carreras ")

        print ("\n --- Consultas Avanzadas ---")
        print("7.Listar todos los codigos de carreras ")
        
        try :
            opcion = int(input("\nSeleccione una opción: "))
            
            if opcion == 1: caballosEntrenadosP_F_YIU(collection)

        except ValueError:
            print ("Debe ingresar un numero.")

#Tiempo promedio de carrera de todos los caballos

#Tiempo promedio de carrera de los caballos entrenados por P F YIU

#Todos los caballos con numero 1o y que el tiempo de carrera es menor a 1.22.70

#Listar todos los caballos que su nombre comience con la letra A

