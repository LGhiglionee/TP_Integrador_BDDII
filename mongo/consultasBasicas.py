#Obtener todos los caballos que sean entrenados P F YIU

def caballosEntrenadosP_F_YIU(collection):
    try:
        query = {"trainer": {"$regex": "P.*F.*YIU", "$options": "i"}}
        nombres_no_repetidos = collection.distinct("horse_name", query)
        
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
            print(f"\nTotal de caballos entrenados por P F YIU: {len(nombres_no_repetidos)}")
            
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
#Todos los caballos que ganaron alguna carrera
def caballosGanadores (collection):
    try:
        query = {"finishing_position":1}
        nombres_no_repetidos = collection.distinct ("horse_name", query)
        
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
            print(f"\nTotal de caballos ganadores: {len(nombres_no_repetidos)}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
#Caballos que pesan menos de la media.
def caballosMenoresDeMil (collection):
    try:
        query = {"declared_horse_weight" : {"$lt" : 1000}}
        nombres_no_repetidos = collection.distinct ("horse_name", query)
        
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
            print(f"\nTotal de caballos que pesan menos de 1000 libras: {len(nombres_no_repetidos)}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
#Cantidad de carreras que se corrieron
def cantCarreras (collection):
    try:
        races_unicas = collection.distinct("race_id")
        total = len(races_unicas)
        print(f"Cantidad total de carreras que se corrieron: {total}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")

#Caballos con finish_time menor a 1.23.00 
def caballosVeloces (collection):
    try:
        query = {"finish_time_seconds": {"$lt" : 83.00}}

        nombres_no_repetidos = collection.distinct ("horse_name", query)
        
        if not nombres_no_repetidos:
                print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
            print(f"\nTotal de caballos que llegaron con tiempo menor a 1 minuto 23 segundos: {len(nombres_no_repetidos)}")
                                    
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
#Buscar historial caballo
def buscarHistorialCaballo (collection):
    nombre = input ("\n Ingresar nombre del caballo que se quiere conocer la información:").upper().strip()
    # Total de carreras jugadas.
    total_carreras = collection.count_documents({"horse_name": nombre})
    print("-" * 40)
    print(f"\n Total de carreras jugadas por {nombre}: {total_carreras}")
    if total_carreras == 0:
            print(f"\nNo se encontraron registros para el caballo: {nombre}")
            return
    # Total de carreras ganadas.
    ganadas = collection.count_documents({
            "horse_name": nombre, 
            "finishing_position": 1
        })
    print("-" * 40)
    print(f"\n Total de carreras ganadas por {nombre} : {ganadas}")

    efectividad = (ganadas / total_carreras) * 100
    print("-" * 40)
    print(f"Efectividad de victoria: {efectividad:.2f}%")

    # Total de carreras que corrió menos de 1 minuto.
    rapidas = collection.count_documents ({
        "horse_name": nombre,
        "finish_time_seconds": {
            "$lt": 60}
        })
    print("-" * 40)
    print(f"\n Total de carreras con buenos tiempos de {nombre} :{rapidas}")    
