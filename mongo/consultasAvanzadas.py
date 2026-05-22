#Tiempo promedio de carrera de todos los caballos

#Tiempo promedio de carrera de los caballos entrenados por P F YIU

#Todos los caballos con numero 1o0y que el tiempo de carrera es menor a 1.22.70
def caballos_diez_tiempo(collection):
    try:
        query = {
            "horse_number": "10",
            "finish_time": { "$lt": "1.22.70" }
        }
        nombres_no_repetidos = collection.distinct ("horse_name", query)
        
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
            print(f"\nCaballos con el numero 10 y tiempo menor a 1.22.70 {len(nombres_no_repetidos)}")
            
    except Exception as e:
        print(f"Error en la consulta: {e}")

#Listar todos los caballos que su nombre comience con la letra A

def caballosConA (collection):
    try:
        query = {
            "horse_name": { "$regex": "^A"}
        }
        nombres_no_repetidos = collection.distinct ("horse_name", query)
        
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
            print(f"\nCaballos que comiencen con la letra A: {len(nombres_no_repetidos)}")
            
    except Exception as e:
        print(f"Error en la consulta: {e}")

#TOP 10 de tiempos

'''def top_10_tiempos(collection):
    try:
        query = {}
        proyeccion = {
            "horse_name": 1,
            "finish_time": 1,
            "_id": 0
        }
        resultados = collection.find(query, proyeccion).sort("finish_time", 1).limit(10)
        
        print("TOP 10 de los tiempos más rápidos:")
        
        posicion = 1
        for caballo in resultados:
            print(f"Puesto {posicion}: {caballo}")
            posicion += 1
            
    except Exception as e:
        print(f"Error en la consulta: {e}")'''