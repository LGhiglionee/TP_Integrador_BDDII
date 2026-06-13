def insertar_caballo(collection, nuevo_doc):
    resultado = collection.insert_one(nuevo_doc)
    return resultado.inserted_id

def buscar_caballo_por_id_y_carrera(collection, horse_id, race_id):
    return collection.find_one({"horse_id": horse_id, "race_id": race_id})

def actualizar_caballo(collection, horse_id, race_id, campos_a_actualizar):
    resultado = collection.update_one(
        {"horse_id": horse_id, "race_id": race_id}, 
        {"$set": campos_a_actualizar}
    )
    return resultado

def borrar_caballo_todas_carreras(collection, horse_id):
    resultado = collection.delete_one({"horse_id": horse_id})
    return resultado

def borrar_caballo_carrera_especifica(collection, horse_id, race_id):
    resultado = collection.delete_one({"horse_id": horse_id, "race_id": race_id})
    return resultado