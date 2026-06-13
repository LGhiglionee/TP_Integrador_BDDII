def caballosEntrenadosP_F_YIU(collection):
    try:
        query = {"trainer": {"$regex": "P.*F.*YIU", "$options": "i"}}

        nombres_no_repetidos = collection.distinct("horse_name", query)
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            nombres_no_repetidos = sorted(nombres_no_repetidos)
            print(f"\nEl total de caballos entrenados por P F YIU es {len(nombres_no_repetidos)}")
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
            
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
def caballosGanadores (collection):
    try:
        query = {"finishing_position":1}

        nombres_no_repetidos = collection.distinct ("horse_name", query)
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            nombres_no_repetidos = sorted(nombres_no_repetidos)
            print(f"\nEl total de caballos ganadores es {len(nombres_no_repetidos)}")            
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
def caballosMenoresDeMil (collection):
    try:
        query = {"declared_horse_weight" : {"$lt" : 1000}}

        nombres_no_repetidos = collection.distinct ("horse_name", query)
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            nombres_no_repetidos = sorted(nombres_no_repetidos)
            print(f"\nEl total de caballos que pesan menos de 1000 libras es {len(nombres_no_repetidos)}")
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
def cantCarreras (collection):
    try:
        races_unicas = collection.distinct("race_id")
        total = len(races_unicas)

        print(f"\nLa cantidad total de carreras que se corrieron fue {total}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")

def caballosVeloces (collection):
    try:
        query = {"finish_time_seconds": {"$lt" : 83.00}}

        nombres_no_repetidos = collection.distinct ("horse_name", query)
        if not nombres_no_repetidos:
                print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            nombres_no_repetidos = sorted(nombres_no_repetidos)
            print(f"\nEl total de caballos que llegaron con tiempo menor a 1 minuto 23 segundos es {len(nombres_no_repetidos)}")

            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
                                    
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
def buscarHistorialCaballo (collection):
    try:
        nombre = input ("\n Ingresar nombre del caballo el cual se quiere conocer el historial:").upper().strip()
        # Total de carreras jugadas.
        total_carreras = collection.count_documents({"horse_name": nombre})
        if total_carreras == 0:
                print(f"\nNo se encontraron registros para el caballo: {nombre}")
                return
        print(f"\nEl total de carreras jugadas por {nombre} fue {total_carreras}")
        # Total de carreras ganadas.
        ganadas = collection.count_documents({
                "horse_name": nombre,
                "finishing_position": 1
            })
        print("")
        print(f"El total de carreras ganadas por {nombre} fue {ganadas}")

        efectividad = (ganadas / total_carreras) * 100
        print("")
        print(f"La efectividad de victoria de {nombre} fue {efectividad:.2f}%")

        # Total de carreras que corrió menos de 1 minuto.
        rapidas = collection.count_documents ({
            "horse_name": nombre,
            "finish_time_seconds": {
                "$lt": 60}
            })
        print("")
        print(f"El total de carreras corridas con tiempo menor a 1 minuto de {nombre} fueron {rapidas}")
    except Exception as e:
        print("Error en la consulta:{e}")