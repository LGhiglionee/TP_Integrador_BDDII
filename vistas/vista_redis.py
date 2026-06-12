import streamlit as st
import io
from contextlib import redirect_stdout

from motor_redis.consultas.consultasBasicas_redis import *
from motor_redis.consultas.consultasAvanzadas_redis import *

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

    mensaje_crud = None
    tipo_mensaje = None
    output_resultado = ""
    opcion = None
    categoria = None
    id_carrera = ""
    cant_apuestas = None
    ejecutar = False

    col1, col2 = st.columns([1, 1.8])
    
    with col1:
        with st.container(border=True):
            st.markdown("### Panel de Control")

            modo_operacion = st.radio("Modo de Operación",["Modificar Datos","Consultas/Simulación"],horizontal=True,key="modo_operacion_redis")
            if modo_operacion == "Consultas/Simulación":
                categoria = st.radio("Tipo de consulta",["Simples", "Complejas"],key="btn_tipo_consulta_redis")
                if categoria == "Simples":
                    opcion = st.selectbox(
                        "Seleccione la consulta simple:",
                        [
                            "1. Crear una carrera",
                            "2. Generar apuestas ficticias para una carrera",
                            "3. Ver estado de una carrera",
                            "4. Ver participantes de una carrera",
                            "5. Ver apuestas activas de una carrera"
                        ],
                        key="select_simple_redis"
                    )
                    if opcion and opcion.startswith("2."):
                        cant_apuestas = st.number_input("Cantidad de apuestas a generar:",min_value=1,max_value=1000,value=10,key="cant_apuestas_redis")
                    id_carrera = st.text_input("Ingrese ID de la Carrera:", value="", placeholder="Ej: 2016-567",key="id_simple_redis").strip()
                    ejecutar = st.button("Ejecutar Consulta Simple", use_container_width=True, type="primary", key="btn_ejecutar_simple_redis")

                elif categoria == "Complejas":
                    opcion = st.selectbox(
                        "Seleccione la consulta compleja:",
                        [
                            "1. Simular carrera en tiempo real",
                            "2. Ver ranking actual de una carrera",
                            "3. Obtener caballo ganador de una carrera",
                            "4. Finalizar una carrera",
                            "5. Actualizar apuestas de una carrera",
                            "6. Expirar datos temporales de una carrera"
                        ],
                        key="select_compleja_redis"
                    )
                    id_carrera = st.text_input("Ingrese ID de la Carrera:", value="", placeholder="Ej: 2016-567",key="id_compleja_redis").strip()
                    ejecutar = st.button("Ejecutar Consulta Compleja", use_container_width=True, type="primary", key="btn_ejecutar_compleja_redis")
            elif modo_operacion == "Modificar Datos":
                categoria_crud = st.radio("Operación CRUD",["Inserción", "Actualización", "Borrado"],key="crud_redis")

    with col2:
        st.subheader("Consola de Salida")

        if ejecutar:
            if not id_carrera:
                st.warning("El ID de la carrera es obligatorio para todas las consultas.")
            else:
                with st.spinner('Ejecutando comando en Redis...'):
                    # Evaluación de Consultas Básicas
                    if categoria == "Simples" and opcion:
                        if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(crearCarrera, redis_db, id_carrera)
                        elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(generarApuestasFicticias, redis_db, id_carrera, cant_apuestas)
                        elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(verEstadoCarrera, redis_db, id_carrera)
                        elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(verParticipantes, redis_db, id_carrera)
                        elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(verApuestasActivas, redis_db, id_carrera)

                    # Evaluación de Consultas Avanzadas
                    elif categoria == "Complejas" and opcion:
                        if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(simularCarrera, redis_db, id_carrera)
                        elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(verRanking, redis_db, id_carrera)
                        elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(obtenerGanador, redis_db, id_carrera)
                        elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(finalizarCarrera, redis_db, id_carrera)
                        elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(actualizarApuestas, redis_db, id_carrera)
                        elif opcion.startswith("6."):output_resultado = ejecutar_consulta_y_capturar_output(expirarDatosCarrera, redis_db, id_carrera)

        if output_resultado:
            consulta_limpia = opcion.split(". ", 1)[-1].replace(" ", "_").lower()
            id_limpio = id_carrera.replace(" ", "_").lower()

            st.download_button(
                label="Descargar datos (TXT)",
                data=output_resultado,
                file_name=f"resultado_{consulta_limpia}_{id_limpio}_redis.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.code(output_resultado, language="text")
        else:
            st.info("Seleccione una consulta del panel izquierdo y presiona el botón para visualizar los datos aquí.")