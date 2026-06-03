import streamlit as st

from motor_mongo.conectarMongo import ConectarMongo
from vistas.vista_mongo import mostrar_mongo
from motor_redis.conectarRedis import conectarRedis
from vistas.vista_redis import mostrar_redis

# Configuración de la página web
st.set_page_config(
    page_title="Dashboard Multimotor - EQUIDATA", 
    page_icon="vistas/logo.png",  # <-- Asegúrate de poner la ruta correcta a tu logo
    layout="wide"
)

st.markdown("""
    <style>

        /* Hace que el texto de cada pestaña sea más grande y legible */
        div[data-testid="stTabs"] button p {
            font-size: 20px !important;
            font-weight: 600 !important;
        }
        
        /* Fuerza a la barra contenedora a usar el 100% del ancho de la pantalla */
        div[data-testid="stTabs"] [role="tablist"] {
            display: flex !important;
            justify-content: space-between !important;
            width: 100% !important;
            gap: 12px !important;
        }
        
        /* Distribuye las pestañas de forma equitativa y les da aire arriba/abajo */
        div[data-testid="stTabs"] button {
            flex-grow: 1 !important;
            text-align: center !important;
            padding: 14px 0px !important;
        }
    </style>
""", unsafe_allow_html=True)

col_logo, col_titulo = st.columns([1, 15], vertical_alignment="center")

with col_logo:
    st.image("vistas/logo.png", width=100)

with col_titulo:
    st.title("Trabajo Práctico Integrador - EQUIDATA")

# Inicializar la conexión a Mongo una sola vez (evita reconexiones molestas en entorno web)
@st.cache_resource
def obtener_coleccion_mongo():
    return ConectarMongo("Cursus", "InfoHorses")

def obtener_conexion_redis():
    return conectarRedis()

colleccion_mongo = obtener_coleccion_mongo()
redis_db = obtener_conexion_redis()

# Sistema de pestañas
tab_mongo, tab_redis, tab_cassandra, tab_neo4j = st.tabs([
    "MongoDB (Documental)", 
    "Redis (Clave-Valor)", 
    "Cassandra (Columnar)", 
    "Neo4j (Grafos)"
])

with tab_mongo:
    mostrar_mongo (colleccion_mongo)
    
with tab_redis:
    mostrar_redis(redis_db)

with tab_cassandra:
    st.header("Consultas en Apache Cassandra")
    st.info("Estructura Columnar (CQL) lista para integración.")

with tab_neo4j:
    st.header("Consultas en Neo4j")
    st.info("Consultas de Grafos (Cypher) listas para integración de relaciones (Entrenador -> Corre -> Carrera).")