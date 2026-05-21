from menu import mostrarMenu
from conectarMongo import *;
from consultasBasicas import *;


collection = ConectarMongo("Cursus", "InfoHorses")

# Lanzar el menú
if collection is not None:
    mostrarMenu(collection)
else:
    print("Error: No se pudo conectar a la colección.")