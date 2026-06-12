import streamlit as st
import io
import builtins
from contextlib import redirect_stdout

from motor_neo4j.consultas.consultasBasicas import *
from motor_neo4j.consultas.consultasAvanzadas import *

def ejecutar_consulta_y_capturar_output(func, session, valor_input=None):
    f = io.StringIO()
    input_original = builtins.input

    if valor_input is not None:
        builtins.input = lambda *args, **kwargs: valor_input

    with redirect_stdout(f):
        try:
            func(session)
        except Exception as e:
            print(f"Error en la ejecución web: {e}")
        finally:
            builtins.input = input_original
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
            categoria = st.radio("Tipo de consulta", ["Simples", "Complejas",],key="btn_tipo_consulta_neo4j")
            parametro = None
            opcion = None
            if categoria == "Simples":
                opcion = st.selectbox(
                    "Seleccione la consulta simple:",
                    [
                        "1. Mostrar todos los entrenadores registrados",
                        "2. Mostrar todos los caballos ganadores",
                        "3. Contar la cantidad total de caballos en el grafo",
                        "4. Mostrar entrenadores cuyo nombre empiece con P",
                        "5. Mostrar los caballos que contengan 'DRAGON' en su nombre"
                    ]
                )
                ejecutar = st.button("Ejecutar Consulta Simple", use_container_width=True, type="primary",key="btn_ejecutar_consulta_s_neo4j")
                
            elif categoria == "Complejas":
                opcion = st.selectbox(
                    "Seleccione la consulta compleja:",
                    [
                        "1. Buscar posición de un caballo específico",
                        "2. Recomendar un entrenador",
                        "3. Buscar caballos similares (Patrón de Diamante)",
                        "4. Recomendar apuestas por éxito genético",
                        "5. Buscar ficha genealógica estructurada (Línea de Sangre)",
                        "6. Mostrar ranking de entrenadores por linaje"
                        ]
                )

                if opcion == "6. Mostrar ranking de entrenadores por linaje":
                    parametro = st.text_input("Ingresar Nombre del Padre:", value="").upper().strip()
                else:
                    parametro = st.text_input("Ingresar Nombre del Caballo:", value="").upper().strip()
                ejecutar = st.button("Ejecutar Consulta Compleja", use_container_width=True, type="primary",key="btn_ejecutar_consulta_c_neo4j")

    with col2:
        st.subheader("Consola de Salida")
        output_resultado = ""
        
        if ejecutar:
            with st.spinner('Consultando el grafo en Neo4j...'):
                with driver.session(database="neo4j") as session:
                    if categoria == "Simples" and opcion:
                        if opcion.startswith("1."): output_resultado = ejecutar_consulta_y_capturar_output(listar_todos_entrenadores, session)
                        elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(caballos_ganadores, session)
                        elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(cantidad_total_caballos, session)
                        elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(entrenadores_letra_p, session)
                        elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(caballos_con_dragon, session)

                    elif categoria == "Complejas" and opcion:
                        if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(buscar_caballo_nombre, session)
                        elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(recomendacion_entrenador_matchmaking, session)
                        elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(caballos_similares_diamante, session)
                        elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(recomendacion_apuestas_linaje, session)
                        elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(linea_sangre_caballo, session)
                        elif opcion.startswith("6."):output_resultado = ejecutar_consulta_y_capturar_output(ranking_entrenadores_por_linaje, session)

        if output_resultado:
            accion_limpia = opcion.split(". ", 1)[-1].replace(" ", "_").lower()
            nombre_final_archivo = f"resultado_{accion_limpia}__neo4j.txt"
            st.download_button(
                label="Descargar datos (TXT)",
                data=output_resultado,
                file_name=nombre_final_archivo,
                mime="text/plain",
                use_container_width=True
            )
            st.code(output_resultado, language="text")
        else:
            st.info("Selecciona una consulta del panel izquierdo y presiona el botón para visualizar los datos aquí.")