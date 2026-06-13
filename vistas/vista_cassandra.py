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

from motor_cassandra.consultas.consultasBasicas_cassandra import *
from motor_cassandra.consultas.consultasAvanzadas_cassandra import *


# =========================================================
# FUNCIÓN AUXILIAR PARA CAPTURAR SALIDA DE CONSOLA
# =========================================================
def ejecutar_consulta_y_capturar_output(func, *args, **kwargs):
    """
    Ejecuta una función de consulta Cassandra y captura todo lo que imprime
    por consola.

    Esto permite reutilizar funciones pensadas para ejecución por terminal
    dentro de Streamlit, mostrando el resultado en la consola de salida web.
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

    Recibe una sesión activa de Cassandra y permite seleccionar operaciones
    de consulta o gestión de datos desde un panel lateral.
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
                categoria_crud = st.radio("Operación CRUD",["Inserción", "Actualización", "Borrado"],key="crud_cassandra")

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
                            "1. Consulta simple 1",
                            "2. Consulta simple 2",
                            "3. Consulta simple 3",
                            "4. Consulta simple 4",
                            "5. Consulta simple 5"
                        ],
                        key="select_simple_cassandra"
                    )

                    id_carrera = st.text_input("Ingrese ID de la Carrera:",value="",placeholder="Ej: 2016-567",key="id_simple_cassandra").strip()

                    ejecutar = st.button("Ejecutar Consulta Simple",use_container_width=True,type="primary",key="btn_ejecutar_s_cassandra")

                # -------------------------------------------------
                # CONSULTAS COMPLEJAS
                # -------------------------------------------------
                elif categoria == "Complejas":
                    opcion = st.selectbox(
                        "Seleccione la consulta compleja:",
                        [
                            "1. Consulta compleja 1",
                            "2. Consulta compleja 2",
                            "3. Consulta compleja 3",
                            "4. Consulta compleja 4",
                            "5. Consulta compleja 5"
                        ],
                        key="select_compleja_cassandra"
                    )

                    parametro = st.text_input(
                        "Ingrese parámetro de búsqueda:",
                        value="",
                        placeholder="Ej: GOLDEN DRAGON / 2016-567",
                        key="parametro_cassandra"
                    ).upper().strip()

                    ejecutar = st.button(
                        "Ejecutar Consulta Compleja",
                        use_container_width=True,
                        type="primary",
                        key="btn_ejecutar_c_cassandra"
                    )

    # =========================================================
    # PANEL DERECHO - SALIDA
    # =========================================================
    with col2:
        st.subheader("Consola de Salida")
        # Ejecuta la consulta seleccionada desde el panel izquierdo.
        if ejecutar:
            with st.spinner("Consultando en Cassandra..."):

                # ---------------------------------------------
                # EJECUCIÓN DE CONSULTAS SIMPLES
                # ---------------------------------------------
                if categoria == "Simples" and opcion:
                    if not id_carrera:
                        st.warning("El ID de la carrera es obligatorio para esta consulta.")
                    else:
                        if opcion.startswith("1."):output_resultado = "Pendiente: conectar función simple 1 de Cassandra."
                        elif opcion.startswith("2."):output_resultado = "Pendiente: conectar función simple 2 de Cassandra."
                        elif opcion.startswith("3."):output_resultado = "Pendiente: conectar función simple 3 de Cassandra."
                        elif opcion.startswith("4."):output_resultado = "Pendiente: conectar función simple 4 de Cassandra."
                        elif opcion.startswith("5."):output_resultado = "Pendiente: conectar función simple 5 de Cassandra."

                # ---------------------------------------------
                # EJECUCIÓN DE CONSULTAS COMPLEJAS
                # ---------------------------------------------
                elif categoria == "Complejas" and opcion:
                    if not parametro:
                        st.warning("Por favor, ingresá un parámetro antes de ejecutar la consulta.")
                    else:
                        if opcion.startswith("1."):output_resultado = "Pendiente: conectar función compleja 1 de Cassandra."

                        elif opcion.startswith("2."):output_resultado = "Pendiente: conectar función compleja 2 de Cassandra."

                        elif opcion.startswith("3."):output_resultado = "Pendiente: conectar función compleja 3 de Cassandra."

                        elif opcion.startswith("4."):output_resultado = "Pendiente: conectar función compleja 4 de Cassandra."

                        elif opcion.startswith("5."):output_resultado = "Pendiente: conectar función compleja 5 de Cassandra."

        # =========================================================
        # RENDERIZADO DEL RESULTADO
        # =========================================================
        if output_resultado:
            if opcion:
                accion_limpia = opcion.split(". ", 1)[-1].replace(" ", "_").lower()
            else:
                accion_limpia = "resultado"

            st.download_button(
                label="Descargar datos (TXT)",
                data=output_resultado,
                file_name=f"resultado_{accion_limpia}_cassandra.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.code(output_resultado, language="text")
        else:
            st.info("Seleccione una operación del panel izquierdo para visualizar los datos aquí.")