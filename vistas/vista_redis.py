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
    st.header("Consultas y Simulación en base de datos Clave-Valor - Redis")
    
    if redis_db is None:
        st.error("No se pudo conectar a la base de datos Redis.")
        return

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Acciones de Carrera")
        
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
        
        id_carrera = st.text_input("Ingrese ID de la carrera:", value="").strip()
        
        cant_apuestas = None
        if categoria == "Básicas" and opcion and opcion.startswith("2."):
            cant_apuestas = st.number_input("Cantidad de apuestas a generar:", min_value=1, max_value=1000, value=10)
        
        ejecutar = st.button("Ejecutar Acción")

    with col2:
        st.subheader("Resultado de la Base de Datos")
        output_resultado = ""
        
        if ejecutar:
            if not id_carrera:
                st.warning("El ID de la carrera es obligatorio para todas las consultas.")
            else:
                with st.spinner('Ejecutando en Redis...'):
                    # Evaluación de Consultas Básicas
                    if categoria == "Básicas" and opcion:
                        if opcion.startswith("1."):
                            output_resultado = ejecutar_consulta_y_capturar_output(crearCarrera, redis_db, id_carrera)
                        elif opcion.startswith("2."):
                            output_resultado = ejecutar_consulta_y_capturar_output(generarApuestasFicticias, redis_db, id_carrera, cant_apuestas)
                        elif opcion.startswith("3."):
                            output_resultado = ejecutar_consulta_y_capturar_output(verEstadoCarrera, redis_db, id_carrera)
                        elif opcion.startswith("4."):
                            output_resultado = ejecutar_consulta_y_capturar_output(verParticipantes, redis_db, id_carrera)
                        elif opcion.startswith("5."):
                            output_resultado = ejecutar_consulta_y_capturar_output(verApuestasActivas, redis_db, id_carrera)
                    
                    # Evaluación de Consultas Avanzadas
                    elif categoria == "Avanzadas" and opcion:
                        if opcion.startswith("1."):
                            output_resultado = ejecutar_consulta_y_capturar_output(simularCarrera, redis_db, id_carrera)
                        elif opcion.startswith("2."):
                            output_resultado = ejecutar_consulta_y_capturar_output(verRanking, redis_db, id_carrera)
                        elif opcion.startswith("3."):
                            output_resultado = ejecutar_consulta_y_capturar_output(obtenerGanador, redis_db, id_carrera)
                        elif opcion.startswith("4."):
                            output_resultado = ejecutar_consulta_y_capturar_output(finalizarCarrera, redis_db, id_carrera)
                        elif opcion.startswith("5."):
                            output_resultado = ejecutar_consulta_y_capturar_output(actualizarApuestas, redis_db, id_carrera)
                        elif opcion.startswith("6."):
                            output_resultado = ejecutar_consulta_y_capturar_output(expirarDatosCarrera, redis_db, id_carrera)

        if output_resultado:
            st.code(output_resultado, language="text")
        else:
            st.write("Completa los datos y haz clic en 'Ejecutar Acción' para ver los resultados.")