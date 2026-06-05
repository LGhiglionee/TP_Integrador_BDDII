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
                ["Básicas", "Avanzadas con Parámetro"]
            )
        
            opcion = None
            parametro = ""
            
            if categoria == "Básicas":
                opcion = st.selectbox(
                    "Selecciona la consulta básica:",
                    [
                        #PONER LAS CONSULTAS QUE VAMOS A HACER
                    ]
                )
                ejecutar = st.button("Ejecutar Consulta", use_container_width=True, type="primary")
                
            elif categoria == "Avanzadas con Parámetro":
                opcion = st.selectbox(
                    "Selecciona la consulta avanzada:",
                    [
                        #PONER LAS CONSULTAS QUE VAMOS A HACER
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
                if categoria == "Básicas" and opcion:
                    '''if opcion.startswith("1."): output_resultado'''
                    '''elif opcion.startswith("2."): output_resultado'''

                elif categoria == "Avanzadas con Parámetro" and opcion:
                    if not parametro:
                        st.warning("Por favor, ingrese un parámetro válido.")
                    else:
                        input_original = builtins.input
                        builtins.input = lambda *args: parametro                        
                        '''if opcion.startswith("1."):
                        elif opcion.startswith("2."):
                        elif opcion.startswith("3."):
                        builtins.input = input_original'''

        if output_resultado:
            st.code(output_resultado, language="text")
        else:
            st.info("Selecciona una consulta del panel izquierdo y presiona el botón para visualizar los datos aquí.")