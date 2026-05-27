#Tiempo promedio de carrera de todos los caballos

def promedio_tiempo_todos(collection):
    try:
        query = {}
        proyeccion = {"finish_time_seconds": 1, "_id": 0}
        
        resultados = list(collection.find(query, proyeccion))
        
        if not resultados:
            print("No se encontraron resultados para poder calcular el promedio.")
        else:
            suma_tiempos = 0
            cantidad_caballos = 0
            for caballo in resultados:
                if 'finish_time_seconds' in caballo:
                    suma_tiempos += caballo['finish_time_seconds']
                    cantidad_caballos += 1
            
            if cantidad_caballos > 0:
                promedio = suma_tiempos / cantidad_caballos
                print(f"El tiempo promedio de carrera de todos los caballos fue de: {promedio:.2f} segundos")
            else:
                print("No hay tiempos válidos para promediar.")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")

#Tiempo promedio de carrera de los caballos entrenados por P F YIU
def promedio_tiempo_entrenador(collection):
    try:
        query = {"trainer": {"$regex": "P.*F.*YIU", "$options": "i"}}
        proyeccion = {"finish_time_seconds": 1, "_id": 0}
        
        resultados = list(collection.find(query, proyeccion))
        
        if not resultados:
            print("No se encontraron resultados de caballos entrenados por P F YIU.")
        else:
            suma_tiempos = 0
            cantidad_caballos = 0
        
            for caballo in resultados:
                if 'finish_time_seconds' in caballo:
                    suma_tiempos += caballo['finish_time_seconds']
                    cantidad_caballos += 1
            
            if cantidad_caballos > 0:
                promedio = suma_tiempos / cantidad_caballos
                print(f"El tiempo promedio de los caballos entrenados por P F YIU fue de: {promedio:.2f} segundos")
            else:
                print("No hay tiempos válidos para promediar.")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")

#Todos los caballos con numero 10 y que el tiempo de carrera es menor a 1.22.70
def caballos_diez_tiempo(collection):
    try:
        query = {
            "horse_number": 10,
            "finish_time_seconds": { "$lt": 82.70 }
        }
        nombres_no_repetidos = collection.distinct ("horse_name", query)
        
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            print(f"\nLos caballos con el numero 10 y tiempo menor a 1.22.70 fueron: {len(nombres_no_repetidos)}")
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
            
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
            print(f"\nLos caballos que comienzan con la letra A son: {len(nombres_no_repetidos)}")            
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
            
    except Exception as e:
        print(f"Error en la consulta: {e}")

#TOP 10 de tiempos

def top_10_tiempos(collection):
    try:
        query = {}
        proyeccion = {
            "horse_name": 1,
            "finish_time": 1,
            "_id": 0
        }
        resultados = collection.find(query, proyeccion).sort("finish_time_seconds").limit(10)
        
        print("El top 10 de los caballos más rápidos:")
        
        posicion = 1
        for caballo in resultados:
            print(f"Puesto {posicion}: El caballo {caballo['horse_name']} con un tiempo de: {caballo['finish_time']}")
            posicion += 1
            
    except Exception as e:
        print(f"Error en la consulta: {e}")