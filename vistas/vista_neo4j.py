import streamlit as st
import io
import sys

from motor_neo4j.consultas.consultasBasicas_neo4j import *
from motor_neo4j.consultas.consultasAvanzadas_neo4j import *
from motor_neo4j.crud.crud_neo4j import *

def ejecutar_consulta_y_capturar_output(func, session, valor_input=None):
    f_out = io.StringIO()
    entrada_simulada = f"{valor_input}\n" if valor_input is not None else "\n"
    f_in = io.StringIO(entrada_simulada)

    original_stdout = sys.stdout
    original_stdin = sys.stdin

    try:
        sys.stdout = f_out
        sys.stdin = f_in
        try:
            if valor_input is not None:
                func(session, valor_input)
            else:
                func(session)
        except TypeError as te:
            if "argument" in str(te) or "positional" in str(te):
                func(session)
            else:
                raise te

    except Exception as e:
        f_out.write(f"Error backend:\n{str(e)}\n")
    finally:
        sys.stdout = original_stdout
        sys.stdin = original_stdin

    valor_final = f_out.getvalue()
    if not valor_final:
        valor_final = "La consulta se ejecutó pero no devolvió texto de salida."

    return valor_final

def armar_salida_insercion_neo4j(datos):
    salida = "Se insertó el registro en Neo4j\n\n"

    salida += "Nodo Caballo:\n"
    salida += f"ID Caballo: {datos.get('horse_id')}\n"
    salida += f"Nombre: {datos.get('horse_name')}\n"
    salida += f"Número: {datos.get('horse_number') or 'Sin cargar'}\n\n"

    salida += "Nodo Carrera:\n"
    salida += f"ID Carrera: {datos.get('race_id')}\n\n"

    salida += "Relación CORRIO:\n"
    salida += f"Posición final: {datos.get('finishing_position') or 'Sin cargar'}\n"
    salida += f"Posición de salida: {datos.get('draw') or 'Sin cargar'}\n"
    salida += f"Tiempo: {datos.get('finish_time') or 'Sin cargar'}\n"
    salida += f"Tiempo en segundos: {datos.get('finish_time_seconds') or 'Sin cargar'}\n"
    salida += f"Peso actual: {datos.get('actual_weight') or 'Sin cargar'}\n"
    salida += f"Peso declarado: {datos.get('declared_horse_weight') or 'Sin cargar'}\n"
    salida += f"Posición parcial 1: {datos.get('running_position_1') or 'Sin cargar'}\n"
    salida += f"Posición parcial 2: {datos.get('running_position_2') or 'Sin cargar'}\n"
    salida += f"Posición parcial 3: {datos.get('running_position_3') or 'Sin cargar'}\n\n"

    salida += "Relaciones adicionales:\n"
    salida += f"Entrenado por: {datos.get('trainer') or 'Desconocido'}\n"
    salida += f"Montado por: {datos.get('jockey') or 'Desconocido'}\n"
    salida += f"Padre: {datos.get('father') or 'Desconocido'}\n"
    salida += f"Madre: {datos.get('mother') or 'Desconocida'}\n"
    salida += f"Abuelo: {datos.get('gfather') or 'Desconocido'}\n"

    return salida

def armar_salida_borrado_neo4j(tipo_borrado, horse_id, race_id=None, resultado=None):
    salida = "Se eliminó el registro de Neo4j\n\n"

    salida += f"ID Caballo: {horse_id}\n"

    if race_id:
        salida += f"ID Carrera: {race_id}\n"

    if resultado:
        if resultado.get("nombre"):
            salida += f"Nombre del caballo: {resultado.get('nombre')}\n"
        if resultado.get("carrera_id"):
            salida += f"Carrera eliminada: {resultado.get('carrera_id')}\n"

    return salida

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

    if "neo4j_ultimo_resultado_crud" not in st.session_state:
        st.session_state["neo4j_ultimo_resultado_crud"] = ""

    if "neo4j_ultimo_archivo_crud" not in st.session_state:
        st.session_state["neo4j_ultimo_archivo_crud"] = "resultado_crud_neo4j.txt"

    col1, col2 = st.columns([1, 1.8])
    with col1:
        with st.container(border=True):
            st.markdown("### Panel de Control")

            modo_operacion = st.radio("Modo de Operación",["Modificar Datos", "Consultas/Simulación"],horizontal=True,key="modo_operacion_neo4j")

            if modo_operacion == "Modificar Datos":
                categoria_crud = st.radio("Operación CRUD",["Inserción", "Borrado"],key="crud_neo4j")

                if categoria_crud == "Inserción":
                    with st.form("form_insercion_neo4j", clear_on_submit=True):
                        st.markdown("**Inserción de registro en Neo4j**")

                        horse_id = st.text_input("ID Caballo (Obligatorio):",value="",placeholder="Ej: A177",key="neo4j_insert_horse_id").upper().strip()
                        horse_name = st.text_input("Nombre del Caballo (Obligatorio):",value="",placeholder="Ej: ENCORE BOY",key="neo4j_insert_horse_name").upper().strip()
                        race_id = st.text_input("ID Carrera (Obligatorio):",value="",placeholder="Ej: 2016-783",key="neo4j_insert_race_id").upper().strip()
                        jockey = st.text_input("Jockey:",value="",placeholder="Ej: Z Purton",key="neo4j_insert_jockey").strip()
                        trainer = st.text_input("Entrenador:",value="",placeholder="Ej: P F Yiu",key="neo4j_insert_trainer").strip()

                        with st.expander("Ver campos opcionales"):
                            colA, colB = st.columns(2)
                            with colA:
                                horse_number = st.text_input("N° Caballo:",value="",key="neo4j_insert_horse_number").strip()
                                father = st.text_input("Padre:",value="",key="neo4j_insert_father").upper().strip()
                                mother = st.text_input("Madre:",value="",key="neo4j_insert_mother").upper().strip()
                                gfather = st.text_input("Abuelo:",value="",key="neo4j_insert_gfather").upper().strip()
                                actual_weight = st.text_input("Peso actual:",value="",key="neo4j_insert_actual_weight").strip()
                                declared_horse_weight = st.text_input("Peso declarado:",value="",key="neo4j_insert_declared_weight").strip()
                            with colB:
                                draw = st.text_input("Posición salida:",value="",key="neo4j_insert_draw").strip()
                                finishing_position = st.text_input("Posición final:",value="",key="neo4j_insert_finishing_position").strip()
                                running_position_1 = st.text_input("Posición parcial 1:",value="",key="neo4j_insert_running_1").strip()
                                running_position_2 = st.text_input("Posición parcial 2:",value="",key="neo4j_insert_running_2").strip()
                                running_position_3 = st.text_input("Posición parcial 3:",value="",key="neo4j_insert_running_3").strip()
                                finish_time = st.text_input("Tiempo:",value="",placeholder="Ej: 1.09.98",key="neo4j_insert_finish_time").strip()
                                finish_time_seconds = st.text_input("Tiempo en segundos:",value="",placeholder="Ej: 69,098",key="neo4j_insert_finish_time_seconds").strip()

                        btn_insertar = st.form_submit_button("Insertar Registro",type="primary",use_container_width=True)

                        if btn_insertar:
                            if not horse_id or not horse_name or not race_id:
                                mensaje_crud = "El ID del caballo, el nombre del caballo y el ID de carrera son obligatorios."
                                tipo_mensaje = "error"
                            else:
                                datos = {
                                    "horse_id": horse_id,"horse_name": horse_name,"race_id": race_id,"jockey": jockey,
                                    "trainer": trainer,"horse_number": horse_number,"father": father,"mother": mother,"gfather": gfather,
                                    "actual_weight": actual_weight,"declared_horse_weight": declared_horse_weight,"draw": draw,
                                    "finishing_position": finishing_position,"running_position_1": running_position_1,"running_position_2": running_position_2,
                                    "running_position_3": running_position_3,"finish_time": finish_time,"finish_time_seconds": finish_time_seconds
                                }

                                with driver.session(database="neo4j") as session:
                                    existe = buscar_participacion_caballo(session,horse_id,race_id)

                                    if existe:
                                        mensaje_crud = f"El caballo {horse_id} ya está registrado en la carrera {race_id}."
                                        tipo_mensaje = "error"
                                    else:
                                        insertar_registro_carrera(session, datos)
                                        mensaje_crud = f"Se insertó correctamente el caballo {horse_name} en la carrera {race_id}."
                                        tipo_mensaje = "success"

                                        st.session_state["neo4j_ultimo_resultado_crud"] = armar_salida_insercion_neo4j(datos)
                                        st.session_state["neo4j_ultimo_archivo_crud"] = f"resultado_insercion_{horse_id}_{race_id}_neo4j.txt"

                elif categoria_crud == "Borrado":
                    tipo_borrado = st.radio("Opciones de Eliminación:",["Eliminar caballo de una carrera específica","Eliminar caballo completo del grafo"],key="tipo_borrado_neo4j")

                    with st.form("form_borrado_neo4j", clear_on_submit=True):
                        if tipo_borrado == "Eliminar caballo de una carrera específica":
                            st.markdown("**Eliminar participación en una carrera específica**")

                            colBusqA, colBusqB = st.columns(2)
                            with colBusqA:horse_id_borrar = st.text_input("ID Caballo (Obligatorio):",value="",placeholder="Ej: A177",key="neo4j_delete_horse_id").upper().strip()

                            with colBusqB:race_id_borrar = st.text_input("ID Carrera (Obligatorio):",value="",placeholder="Ej: 2016-783",key="neo4j_delete_race_id").upper().strip()

                        else:
                            st.markdown("**Eliminar caballo completo del grafo**")
                            st.warning("Esto eliminará el nodo del caballo y todas sus relaciones.")

                            horse_id_borrar = st.text_input("ID Caballo (Obligatorio):",value="",placeholder="Ej: A177",key="neo4j_delete_all_horse_id").upper().strip()
                            race_id_borrar = None

                        btn_borrar = st.form_submit_button("Ejecutar Eliminación",type="primary",use_container_width=True)
                        if btn_borrar:
                            with driver.session(database="neo4j") as session:
                                if tipo_borrado == "Eliminar caballo de una carrera específica":
                                    if not horse_id_borrar or not race_id_borrar:
                                        mensaje_crud = "El ID del caballo y el ID de carrera son obligatorios."
                                        tipo_mensaje = "error"
                                    else:
                                        resultado = borrar_caballo_carrera_especifica(session,horse_id_borrar,race_id_borrar)
                                        if resultado["deleted_count"] > 0:
                                            mensaje_crud = f"Se eliminó la participación del caballo {horse_id_borrar} en la carrera {race_id_borrar}."
                                            tipo_mensaje = "success"

                                            st.session_state["neo4j_ultimo_resultado_crud"] = armar_salida_borrado_neo4j("Eliminar caballo de una carrera específica",horse_id_borrar,race_id_borrar,resultado)
                                            st.session_state["neo4j_ultimo_archivo_crud"] = f"resultado_borrado_{horse_id_borrar}_{race_id_borrar}_neo4j.txt"
                                        else:
                                            mensaje_crud = f"No se encontró al caballo {horse_id_borrar} participando en la carrera {race_id_borrar}."
                                            tipo_mensaje = "error"

                                else:
                                    if not horse_id_borrar:
                                        mensaje_crud = "El ID del caballo es obligatorio."
                                        tipo_mensaje = "error"
                                    else:
                                        resultado = borrar_caballo_completo(session,horse_id_borrar)
                                        if resultado["deleted_count"] > 0:
                                            mensaje_crud = f"Se eliminó completamente el caballo {horse_id_borrar} del grafo."
                                            tipo_mensaje = "success"

                                            st.session_state["neo4j_ultimo_resultado_crud"] = armar_salida_borrado_neo4j("Eliminar caballo completo del grafo",horse_id_borrar,None,resultado)
                                            st.session_state["neo4j_ultimo_archivo_crud"] = f"resultado_borrado_completo_{horse_id_borrar}_neo4j.txt"
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
                        ],
                        key="select_simple_neo4j"
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
                        ],
                        key="select_compleja_neo4j"
                    )

                    if opcion == "6. Mostrar ranking de entrenadores por linaje":parametro = st.text_input("Ingresar Nombre del Padre:", value="",key="param_padre_neo4j").upper().strip()
                    else:parametro = st.text_input("Ingresar Nombre del Caballo:", value="", key="param_caballo_neo4j").upper().strip()

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
            st.download_button(label="Descargar datos (TXT)",data=output_resultado,file_name=nombre_final_archivo,mime="text/plain",use_container_width=True)
            st.code(output_resultado, language="text")

        elif st.session_state.get("neo4j_ultimo_resultado_crud"):
            st.markdown("### Última operación realizada")
            st.download_button(label="Descargar datos (TXT)",data=st.session_state["neo4j_ultimo_resultado_crud"],file_name=st.session_state["neo4j_ultimo_archivo_crud"],mime="text/plain",use_container_width=True)

            st.code(st.session_state["neo4j_ultimo_resultado_crud"],language="text")

        else:
            st.info("Seleccione una consulta del panel izquierdo y presiona el botón para visualizar los datos aquí.")