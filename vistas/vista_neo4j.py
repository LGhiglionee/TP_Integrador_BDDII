import streamlit as st
import io
import builtins
from contextlib import redirect_stdout

from motor_neo4j.consultas.consultasBasicas import *
from motor_neo4j.consultas.consultasAvanzadas import *

def ejecutar_consulta_y_capturar_output(func, *args, **kwargs):
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Error en la ejecución web: {e}")
    return f.getvalue()

def mostrar_neo4j(driver):
    st.header("Consultas de Grafos - Neo4j")
    
    if driver is None:
        st.error("No se pudo conectar a la base de datos Neo4j.")
        return

    col1, col2 = st.columns([1, 1.8])
    
    with col1:
        with st.container(border=True):
            st.markdown("Panel de Control")        
            categoria = st.radio(
                "Tipo de consulta", 
                ["Básicas", "Avanzadas"]
            )
        
            opcion = None
            parametro = ""
            
            if categoria == "Básicas":
                opcion = st.selectbox(
                    "Selecciona la consulta básica:",
                    [
                        "1. Listar todos los entrenadores únicos registrados",
                        "2. Mostrar todos los caballos ganadores (Posición 1)",
                        "3. Contar la cantidad total de caballos en el grafo",
                        "4. Mostrar entrenadores cuyo nombre empieza con P",
                        "5. Mostrar caballos que contienen 'DRAGON' en su nombre"
                    ]
                )
                ejecutar = st.button("Ejecutar Consulta", use_container_width=True, type="primary")
                
            elif categoria == "Avanzadas":
                opcion = st.selectbox(
                    "Selecciona la consulta avanzada:",
                    [
                        "1. Buscar posición de un caballo específico",
                        "2. Recomendación de Entrenador (Matchmaking por hermanos)",
                        "3. Buscar Caballos Similares (Patrón de Diamante)",
                        "4. Recomendación de Apuestas por Éxito Genético",
                        "5. Ficha Genealógica Estructurada (Línea de Sangre)"                    
                        ]
                )
                st.info("Esta consulta requiere un parámetro de búsqueda.")
                parametro = st.text_input("Ingresar parámetro (Nombre del Caballo):", value="").upper().strip()
                ejecutar = st.button("Ejecutar Búsqueda", use_container_width=True, type="primary")

    with col2:
        st.subheader("Consola de Salida")
        output_resultado = ""
        
        if ejecutar:
            with st.spinner('Consultando el grafo en Neo4j...'):
                with driver.session(database="neo4j") as session:
                    
                    if categoria == "Básicas" and opcion:
                        if opcion.startswith("1."): 
                            output_resultado = ejecutar_consulta_y_capturar_output(listar_todos_entrenadores, session)
                        elif opcion.startswith("2."): 
                            output_resultado = ejecutar_consulta_y_capturar_output(caballos_ganadores, session)
                        elif opcion.startswith("3."): 
                            output_resultado = ejecutar_consulta_y_capturar_output(cantidad_total_caballos, session)
                        elif opcion.startswith("4."): 
                            output_resultado = ejecutar_consulta_y_capturar_output(entrenadores_letra_p, session)
                        elif opcion.startswith("5."): 
                            output_resultado = ejecutar_consulta_y_capturar_output(caballos_con_dragon, session)

                    elif categoria == "Avanzadas" and opcion:
                        if not parametro:
                            st.warning("Por favor, ingrese un parámetro válido.")
                        else:
                            input_original = builtins.input
                            builtins.input = lambda *args: parametro                        
                            
                            if opcion.startswith("1."):
                                output_resultado = ejecutar_consulta_y_capturar_output(buscar_caballo_nombre, session)
                            elif opcion.startswith("2."):
                                output_resultado = ejecutar_consulta_y_capturar_output(recomendacion_entrenador_matchmaking, session)
                            elif opcion.startswith("3."):
                                output_resultado = ejecutar_consulta_y_capturar_output(caballos_similares_diamante, session)
                            elif opcion.startswith("4."):
                                output_resultado = ejecutar_consulta_y_capturar_output(recomendacion_apuestas_linaje, session)
                            elif opcion.startswith("5."):
                                output_resultado = ejecutar_consulta_y_capturar_output(linea_sangre_caballo, session)
                                
                            builtins.input = input_original

        if output_resultado:
            st.code(output_resultado, language="text")
        else:
            st.info("Selecciona una consulta del panel izquierdo y presiona el botón para visualizar los datos aquí.")