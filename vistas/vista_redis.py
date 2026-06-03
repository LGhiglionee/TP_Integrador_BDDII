import streamlit as st
import io
from contextlib import redirect_stdout

# IMPORTANTE: Cambiá el nombre de tu carpeta de "redis" a "motor_redis" (o el que uses)
from motor_redis.consultas.consultasBasicas import *
from motor_redis.consultas.consultasAvanzadas import *

def ejecutar_consulta_y_capturar_output(func, *args, **kwargs):
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Error en la ejecución web: {e}")
    return f.getvalue()

def mostrar_redis(redis_db):
    st.header("Simulación en tiempo real - Redis")
    
    if redis_db is None:
        st.error("No se pudo conectar a la base de datos Redis.")
        return

    col1, col2 = st.columns([1, 1.8])
    
    with col1:
        with st.container(border=True):
            st.markdown("Panel de control")
        
            # Agrupamos los menús de Redis
            categoria = st.radio("Tipo de Acción", ["Básicas", "Avanzadas"])
        
            opcion = None
            if categoria == "Básicas":
                opcion = st.selectbox(
                    "Selecciona la acción básica:",
                    [
                        "1. Crear carrera", 
                        "2. Generar apuestas ficticias", 
                        "3. Ver estado de una carrera", 
                        "4. Ver participantes", 
                        "5. Ver apuestas activas"
                    ]
                )
            elif categoria == "Avanzadas":
                opcion = st.selectbox(
                    "Selecciona la acción avanzada:",
                    [
                        "1. Simular carrera en tiempo real", 
                        "2. Ver ranking actual", 
                        "3. Obtener caballo ganador", 
                        "4. Finalizar carrera", 
                        "5. Actualizar apuestas ganadas/perdidas", 
                        "6. Expirar datos temporales de una carrera"
                    ]
                )
        
            id_carrera = st.text_input("ID de la Carrera:", value="", placeholder="Ej: CARRERA_01")        
            
            cant_apuestas = None
            if "Básicas" in categoria and opcion and opcion.startswith("2."):
                cant_apuestas = st.number_input("Cantidad de apuestas a generar:", min_value=1, max_value=1000, value=10)
            
            ejecutar = st.button("Ejecutar en Redis", use_container_width=True, type="primary")

    with col2:
        st.subheader("Consola de Salida")
        output_resultado = ""
        
        if ejecutar:
            if not id_carrera:
                st.warning("El ID de la carrera es obligatorio para operar en Redis.")
            else:
                with st.spinner('Ejecutando comando en Redis...'):
                    # Evaluación de Consultas Básicas
                    if categoria == "Básicas" and opcion:
                        if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(crearCarrera, redis_db, id_carrera)
                        elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(generarApuestasFicticias, redis_db, id_carrera, cant_apuestas)
                        elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(verEstadoCarrera, redis_db, id_carrera)
                        elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(verParticipantes, redis_db, id_carrera)
                        elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(verApuestasActivas, redis_db, id_carrera)
                    
                    # Evaluación de Consultas Avanzadas
                    elif categoria == "Avanzadas" and opcion:
                        if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(simularCarrera, redis_db, id_carrera)
                        elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(verRanking, redis_db, id_carrera)
                        elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(obtenerGanador, redis_db, id_carrera)
                        elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(finalizarCarrera, redis_db, id_carrera)
                        elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(actualizarApuestas, redis_db, id_carrera)
                        elif opcion.startswith("6."):output_resultado = ejecutar_consulta_y_capturar_output(expirarDatosCarrera, redis_db, id_carrera)

        if output_resultado:
            accion_limpia = opcion.split(". ", 1)[-1].replace(" ", "_").lower()
            id_limpio = id_carrera.replace(" ", "_").lower()
            nombre_final_archivo = f"resultado_{accion_limpia}_{id_limpio}_redis.txt"            
            st.download_button(
                label="Descargar datos (TXT)",
                data=output_resultado,
                file_name=nombre_final_archivo,
                mime="text/plain",
                use_container_width=True
            )
            st.code(output_resultado, language="text")
        else:
            st.write("Configure los parámetros a la izquierda y presione 'Ejecutar en Redis' para ver la respuesta del servidor transaccional.")