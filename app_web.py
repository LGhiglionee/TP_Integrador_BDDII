"""
Archivo principal de la aplicación web EQUIDATA.

Este módulo inicializa el dashboard desarrollado con Streamlit y organiza
la navegación entre los distintos motores NoSQL utilizados en el proyecto:
MongoDB, Redis, Neo4j y Cassandra.

Cada motor cuenta con su propia vista y su propia función de conexión.
Las conexiones se almacenan en caché con st.cache_resource para evitar
reconexiones innecesarias durante la ejecución de la aplicación.
"""
import streamlit as st

from motor_mongo.conectarMongo import ConectarMongo
from vistas.vista_mongo import mostrar_mongo
from motor_redis.conectarRedis import conectarRedis
from vistas.vista_redis import mostrar_redis
from motor_neo4j.conectarNeo4j import ConectarNeo4j, uri, user, password
from vistas.vista_neo4j import mostrar_neo4j
from vistas.vista_cassandra import mostrar_cassandra
from motor_cassandra.conectarCassandra import ConectarCassandra

# =========================================================
# CONFIGURACIÓN GENERAL DE LA APLICACIÓN
# =========================================================
st.set_page_config(
    page_title="Dashboard Multimotor - EQUIDATA", 
    page_icon="vistas/logo.png",
    layout="wide"
)

# =========================================================
# ESTILOS PERSONALIZADOS PARA LA INTERFAZ
# =========================================================
# Se aplican estilos CSS sobre los componentes de pestañas de Streamlit
# para mejorar la legibilidad y distribuir mejor el espacio disponible.
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

# =========================================================
# ENCABEZADO DEL DASHBOARD
# =========================================================
# Se muestra el logo institucional junto al título principal del proyecto.
col_logo, col_titulo = st.columns([1, 15], vertical_alignment="center")

with col_logo:
    st.image("vistas/logo.png", width=100)
with col_titulo:
    st.title("Trabajo Práctico Integrador - EQUIDATA")

# =========================================================
# CONEXIONES A LOS MOTORES DE BASES DE DATOS
# =========================================================
# st.cache_resource permite reutilizar la misma conexión durante la sesión
# de Streamlit. Esto evita reconexiones constantes cada vez que la app se
# actualiza por una interacción del usuario.

@st.cache_resource
def obtener_coleccion_mongo():
    return ConectarMongo("Cursus", "InfoHorses")

@st.cache_resource
def obtener_conexion_neo4j():
    return ConectarNeo4j(uri, user, password)

@st.cache_resource
def obtener_conexion_redis():
    return conectarRedis()

@st.cache_resource
def obtener_conexion_cassandra ():
    return ConectarCassandra()

# =========================================================
# SISTEMA DE PESTAÑAS DEL DASHBOARD
# =========================================================
# Cada pestaña representa un motor NoSQL diferente y delega la interfaz
# específica a su respectivo archivo dentro de la carpeta vistas.
tab_cassandra, tab_mongo, tab_neo4j, tab_redis = st.tabs([
    "Cassandra (Columnar)",
    "MongoDB (Documental)",
    "Neo4j (Grafos)", 
    "Redis (Clave-Valor)"
])

# =========================================================
# RENDERIZADO DE CADA VISTA
# =========================================================
# Cada función mostrar_* recibe la conexión correspondiente y construye
# el panel de operaciones propio de cada motor.
with tab_mongo:
    mostrar_mongo (obtener_coleccion_mongo())
    
with tab_redis:
    mostrar_redis(obtener_conexion_redis(),obtener_conexion_cassandra())

with tab_cassandra:
    mostrar_cassandra(obtener_conexion_cassandra())

with tab_neo4j:
    mostrar_neo4j(obtener_conexion_neo4j())