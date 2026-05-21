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
            print(f"\nTotal de caballos únicos: {len(nombres_no_repetidos)}")
            
    except Exception as e:
        print(f"Error en la consulta: {e}")
        

#Todos los caballos que ganaron alguna carrera

#Caballos que pesan menos de 1000

#Cantidad de carreras que se corrieron

#Caballos con tiempos menores a 1.23.000

#Listar todos los codigos de carreras