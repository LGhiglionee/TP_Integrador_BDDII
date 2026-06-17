"""
Módulo de consultas básicas para MongoDB.
Gestiona el filtrado y resumen de datos mediante el método .distinct()
y el conteo condicional con .count_documents().
"""
def caballosEntrenadosP_F_YIU(collection):
    """
    Filtra caballos por entrenador usando una expresión regular (Regex)
    y obtiene una lista única de sus nombres.
    """
    try:
        # Regex flexible: P seguido de cualquier cosa, F, cualquier cosa, YIU
        query = {"trainer": {"$regex": "P.*F.*YIU", "$options": "i"}}

        nombres_no_repetidos = collection.distinct("horse_name", query)
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            nombres_no_repetidos = sorted(nombres_no_repetidos)
            print(f"\nTotal de caballos entrenados por P F YIU es {len(nombres_no_repetidos)}")
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
            
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
def caballosGanadores (collection):
    """
    Identifica caballos ganadores mediante el filtro de posición final igual a 1.
    """
    try:
        query = {"finishing_position":1}

        nombres_no_repetidos = collection.distinct ("horse_name", query)
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            nombres_no_repetidos = sorted(nombres_no_repetidos)
            print(f"\nTotal de caballos ganadores es {len(nombres_no_repetidos)}")
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
def caballosMenoresDeMil (collection):
    """
    Aplica un filtro de comparación numérica ($lt - less than) sobre el peso.
    """
    try:
        query = {"declared_horse_weight" : {"$lt" : 1000}}

        nombres_no_repetidos = collection.distinct ("horse_name", query)
        if not nombres_no_repetidos:
            print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            nombres_no_repetidos = sorted(nombres_no_repetidos)
            print(f"\nTotal de caballos que pesan menos de 1000 libras es {len(nombres_no_repetidos)}")
            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")
        
def cantCarreras (collection):
    """
    Cuenta el número de eventos distintos (race_id) para determinar cuántas carreras hubo.
    """
    try:
        races_unicas = collection.distinct("race_id")
        total = len(races_unicas)

        print(f"\nTotal de carreras corridas fue {total}")
                
    except Exception as e:
        print(f"Error en la consulta: {e}")

def caballosVeloces (collection):
    """
    Filtra caballos según un umbral de tiempo (83 segundos), utilizando comparación numérica.
    """
    try:
        query = {"finish_time_seconds": {"$lt" : 83.00}}

        nombres_no_repetidos = collection.distinct ("horse_name", query)
        if not nombres_no_repetidos:
                print("No se encontraron resultados. Verificá los nombres de las columnas.")
        else:
            nombres_no_repetidos = sorted(nombres_no_repetidos)
            print(f"\nTotal de caballos que llegaron con tiempo menor a 1 minuto 23 segundos es {len(nombres_no_repetidos)}")

            for nombre in nombres_no_repetidos:
                print(f"- {nombre}")
                                    
    except Exception as e:
        print(f"Error en la consulta: {e}")
        print(f"Error en la consulta: {e}")

def buscarHistorialCaballo (collection):
    """
    Realiza múltiples consultas sobre el mismo nombre para calcular estadísticas
    de éxito (efectividad) y métricas de desempeño histórico.
    """
    try:
        nombre = input ("\n Ingresar nombre del caballo el cual se quiere conocer el historial:").upper().strip()
        total_carreras = collection.count_documents({"horse_name": nombre})
        if total_carreras == 0:
                print(f"\nNo se encontraron registros para el caballo: {nombre}")
                return
        print(f"\nTotal de carreras jugadas por {nombre} fue {total_carreras}")

        # Filtro compuesto para contar victorias
        ganadas = collection.count_documents({
                "horse_name": nombre,
                "finishing_position": 1
            })
        print("")
        print(f"Total de carreras ganadas por {nombre} fue {ganadas}")

        efectividad = (ganadas / total_carreras) * 100
        print("")
        print(f"La efectividad de victoria de {nombre} fue {efectividad:.2f}%")

        # Filtro de tiempo para métricas de alto rendimiento
        rapidas = collection.count_documents ({
            "horse_name": nombre,
            "finish_time_seconds": {
                "$lt": 60}
            })
        print("")
        print(f"Total de carreras corridas con tiempo menor a 1 minuto de {nombre} fue {rapidas}")
    except Exception as e:
        print("Error en la consulta:{e}")