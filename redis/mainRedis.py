from menuRedis import mostrarMenuRedis
from conectarRedis import *

redis_db = conectarRedis()

# Lanzar el menú
if redis_db is not None:
    mostrarMenuRedis(redis_db)
else:
    print("Error: No se pudo conectar a Redis.")