"""
Vista de Cassandra para el dashboard EQUIDATA.

Este módulo construye la interfaz web correspondiente al motor Cassandra.
Permite organizar las consultas simples y complejas sobre tablas columnarizadas,
manteniendo una estructura visual homogénea con el resto de los motores del TP.

Actualmente la vista deja preparada la estructura de consultas y CRUD.
Las funciones específicas de Cassandra pueden conectarse dentro de los bloques
marcados como pendientes.
"""
import streamlit as st
import io
from contextlib import redirect_stdout

from motor_cassandra.Consultas.consultasBasicas_cassandra import *
from motor_cassandra.Consultas.consultasAvanzadas_cassandra import *
from motor_cassandra.crud.crud_cassandra import *

# =========================================================
# FUNCIÓN AUXILIAR PARA CAPTURAR SALIDA DE CONSOLA
# =========================================================
def ejecutar_consulta_y_capturar_output(func, *args, **kwargs):
    """
    Ejecuta una función de consulta Cassandra y captura todo lo que imprime
    por consola.
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
# VISTA PRINCIPAL DE CASSANDRA
# =========================================================
def mostrar_cassandra(session):
    """
    Renderiza la pestaña de Cassandra dentro del dashboard.
    Maneja el panel de control a la izquierda y la consola de salida a la derecha.
    """
    st.header("Consultas y Gestión Columnar - Cassandra")

    # Validación inicial de conexión.
    if session is None:
        st.error("No se pudo conectar a la base de datos Cassandra.")
        return

    # Variables generales de control de la vista.
    ejecutar = False
    output_resultado = ""
    opcion = None
    categoria = None
    parametro = ""
    id_carrera = ""

    # Variables específicas para operaciones CRUD.
    categoria_crud = None
    opcion_crud = None
    finishing_position = None
    horse_id = ""
    horse_number = None
    horse_name = ""
    jockey = ""
    trainer = ""
    finish_time = ""
    finish_time_seconds = None
    confirmar_borrado = False
    nombre_operacion = ""

    # Distribución principal:columna izquierda para controles, columna derecha para resultados.
    col1, col2 = st.columns([1, 1.8])

    # =========================================================
    # PANEL IZQUIERDO - CONTROLES
    # =========================================================
    with col1:
        with st.container(border=True):
            st.markdown("### Panel de Control")
            modo_operacion = st.radio("Modo de Operación",["Modificar Datos", "Consultas/Simulación"],horizontal=True,key="modo_operacion_cassandra")

            # -----------------------------------------------------
            # CRUD - ESTRUCTURA VISUAL
            # -----------------------------------------------------
            if modo_operacion == "Modificar Datos":
                categoria_crud = st.radio("Operación CRUD",["Inserción","Lectura","Actualización","Borrado"],key="crud_cassandra")
                # -------------------------------------------------
                # CRUD - INSERCIÓN
                # -------------------------------------------------
                if categoria_crud == "Inserción":
                    st.markdown("**Inserción de registro en Cassandra**")
                    opcion_crud = st.selectbox("Seleccione la operación de inserción:",["1. Crear resultado manual"],key="select_insert_cassandra")

                    id_carrera = st.text_input("Ingrese ID de la Carrera:",value="",placeholder="Ej: 2016-567",key="id_insert_cassandra").strip()
                    finishing_position = st.number_input("Ingrese Posición de Llegada:",min_value=1,max_value=100,value=1,key="pos_insert_cassandra")
                    horse_id = st.text_input("Ingrese ID del caballo:",value="",placeholder="Ej: 12345",key="horse_insert_cassandra").strip()
                    horse_number = st.number_input("Ingrese Número de Mantilla (#):",min_value=1,max_value=100,value=1,key="num_insert_cassandra")
                    horse_name = st.text_input("Ingrese Nombre del Caballo:",value="",key="name_insert_cassandra").strip()
                    jockey = st.text_input("Ingrese Nombre del Jockey:",value="",key="jockey_insert_cassandra").strip()
                    trainer = st.text_input("Ingrese Nombre del Entrenador:",value="",key="trainer_insert_cassandra").strip()
                    finish_time = st.text_input("Ingrese Tiempo (Texto):",value="",placeholder="Ej: 1.22.45",key="time_insert_cassandra").strip()
                    finish_time_seconds = st.number_input("Ingrese Tiempo (Segundos):",min_value=0.0,value=0.0,step=0.1,key="seconds_insert_cassandra")

                    ejecutar = st.button("Ejecutar Inserción",use_container_width=True,type="primary",key="btn_insert_cassandra")

                # -------------------------------------------------
                # CRUD - LECTURA
                # -------------------------------------------------
                elif categoria_crud == "Lectura":
                    st.markdown("**Lectura de registro en Cassandra**")
                    opcion_crud = st.selectbox("Seleccione la operación de lectura:",["1. Buscar resultado específico"],key="select_read_cassandra")

                    id_carrera = st.text_input("Ingrese ID de la Carrera:",value="",placeholder="Ej: 2016-567",key="id_read_cassandra").strip()
                    finishing_position = st.number_input("Ingrese Posición de Llegada:",min_value=1,max_value=100,value=1,key="pos_read_cassandra")
                    horse_id = st.text_input("Ingrese ID del caballo:",value="",placeholder="Ej: 12345",key="horse_read_cassandra").strip()

                    ejecutar = st.button("Ejecutar Lectura",use_container_width=True,type="primary",key="btn_read_cassandra")

                # -------------------------------------------------
                # CRUD - ACTUALIZACIÓN
                # -------------------------------------------------
                elif categoria_crud == "Actualización":
                    st.markdown("**Actualización de registro en Cassandra**")
                    opcion_crud = st.selectbox("Seleccione la operación de actualización:",["1. Actualizar tiempo de resultado"],key="select_update_cassandra")

                    id_carrera = st.text_input("Ingrese ID de la Carrera:",value="",placeholder="Ej: 2016-567",key="id_update_cassandra").strip()
                    finishing_position = st.number_input("Ingrese Posición de Llegada:",min_value=1,max_value=100,value=1,key="pos_update_cassandra")
                    horse_id = st.text_input("Ingrese ID del caballo:",value="",placeholder="Ej: 12345",key="horse_update_cassandra").strip()
                    finish_time = st.text_input("Nuevo Tiempo (Texto):",value="",placeholder="Ej: 1.20.15",key="time_update_cassandra").strip()
                    finish_time_seconds = st.number_input("Nuevo Tiempo (Segundos):",min_value=0.0,value=0.0,step=0.1,key="seconds_update_cassandra")

                    ejecutar = st.button("Ejecutar Actualización",use_container_width=True,type="primary",key="btn_update_cassandra")

                # -------------------------------------------------
                # CRUD - BORRADO
                # -------------------------------------------------
                elif categoria_crud == "Borrado":
                    st.markdown("**Borrado de registro en Cassandra**")
                    opcion_crud = st.selectbox("Seleccione la operación de borrado:",["1. Borrar resultado específico"],key="select_delete_cassandra")

                    id_carrera = st.text_input("Ingrese ID de la Carrera:",value="",placeholder="Ej: 2016-567",key="id_delete_cassandra").strip()
                    finishing_position = st.number_input("Ingrese Posición de Llegada:",min_value=1,max_value=100,value=1,key="pos_delete_cassandra")
                    horse_id = st.text_input("Ingrese ID del caballo:",value="",placeholder="Ej: 12345",key="horse_delete_cassandra").strip()
                    confirmar_borrado = st.checkbox("Confirmo que deseo borrar este resultado de carrera específico.",key="confirm_delete_resultado_cassandra")

                    ejecutar = st.button("Ejecutar Borrado",use_container_width=True,type="primary",key="btn_delete_cassandra")

            # -----------------------------------------------------
            # CONSULTAS Y SIMULACIÓN
            # -----------------------------------------------------
            elif modo_operacion == "Consultas/Simulación":
                categoria = st.radio("Tipo de consulta",["Simples", "Complejas"],key="btn_tipo_consulta_cassandra")

                # -------------------------------------------------
                # CONSULTAS SIMPLES
                # -------------------------------------------------
                if categoria == "Simples":
                    opcion = st.selectbox(
                        "Seleccione la consulta simple:",
                        [
                            "1. Ver resultado completo de una carrera",
                            "2. Ver ganador definitivo de una carrera",
                            "3. Ver podio (Top 3) de una carrera",
                            "4. Ver historial completo de un caballo",
                            "5. Ver historial completo de un jockey"
                        ],
                        key="select_simple_cassandra"
                    )

                    if opcion.startswith("4."):
                        lbl = "Ingrese ID del Caballo:"
                    elif opcion.startswith("5."):
                        lbl = "Ingrese Nombre del Jockey:"
                    else:
                        lbl = "Ingrese ID de la Carrera:"

                    id_carrera = st.text_input(lbl, value="", placeholder="Ej: 2016-567",key="id_simple_cassandra").strip()
                    ejecutar = st.button("Ejecutar Consulta Simple",use_container_width=True,type="primary",key="btn_ejecutar_s_cassandra")

                # -------------------------------------------------
                # CONSULTAS COMPLEJAS
                # -------------------------------------------------
                elif categoria == "Complejas":
                    opcion = st.selectbox(
                        "Seleccione la consulta compleja:",
                        [
                            "1. Ver rendimiento analítico de un caballo",
                            "2. Ver rendimiento analítico de un jockey",
                            "3. Filtrar últimas N carreras de un caballo",
                            "4. Filtrar últimas N carreras de un jockey",
                            "5. Ver todos los caballos"
                        ],
                        key="select_compleja_cassandra"
                    )

                    if opcion and (opcion.startswith("3.") or opcion.startswith("4.") or opcion.startswith("5.")):
                        limite_filas = st.number_input("Cantidad de registros (Límite):",min_value=1,max_value=100,value=5,key="limite_compleja_cassandra")

                    if opcion.startswith("1.") or opcion.startswith("3."):
                        lbl = "Ingrese ID del Caballo:"
                    elif opcion.startswith("2.") or opcion.startswith("4."):
                        lbl = "Ingrese Nombre del Jockey:"

                    id_carrera = st.text_input(lbl, value="", placeholder="Ej: 2016-567",key="id_compleja_cassandra").strip()
                    ejecutar = st.button("Ejecutar Consulta Compleja",use_container_width=True,type="primary",key="btn_ejecutar_c_cassandra")

    # =========================================================
    # PANEL DERECHO - SALIDA
    # =========================================================
    with col2:
        st.subheader("Consola de Salida")
        # Ejecuta la consulta seleccionada desde el panel izquierdo.
        if ejecutar:
            if not id_carrera:
                st.warning("El parámetro o ID de búsqueda es obligatorio para todas las consultas.")
            with st.spinner("Consultando en Cassandra..."):
                # ---------------------------------------------
                # EJECUCIÓN DE CONSULTAS SIMPLES
                # ---------------------------------------------
                if categoria == "Simples" and opcion:
                    if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(verResultadoCarrera, session, id_carrera)
                    elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(verGanadorCarrera, session, id_carrera)
                    elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(verTopTresCarrera, session, id_carrera)
                    elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(verHistorialCaballo, session, id_carrera)
                    elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(verHistorialJockey, session, id_carrera)

                # ---------------------------------------------
                # EJECUCIÓN DE CONSULTAS COMPLEJAS
                # ---------------------------------------------
                elif categoria == "Complejas" and opcion:
                    if opcion.startswith("1."):output_resultado = ejecutar_consulta_y_capturar_output(verRendimientoCaballo, session, id_carrera)
                    elif opcion.startswith("2."):output_resultado = ejecutar_consulta_y_capturar_output(verJockeyPorPosicionFinalDelCaballo, session, id_carrera)
                    elif opcion.startswith("3."):output_resultado = ejecutar_consulta_y_capturar_output(verEntrenadorPorJockey, session, id_carrera)
                    elif opcion.startswith("4."):output_resultado = ejecutar_consulta_y_capturar_output(verTiempoPromedioPorDupla, session, id_carrera, limite_filas)
                    elif opcion.startswith("5."):output_resultado = ejecutar_consulta_y_capturar_output(verCaballos, session)

                # ---------------------------------------------
                # EJECUCIÓN DE OPERACIONES CRUD
                # ---------------------------------------------
                elif categoria_crud == "Inserción" and opcion_crud:
                    nombre_operacion = opcion_crud
                    if opcion_crud.startswith("1."):
                        if not horse_id or not horse_name:st.warning("El ID y Nombre del caballo son obligatorios para crear el registro.")
                        else:
                            output_resultado = ejecutar_consulta_y_capturar_output(crear_resultado_manual,session,id_carrera,finishing_position,horse_id,horse_number,horse_name,jockey,trainer,finish_time,finish_time_seconds)

                elif categoria_crud == "Lectura" and opcion_crud:
                    nombre_operacion = opcion_crud
                    if opcion_crud.startswith("1."):
                        if not horse_id:st.warning("El ID del caballo es obligatorio para buscar el registro.")
                        else:
                            output_resultado = ejecutar_consulta_y_capturar_output(leer_resultado_especifico,session,id_carrera,finishing_position,horse_id)

                elif categoria_crud == "Actualización" and opcion_crud:
                    nombre_operacion = opcion_crud
                    if opcion_crud.startswith("1."):
                        if not horse_id:st.warning("El ID del caballo es obligatorio para actualizar el registro.")
                        else:
                            output_resultado = ejecutar_consulta_y_capturar_output(actualizar_tiempo_resultado,session,id_carrera,finishing_position,horse_id,finish_time,finish_time_seconds)

                elif categoria_crud == "Borrado" and opcion_crud:
                    nombre_operacion = opcion_crud
                    if opcion_crud.startswith("1."):
                        if not horse_id:st.warning("El ID del caballo es obligatorio para borrar el registro.")
                        elif not confirmar_borrado:st.warning("Para borrar este registro, primero debe confirmar la operación.")
                        else:
                            output_resultado = ejecutar_consulta_y_capturar_output(eliminar_resultado_especifico,session,id_carrera,finishing_position,horse_id)
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
                operacion_actual = "operacion_cassandra"

            consulta_limpia = operacion_actual.split(". ", 1)[-1].replace(" ", "_").lower()
            id_limpio = id_carrera.replace(" ", "_").lower()

            st.download_button(
                label="Descargar datos (TXT)",
                data=output_resultado,
                file_name=f"resultado_{consulta_limpia}_{id_limpio}_cassandra.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.code(output_resultado, language="text")
        else:
            st.info("Seleccione una operación del panel izquierdo para visualizar los datos aquí.")