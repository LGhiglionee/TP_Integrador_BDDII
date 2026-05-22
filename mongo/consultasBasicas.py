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
        query = {"finishing_position":"1"}
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
        query = {
            "$expr": {
                "$lt": [
                    {"$convert": {
                            "input": "$declared_horse_weight",
                            "to": "int",
                            "onError": 9999,  # Si hay un "-", le pone 9999 para que no sea < 1000
                            "onNull": 9999    # Si está vacío, también le pone 9999
                        }
                    },1000
                ]}
            }
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
    
#Listar todos los codigos de carreras
