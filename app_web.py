import streamlit as st

from mongo.conectarMongo import ConectarMongo
from vistas.vista_mongo import mostrar_mongo
# Configuración de la página web
st.set_page_config(page_title="Dashboard Multimotor", layout="wide")
st.title("Trabajo Práctico Integrador - EQUIDATA")

# Inicializar la conexión a Mongo una sola vez (evita reconexiones molestas en entorno web)
@st.cache_resource
def obtener_coleccion_mongo():
    return ConectarMongo("Cursus", "InfoHorses")

colleccion_mongo = obtener_coleccion_mongo()

# Sistema de pestañas
tab_mongo, tab_redis, tab_cassandra, tab_neo4j = st.tabs([
    "MongoDB (Documental)", 
    "Redis (Clave-Valor)", 
    "Cassandra (Columnar)", 
    "Neo4j (Grafos)"
])

with tab_mongo:
    mostrar_mongo (colleccion_mongo)
    
# ==================== PLACEHOLDERS PARA OTROS MOTORES ====================
with tab_redis:
    st.header("Consultas en Redis")
    st.info("Estructura Clave-Valor lista para conectar. Añadan sus funciones en un script independiente e impórtenlas aquí de la misma forma.")
    st.subheader("Ejemplo de Estructura de Datos:")
    st.json({"caballo:id:100": "nombre_caballo", "caballo:id:100:tiempo_record": "82.10"})

with tab_cassandra:
    st.header("Consultas en Apache Cassandra")
    st.info("Estructura Columnar (CQL) lista para integración.")

with tab_neo4j:
    st.header("Consultas en Neo4j")
    st.info("Consultas de Grafos (Cypher) listas para integración de relaciones (Entrenador -> Corre -> Carrera).")