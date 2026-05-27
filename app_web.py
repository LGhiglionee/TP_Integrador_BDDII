import streamlit as st
import io
import builtins
from contextlib import redirect_stdout

# Importar las funciones de sus scripts actuales sin modificarlos
from mongo.conectarMongo import ConectarMongo
from mongo.consultasBasicas import (
    caballosEntrenadosP_F_YIU, caballosGanadores, caballosMenoresDeMil, 
    cantCarreras, caballosVeloces, buscarHistorialCaballo
)
from mongo.consultasAvanzadas import (
    promedio_tiempo_todos, promedio_tiempo_entrenador, 
    caballos_diez_tiempo, caballosConA, top_10_tiempos
)

# Configuración de la página web
st.set_page_config(page_title="Dashboard Multimotor", layout="wide")
st.title("PANEL DE CONTROL EQUIDATA")

# Inicializar la conexión a Mongo una sola vez (evita reconexiones molestas en entorno web)
@st.cache_resource
def obtener_coleccion():
    return ConectarMongo("Cursus", "InfoHorses")

collection = obtener_coleccion()

# Función auxiliar para capturar los 'print()' de sus scripts y devolverlos como texto
def ejecutar_consulta_y_capturar_output(func, *args, **kwargs):
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Error en la ejecución web: {e}")
    return f.getvalue()

# Crear pestañas para los 4 motores de bases de datos
tab_mongo, tab_redis, tab_cassandra, tab_neo4j = st.tabs([
    "MongoDB (Documental)", 
    "Redis (Clave-Valor)", 
    "Cassandra (Columnar)", 
    "Neo4j (Grafos)"
])

# ==================== PESTAÑA MONGODB ====================
with tab_mongo:
    st.header("Consultas sobre el Dataset de Carreras de Caballos")
    
    if collection is None:
        st.error("No se pudo conectar a la colección de MongoDB.")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Seleccione una Consulta")
            
            # Agrupamos sus menús de consola en secciones web interactivas
            categoria = st.radio("Tipo de consulta", ["Simples", "Complejas", "Historial por Nombre"])
            
            opcion = None
            if categoria == "Simples":
                opcion = st.selectbox(
                    "Selecciona la consulta simple:",
                    [
                        "1. Obtener todos los caballos entrenados por P F YIU",
                        "2. Todos los caballos que ganaron alguna carrera",
                        "3. Caballos que pesan menos de 1000 libras",
                        "4. Cantidad de carreras que se corrieron",
                        "5. Caballos con tiempos menores a 1.23.00"
                    ]
                )
            elif categoria == "Complejas":
                opcion = st.selectbox(
                    "Selecciona la consulta compleja:",
                    [
                        "1. Tiempo promedio de todos los caballos",
                        "2. Tiempo promedio de carrera de los caballos entrenados por P F YIU",
                        "3. Caballos con número 10 y tiempo menor a 1.22.70",
                        "4. Listar todos los caballos cuyo nombre comience con A",
                        "5. TOP 10 de tiempos más rápidos"
                    ]
                )
            elif categoria == "Historial por Nombre":
                st.info("Esta consulta requiere un parámetro de búsqueda.")
                nombre_caballo = st.text_input("Ingresar nombre del caballo:", value="").upper().strip()
                ejecutar_busqueda = st.button("Buscar Historial")

        with col2:
            st.subheader("Resultado de la Base de Datos")
            
            output_resultado = ""
            
            # Evaluación de Consultas Simples
            if categoria == "Simples" and opcion:
                if opcion.startswith("1."):
                    output_resultado = ejecutar_consulta_y_capturar_output(caballosEntrenadosP_F_YIU, collection)
                elif opcion.startswith("2."):
                    output_resultado = ejecutar_consulta_y_capturar_output(caballosGanadores, collection)
                elif opcion.startswith("3."):
                    output_resultado = ejecutar_consulta_y_capturar_output(caballosMenoresDeMil, collection)
                elif opcion.startswith("4."):
                    output_resultado = ejecutar_consulta_y_capturar_output(cantCarreras, collection)
                elif opcion.startswith("5."):
                    output_resultado = ejecutar_consulta_y_capturar_output(caballosVeloces, collection)

            # Evaluación de Consultas Complejas
            elif categoria == "Complejas" and opcion:
                if opcion.startswith("1."):
                    output_resultado = ejecutar_consulta_y_capturar_output(promedio_tiempo_todos, collection)
                elif opcion.startswith("2."):
                    output_resultado = ejecutar_consulta_y_capturar_output(promedio_tiempo_entrenador, collection)
                elif opcion.startswith("3."):
                    output_resultado = ejecutar_consulta_y_capturar_output(caballos_diez_tiempo, collection)
                elif opcion.startswith("4."):
                    output_resultado = ejecutar_consulta_y_capturar_output(caballosConA, collection)
                elif opcion.startswith("5."):
                    output_resultado = ejecutar_consulta_y_capturar_output(top_10_tiempos, collection)
            
            # Evaluación del Historial (Inyección dinámica del input para no romper su script)
            elif categoria == "Historial por Nombre" and ejecutar_busqueda:
                if not nombre_caballo:
                    st.warning("Por favor, ingrese un nombre válido.")
                else:
                    # Guardamos la función input original de Python
                    input_original = builtins.input
                    # Truco: Sobrescribimos temporalmente 'input' para que devuelva lo que el usuario escribió en la web
                    builtins.input = lambda *args: nombre_caballo
                    
                    output_resultado = ejecutar_consulta_y_capturar_output(buscarHistorialCaballo, collection)
                    
                    # Restauramos el input original
                    builtins.input = input_original

            # Renderizado estético del resultado
            if output_resultado:
                st.code(output_resultado, language="text")
            else:
                st.write("Selecciona una opción o ejecuta una acción para ver los resultados en tiempo real.")

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