"""
Vista de Redis para el dashboard EQUIDATA.

Este módulo construye la interfaz web correspondiente al motor Redis.
Permite ejecutar consultas simples y complejas sobre datos temporales
de carreras, apuestas y rankings en tiempo real.

Redis se utiliza como motor clave-valor para simular escenarios dinámicos,
por ejemplo: creación de carreras, generación de apuestas, simulación en
tiempo real y expiración de datos temporales.
"""
import streamlit as st
import io
from contextlib import redirect_stdout

from motor_redis.consultas.consultasBasicas_redis import *
from motor_redis.consultas.consultasAvanzadas_redis import *
from motor_redis.crud.crud_redis import *
from sincronizacion_simultanea.sinc_simu_redis_cassandra import finalizarCarreraSimultanea

# =========================================================
# FUNCIÓN AUXILIAR PARA CAPTURAR SALIDA DE CONSOLA
# =========================================================
def ejecutar_consulta_y_capturar_output(func, *args, **kwargs):
    """
    Ejecuta una función de consulta Redis y captura todo lo que la función
    imprime por consola.

    Esto permite reutilizar funciones diseñadas para consola dentro de
    Streamlit, mostrando el resultado en la interfaz web.
    """
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Error en la ejecución web: {e}")
    valor_final = f.getvalue()

    if not valor_final:
        valor_final = "La consulta se ejecutó pero no devolvió texto de salida."

    return valor_final

# =========================================================
# VISTA PRINCIPAL DE REDIS
# =========================================================
def mostrar_redis(redis_db,cassandra_session=None):
    """
    Renderiza la pestaña de Redis dentro del dashboard.

    Recibe una conexión activa a Redis y permite ejecutar operaciones
    relacionadas con carreras, apuestas y simulación en tiempo real.
    """
    st.header("Simulación en tiempo real - Redis")

    # Validación inicial de conexión.
    if redis_db is None:
        st.error("No se pudo conectar a la base de datos Redis.")
        return

    # Variables de control de la vista.
    output_resultado = ""
    opcion = None
    categoria = None
    id_carrera = ""
    cant_apuestas = None
    ejecutar = False

    # Variables específicas para operaciones CRUD.
    categoria_crud = None
    opcion_crud = None
    horse_id = ""
    monto_apuesta = None
    apuesta_id = ""
    nuevo_estado_carrera = ""
    nuevo_monto_apuesta = None
    nuevo_estado_apuesta = ""
    confirmar_borrado = False
    nombre_operacion = ""

    # Distribución principal de la pantalla:columna izquierda para controles, columna derecha para resultados.
    col1, col2 = st.columns([1, 1.8])

    # =========================================================
    # PANEL IZQUIERDO - CONTROLES
    # =========================================================
    with col1:
        with st.container(border=True):
            st.markdown("### Panel de Control")

            modo_operacion = st.radio("Modo de Operación",["Modificar Datos","Consultas/Simulación"],horizontal=True,key="modo_operacion_redis")

            # -----------------------------------------------------
            # CONSULTAS Y SIMULACIÓN
            # -----------------------------------------------------
            if modo_operacion == "Consultas/Simulación":
                categoria = st.radio("Tipo de consulta",["Simples", "Complejas"],key="btn_tipo_consulta_redis")

                # -------------------------------------------------
                # CONSULTAS SIMPLES
                # -------------------------------------------------
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
                    # La generación de apuestas requiere un parámetro adicional.
                    if opcion and opcion.startswith("2."):
                        cant_apuestas = st.number_input("Cantidad de apuestas a generar:",min_value=1,max_value=1000,value=10,key="cant_apuestas_redis")
                    id_carrera = st.text_input("Ingrese ID de la Carrera:", value="", placeholder="Ej: 2016-567",key="id_simple_redis").strip()
                    ejecutar = st.button("Ejecutar Consulta Simple", use_container_width=True, type="primary", key="btn_ejecutar_simple_redis")

                # -------------------------------------------------
                # CONSULTAS COMPLEJAS
                # -------------------------------------------------
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

            # -----------------------------------------------------
            # CRUD - ESTRUCTURA VISUAL
            # -----------------------------------------------------
            elif modo_operacion == "Modificar Datos":
                categoria_crud = st.radio("Operación CRUD",["Inserción", "Lectura","Actualización", "Borrado"],key="crud_redis")
                # -------------------------------------------------
                # CRUD - INSERCIÓN
                # -------------------------------------------------
                if categoria_crud == "Inserción":
                    st.markdown("**Inserción de registro en Redis**")
                    opcion_crud = st.selectbox("Seleccione la operación de inserción:",["1. Crear apuesta manual"],key="select_insert_redis")

                    id_carrera = st.text_input("Ingrese ID de la Carrera:",value="",placeholder="Ej: 2016-567",key="id_insert_redis").strip()
                    horse_id = st.text_input("Ingrese ID del caballo:",value="",placeholder="Ej: 12345",key="horse_insert_redis").strip()
                    monto_apuesta = st.number_input("Ingrese monto de la apuesta:",min_value=1.0,value=100.0,step=50.0,key="monto_insert_redis")

                    ejecutar = st.button("Ejecutar Inserción",use_container_width=True,type="primary",key="btn_insert_redis")

                # -------------------------------------------------
                # CRUD - LECTURA
                # -------------------------------------------------
                elif categoria_crud == "Lectura":
                    st.markdown("**Lectura de registro en Redis**")
                    opcion_crud = st.selectbox("Seleccione la operación de lectura:",["1. Buscar carrera","2. Buscar apuesta"],key="select_read_redis")

                    id_carrera = st.text_input("Ingrese ID de la Carrera:",value="",placeholder="Ej: 2016-567",key="id_read_redis").strip()
                    if opcion_crud and opcion_crud.startswith("2."):
                        apuesta_id = st.text_input("Ingrese ID de la apuesta:",value="",placeholder="Ej: 1",key="apuesta_read_redis").strip()

                    ejecutar = st.button("Ejecutar Lectura",use_container_width=True,type="primary",key="btn_read_redis")

                # -------------------------------------------------
                # CRUD - ACTUALIZACIÓN
                # -------------------------------------------------
                elif categoria_crud == "Actualización":
                    st.markdown("**Actualización de registro en Cassandra**")
                    opcion_crud = st.selectbox(
                        "Seleccione la operación de actualización:",["1. Actualizar estado de carrera","2. Actualizar apuesta"],key="select_update_redis")

                    id_carrera = st.text_input("Ingrese ID de la Carrera:",value="",placeholder="Ej: 2016-567",key="id_update_redis").strip()
                    if opcion_crud and opcion_crud.startswith("1."):
                        nuevo_estado_carrera = st.selectbox("Seleccione nuevo estado de la carrera:",["Creada", "En curso", "Finalizada"],key="estado_carrera_update_redis")

                    elif opcion_crud and opcion_crud.startswith("2."):
                        apuesta_id = st.text_input("Ingrese ID de la apuesta:",value="",placeholder="Ej: 1",key="apuesta_update_redis").strip()

                        nuevo_monto_apuesta = st.number_input("Nuevo monto de la apuesta:",min_value=0.0,value=0.0,step=50.0,key="monto_update_redis")

                        nuevo_estado_apuesta = st.selectbox("Nuevo estado de la apuesta:",["Activa", "Ganada", "Perdida"],key="estado_apuesta_update_redis")

                    ejecutar = st.button("Ejecutar Actualización",use_container_width=True,type="primary",key="btn_update_redis")

                # -------------------------------------------------
                # CRUD - BORRADO
                # -------------------------------------------------
                elif categoria_crud == "Borrado":
                    st.markdown("**Borrado de registro en Cassandra**")
                    opcion_crud = st.selectbox("Seleccione la operación de borrado:",["1. Borrar apuesta","2. Borrar carrera completa"],key="select_delete_redis")

                    id_carrera = st.text_input("Ingrese ID de la Carrera:",value="",placeholder="Ej: 2016-567",key="id_delete_redis").strip()

                    if opcion_crud and opcion_crud.startswith("1."):
                        apuesta_id = st.text_input("Ingrese ID de la apuesta:",value="",placeholder="Ej: 1",key="apuesta_delete_redis").strip()

                    if opcion_crud and opcion_crud.startswith("2."):
                        confirmar_borrado = st.checkbox("Confirmo que deseo borrar la carrera completa y todos sus datos asociados.",key="confirm_delete_carrera_redis")

                    ejecutar = st.button("Ejecutar Borrado",use_container_width=True,type="primary",key="btn_delete_redis")

    # =========================================================
    # PANEL DERECHO - SALIDA
    # =========================================================
    with col2:
        st.subheader("Consola de Salida")

        # Ejecuta la consulta seleccionada desde el panel izquierdo.
        if ejecutar:
            if not id_carrera:
                st.warning("El ID de la carrera es obligatorio para todas las consultas.")
            else:
                with st.spinner('Ejecutando comando en Redis...'):

                    # ---------------------------------------------
                    # EJECUCIÓN DE CONSULTAS SIMPLES
                    # ---------------------------------------------
                    if categoria == "Simples" and opcion:
                        if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(crearCarrera, redis_db, id_carrera)
                        elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(generarApuestasFicticias, redis_db, id_carrera, cant_apuestas)
                        elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(verEstadoCarrera, redis_db, id_carrera)
                        elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(verParticipantes, redis_db, id_carrera)
                        elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(verApuestasActivas, redis_db, id_carrera)

                    # ---------------------------------------------
                    # EJECUCIÓN DE CONSULTAS COMPLEJAS
                    # ---------------------------------------------
                    elif categoria == "Complejas" and opcion:
                        if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(simularCarrera, redis_db, id_carrera)
                        elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(verRanking, redis_db, id_carrera)
                        elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(obtenerGanador, redis_db, id_carrera)
                        elif opcion.startswith("4."):
                            output_resultado = ejecutar_consulta_y_capturar_output(
                                finalizarCarreraSimultanea, redis_db, cassandra_session, id_carrera
                            )
                        elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(actualizarApuestas, redis_db, id_carrera)
                        elif opcion.startswith("6."):output_resultado = ejecutar_consulta_y_capturar_output(expirarDatosCarrera, redis_db, id_carrera)

                    # ---------------------------------------------
                    # EJECUCIÓN DE OPERACIONES CRUD
                    # ---------------------------------------------
                    elif categoria_crud == "Inserción" and opcion_crud:
                        nombre_operacion = opcion_crud

                        if opcion_crud.startswith("1."):
                            if not horse_id:st.warning("El ID del caballo es obligatorio para crear la apuesta.")
                            else:
                                output_resultado = ejecutar_consulta_y_capturar_output(crearApuestaManual,redis_db,id_carrera,horse_id,monto_apuesta)

                    elif categoria_crud == "Lectura" and opcion_crud:
                        nombre_operacion = opcion_crud

                        if opcion_crud.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(buscarCarrera,redis_db,id_carrera)

                        elif opcion_crud.startswith("2."):
                            if not apuesta_id:
                                st.warning("El ID de la apuesta es obligatorio para buscarla.")
                            else:
                                output_resultado = ejecutar_consulta_y_capturar_output(buscarApuesta,redis_db,id_carrera,apuesta_id)

                    elif categoria_crud == "Actualización" and opcion_crud:
                        nombre_operacion = opcion_crud

                        if opcion_crud.startswith("1."):
                            if nuevo_estado_carrera.strip().lower() == "finalizada":
                                output_resultado = ejecutar_consulta_y_capturar_output(
                                    finalizarCarreraSimultanea, redis_db, cassandra_session, id_carrera)
                            else:
                                output_resultado = ejecutar_consulta_y_capturar_output(
                                    actualizarEstadoCarrera, redis_db, id_carrera, nuevo_estado_carrera)

                        elif opcion_crud.startswith("2."):
                            if not apuesta_id:
                                st.warning("El ID de la apuesta es obligatorio para actualizarla.")
                            else:
                                output_resultado = ejecutar_consulta_y_capturar_output(actualizarApuesta,redis_db,id_carrera,apuesta_id,nuevo_monto_apuesta,nuevo_estado_apuesta)

                    elif categoria_crud == "Borrado" and opcion_crud:
                        nombre_operacion = opcion_crud

                        if opcion_crud.startswith("1."):
                            if not apuesta_id:
                                st.warning("El ID de la apuesta es obligatorio para borrarla.")
                            else:
                                output_resultado = ejecutar_consulta_y_capturar_output(borrarApuesta,redis_db,id_carrera,apuesta_id)

                        elif opcion_crud.startswith("2."):
                            if not confirmar_borrado:
                                st.warning("Para borrar una carrera completa, primero debe confirmar la operación.")
                            else:
                                output_resultado = ejecutar_consulta_y_capturar_output(borrarCarrera,redis_db,id_carrera)

        # =========================================================
        # RENDERIZADO DEL RESULTADO
        # =========================================================
        if output_resultado:
            # Determina el nombre de la operación ejecutada, contemplando tanto consultas como CRUD.
            if opcion is not None:
                    operacion_actual = opcion
            elif opcion_crud is not None:
                operacion_actual = opcion_crud
            else:
                operacion_actual = "operacion_redis"

            consulta_limpia = operacion_actual.split(". ", 1)[-1].replace(" ", "_").lower()
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