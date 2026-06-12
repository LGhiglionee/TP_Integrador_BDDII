import streamlit as st
import io
import sys

from motor_neo4j.consultas.consultasBasicas import *
from motor_neo4j.consultas.consultasAvanzadas import *

# MODIFICADO: Ahora es una función inteligente que se adapta a cualquier firma de backend
def ejecutar_consulta_y_capturar_output(func, session, valor_input=None):
    f_out = io.StringIO()
    entrada_simulada = f"{valor_input}\n" if valor_input is not None else "\n"
    f_in = io.StringIO(entrada_simulada)

    original_stdout = sys.stdout
    original_stdin = sys.stdin

    try:
        sys.stdout = f_out
        sys.stdin = f_in

        # 1. Intentamos mandarlo como parámetro directo (por si tu backend lo pide)
        try:
            func(session, valor_input)
        except TypeError as te:
            # 2. Si protesta por cantidad de argumentos, probamos pasándole solo la session
            if "argument" in str(te) or "positional" in str(te):
                func(session)
            else:
                raise te  # Si era otro tipo de TypeError, lo lanzamos

    except Exception as e:
        f_out.write(f"❌ ERROR EN EL BACKEND:\n{str(e)}\n")
    finally:
        sys.stdout = original_stdout
        sys.stdin = original_stdin

    valor_final = f_out.getvalue()
    if not valor_final:
        valor_final = "⚠️ La consulta se ejecutó pero no devolvió texto de salida."

    return valor_final

def mostrar_neo4j(driver):
    st.header("Consultas de Grafos - Neo4j")

    if driver is None:
        st.error("No se pudo conectar a la base de datos Neo4j.")
        return
    mensaje_crud = None
    tipo_mensaje = None
    ejecutar = False
    output_resultado = ""

    opcion = None
    categoria = None
    parametro = ""

    col1, col2 = st.columns([1, 1.8])

    with col1:
        with st.container(border=True):
            st.markdown("### Panel de Control")

            modo_operacion = st.radio("Modo de Operación",["Modificar Datos", "Consultas/Simulación"],horizontal=True,key="modo_operacion_neo4j")

            if modo_operacion == "Modificar Datos":
                categoria_crud = st.radio("Operación CRUD",["Inserción", "Actualización", "Borrado"],key="crud_neo4j")
            elif modo_operacion == "Consultas/Simulación":
                categoria = st.radio("Tipo de consulta",["Simples", "Complejas"],key="btn_tipo_consulta_neo4j")

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
                            ejecutar = st.button("Ejecutar Consulta Simple", use_container_width=True, type="primary", key="btn_ejecutar_consulta_s_neo4j")

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

                    ejecutar = st.button("Ejecutar Consulta Compleja", use_container_width=True, type="primary", key="btn_ejecutar_consulta_c_neo4j")

    with col2:
        st.subheader("Consola de Salida")
        if ejecutar:
            if categoria == "Complejas" and not parametro:
                st.warning("Por favor, ingrese un nombre antes de ejecutar la consulta.")
            else:
                with st.spinner('Consultando el grafo en Neo4j...'):
                    with driver.session(database="neo4j") as session:

                        if categoria == "Simples" and opcion:
                            if opcion.startswith("1."): output_resultado = ejecutar_consulta_y_capturar_output(listar_todos_entrenadores, session)
                            elif opcion.startswith("2."): output_resultado = ejecutar_consulta_y_capturar_output(caballos_ganadores, session)
                            elif opcion.startswith("3."): output_resultado = ejecutar_consulta_y_capturar_output(cantidad_total_caballos, session)
                            elif opcion.startswith("4."): output_resultado = ejecutar_consulta_y_capturar_output(entrenadores_letra_p, session)
                            elif opcion.startswith("5."): output_resultado = ejecutar_consulta_y_capturar_output(caballos_con_dragon, session)

                        elif categoria == "Complejas" and opcion:
                            if opcion.startswith("1."): output_resultado = ejecutar_consulta_y_capturar_output(buscar_caballo_nombre, session, parametro)
                            elif opcion.startswith("2."): output_resultado = ejecutar_consulta_y_capturar_output(recomendacion_entrenador_matchmaking, session, parametro)
                            elif opcion.startswith("3."): output_resultado = ejecutar_consulta_y_capturar_output(caballos_similares_diamante, session, parametro)
                            elif opcion.startswith("4."): output_resultado = ejecutar_consulta_y_capturar_output(recomendacion_apuestas_linaje, session, parametro)
                            elif opcion.startswith("5."): output_resultado = ejecutar_consulta_y_capturar_output(linea_sangre_caballo, session, parametro)
                            elif opcion.startswith("6."): output_resultado = ejecutar_consulta_y_capturar_output(ranking_entrenadores_por_linaje, session, parametro)

        if output_resultado:
            accion_limpia = opcion.split(". ", 1)[-1].replace(" ", "_").lower()

            if categoria == "Complejas" and parametro:
                    parametro_limpio = parametro.replace(" ", "_").lower()
                    nombre_final_archivo = f"resultado_{accion_limpia}_{parametro_limpio}_neo4j.txt"
            else:
                nombre_final_archivo = f"resultado_{accion_limpia}_neo4j.txt"
            st.download_button(
                label="Descargar datos (TXT)",
                data=output_resultado,
                file_name=nombre_final_archivo,
                mime="text/plain",
                use_container_width=True
            )
            st.code(output_resultado, language="text")
        else:
            st.info("Seleccione una consulta del panel izquierdo y presiona el botón para visualizar los datos aquí.")