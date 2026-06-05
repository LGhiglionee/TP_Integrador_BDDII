import streamlit as st
import io
import builtins
from contextlib import redirect_stdout

from motor_mongo.consultas.consultasBasicas import *
from motor_mongo.consultas.consultasAvanzadas import *

def ejecutar_consulta_y_capturar_output(func, *args, **kwargs):
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Error en la ejecución web: {e}")
    return f.getvalue()

def mostrar_mongo (collection):
    st.header("Consultas sobre base de datos NoSQL - MongoDB")
    
    if collection is None:
        st.error("No se pudo conectar a la colección de MongoDB.")
        return

    col1, col2 = st.columns([1, 1.8])
    
    with col1:
        with st.container(border=True):
            st.markdown("Panel de Control")        
            # Agrupamos sus menús de consola en secciones web interactivas
            categoria = st.radio(
                "Tipo de consulta", 
                ["Simples", "Complejas", "Historial por Nombre"]
                )
        
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
                ejecutar_consulta = st.button("Ejecutar Consulta Simple", use_container_width=True, type="primary")
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
                ejecutar_consulta = st.button("Ejecutar Consulta Compleja", use_container_width=True, type="primary")
                
            elif categoria == "Historial por Nombre":
                st.info("Esta consulta requiere un parámetro de búsqueda.")
                nombre_caballo = st.text_input("Ingresar nombre del caballo:", value="").upper().strip()
                ejecutar_consulta = st.button("Buscar Historial", use_container_width=True, type="primary")
    with col2:
        st.subheader("Consola de Salida")
        
        output_resultado = ""
        
        if ejecutar_consulta:
            with st.spinner('Buscando en MongoDB...'):
                # Evaluación de Consultas Simples
                if categoria == "Simples" and opcion:
                    if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(caballosEntrenadosP_F_YIU, collection)
                    elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(caballosGanadores, collection)
                    elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(caballosMenoresDeMil, collection)
                    elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(cantCarreras, collection)
                    elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(caballosVeloces, collection)

                # Evaluación de Consultas Complejas
                elif categoria == "Complejas" and opcion:
                    if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(promedio_tiempo_todos, collection)
                    elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(promedio_tiempo_entrenador, collection)
                    elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(caballos_diez_tiempo, collection)
                    elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(caballosConA, collection)
                    elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(top_10_tiempos, collection)
        
                # Evaluación del Historial (Inyección dinámica del input para no romper su script)
                elif "Historial" in categoria:
                    if not nombre_caballo:
                        st.warning("Por favor, ingrese un nombre válido.")
                    else:
                        input_original = builtins.input
                        builtins.input = lambda *args: nombre_caballo                        
                        output_resultado = ejecutar_consulta_y_capturar_output(buscarHistorialCaballo, collection)
                        builtins.input = input_original

        # Renderizado estético del resultado
        if output_resultado:
            if "Historial" in categoria:
                consulta_limpia = f"historial_{nombre_caballo.replace(' ', '_').lower()}"
            else:
                consulta_limpia = opcion.split(". ", 1)[-1].replace(" ", "_").lower()
            nombre_final_archivo = f"resultado_{consulta_limpia}_mongo.txt"
            
            # Botón de descarga con el nombre dinámico
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