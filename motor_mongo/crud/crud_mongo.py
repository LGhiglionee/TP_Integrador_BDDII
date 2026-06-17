"""
Módulo de operaciones CRUD para MongoDB.
Gestiona el ciclo de vida de los documentos mediante el driver PyMongo,
asegurando la integridad de los datos en la colección principal.
"""

def insertar_caballo(collection, nuevo_doc):
    """
    Inserta un nuevo documento en la colección.
    Utiliza insert_one para persistir un único registro BSON.
    """
    resultado = collection.insert_one(nuevo_doc)
    return resultado.inserted_id

def buscar_caballo_por_id_y_carrera(collection, horse_id, race_id):
    """
    Realiza una búsqueda precisa (query compuesta) para verificar la existencia
    de un registro antes de realizar operaciones de inserción o actualización.
    """
    return collection.find_one({"horse_id": horse_id, "race_id": race_id})

def actualizar_caballo(collection, horse_id, race_id, campos_a_actualizar):
    """
    Actualiza campos específicos mediante el operador atómico $set.
    Esto permite modificar solo la data necesaria sin sobreescribir todo el documento.
    """
    resultado = collection.update_one(
        {"horse_id": horse_id, "race_id": race_id},  # Filtro de coincidencia
        {"$set": campos_a_actualizar} # Operación de modificación
    )
    return resultado

def borrar_caballo_todas_carreras(collection, horse_id):
    """
    Elimina todos los documentos que coincidan con el ID del caballo.
    Útil para gestionar el ciclo de vida histórico cuando un caballo es dado de baja.
    """
    resultado = collection.delete_many({"horse_id": horse_id})
    return resultado

def borrar_caballo_carrera_especifica(collection, horse_id, race_id):
    """
    Elimina un documento puntual basado en una relación única (Caballo + Carrera).
    """
    resultado = collection.delete_one({"horse_id": horse_id, "race_id": race_id})
    return resultado