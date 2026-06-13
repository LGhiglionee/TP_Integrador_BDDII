"""
Vista de MongoDB para el dashboard EQUIDATA.

Este módulo construye la interfaz web correspondiente al motor documental MongoDB.
Permite realizar operaciones CRUD sobre la colección de caballos y ejecutar
consultas simples, complejas e historial por nombre.

La vista reutiliza funciones de backend que originalmente imprimen resultados
por consola, capturando esa salida para mostrarla dentro de Streamlit.
"""
import streamlit as st
import io
import builtins
from contextlib import redirect_stdout

from motor_mongo.consultas.consultasBasicas_mongo import *
from motor_mongo.consultas.consultasAvanzadas_mongo import *
from motor_mongo.crud.crud_mongo import *

# =========================================================
# FUNCIÓN AUXILIAR PARA CAPTURAR SALIDA DE CONSOLA
# =========================================================
def ejecutar_consulta_y_capturar_output(func, *args, **kwargs):
    """
   Ejecuta una función de consulta y captura todo lo que imprime por consola.

   Esto permite reutilizar funciones diseñadas para terminal dentro de
   Streamlit, mostrando su resultado en la consola de salida de la interfaz.
   """
    f = io.StringIO()

    with redirect_stdout(f):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Error en la ejecución web: {e}")

    valor_final = f.getvalue()

    if not valor_final:
        valor_final ="La consulta se ejecutó pero no devolvió texto de salida."

    return valor_final

# =========================================================
# VALIDACIÓN Y CONVERSIÓN DE DATOS
# =========================================================

def validar_y_tipar_datos(inputs_crudos):
    """
    Recibe los valores ingresados desde la interfaz y construye un documento
    válido para MongoDB.

    La función:
    - descarta campos vacíos;
    - convierte campos numéricos al tipo correspondiente;
    - acumula errores de validación para mostrarlos en pantalla.

    Retorna:
    - doc_limpio: diccionario con los datos listos para insertar o actualizar;
    - errores: lista de mensajes de error detectados.
    """
    doc_limpio = {}
    errores = []

    # Campos almacenados como texto en MongoDB.
    campos_texto = ["horse_id", "horse_name", "race_id", "jockey", "trainer", "father", "mother", "gfather", "finish_time"]
    for campo in campos_texto:
        if inputs_crudos.get(campo):
            doc_limpio[campo] = inputs_crudos[campo]

    # Campos almacenados como enteros.
    campos_enteros = ["horse_number", "actual_weight", "declared_horse_weight", "draw", "finishing_position", "running_position_1", "running_position_2", "running_position_3"]
    for campo in campos_enteros:
        valor = inputs_crudos.get(campo)
        if valor:
            try:
                doc_limpio[campo] = int(valor)
            except ValueError:
                errores.append(f"El campo '{campo}' debe ser un número entero sin letras.")

    # Campo decimal correspondiente al tiempo final expresado en segundos.
    valor_tiempo = inputs_crudos.get("finish_time_seconds")
    if valor_tiempo:
        try:
            doc_limpio["finish_time_seconds"] = float(valor_tiempo.replace(',', '.'))
        except ValueError:
            errores.append("El campo 'finish_time_seconds' debe ser un número válido.")
            
    return doc_limpio, errores

# =========================================================
# VISTA PRINCIPAL DE MONGODB
# =========================================================
def mostrar_mongo(collection):
    """
    Renderiza la pestaña de MongoDB dentro del dashboard.

    Recibe como parámetro la colección principal de MongoDB y permite:
    - insertar documentos;
    - actualizar documentos existentes;
    - borrar documentos;
    - ejecutar consultas simples, complejas e historial por nombre.
    """
    st.header("Consultas Documentales - MongoDB")

    # Validación inicial de conexión.
    if collection is None:
        st.error("No se pudo conectar a la colección de MongoDB.")
        return

    # Variables generales de estado para la vista.
    mensaje_crud = None
    tipo_mensaje = None
    ejecutar_consulta = False
    output_resultado = ""
    opcion = None
    categoria2 = None
    nombre_caballo = ""
    errores_validacion = []

    # Distribución principal:columna izquierda para controles, columna derecha para salida.
    col1, col2 = st.columns([1, 1.8])

    # =========================================================
    # PANEL IZQUIERDO - CONTROLES
    # =========================================================
    with col1:
        with st.container(border=True):
            st.markdown("### Panel de Control")
            
            modo_operacion = st.radio("Modo de Operación", ["Modificar Datos", "Consultas/Simulación"], horizontal=True,key="modo_operacion_mongo")

            # =====================================================
            # CRUD SOBRE DOCUMENTOS
            # =====================================================
            if modo_operacion == "Modificar Datos":
                categoria1 = st.radio("Operación CRUD", ["Inserción", "Actualización", "Borrado"],key="crud_mongo")

                # -------------------------------------------------
                # INSERCIÓN DE DOCUMENTOS
                # -------------------------------------------------
                if categoria1 == "Inserción":
                    with st.form("form_insercion"):
                        st.markdown("**Inserción de registro en MongoDB**")

                        # Datos mínimos necesarios para identificar un registro.
                        horse_id = st.text_input("ID Caballo (Obligatorio):",key="insert_horse_id_mongo").upper().strip()
                        race_id = st.text_input("ID Carrera (Obligatorio):",key="insert_race_id_mongo").upper().strip()
                        horse_name = st.text_input("Nombre Caballo (Obligatorio):",key="insert_horse_name_mongo").upper().strip()
                        jockey = st.text_input("Jockey:",key="insert_jockey_mongo").strip()
                        trainer = st.text_input("Entrenador:",key="insert_trainer_mongo").strip()

                        # Campos opcionales provenientes del dataset original.
                        with st.expander("Ver campos técnicos opcionales (Tiempos, Posiciones, etc.)"):
                            colA, colB = st.columns(2)
                            with colA:
                                horse_number = st.text_input("N° Caballo (Int):",key="insert_horse_number_mongo").strip()
                                father = st.text_input("Padre:",key="insert_father_mongo").strip()
                                mother = st.text_input("Madre:",key="insert_mother_mongo").strip()
                                gfather = st.text_input("Abuelo:",key="insert_gfather_mongo").strip()
                                actual_weight = st.text_input("Peso Actual (Int):",key="insert_actual_weight_mongo").strip()
                                declared_weight = st.text_input("Peso Declarado (Int):",key="insert_declared_weight_mongo").strip()

                            with colB:
                                draw = st.text_input("Sorteo (Int):",key="insert_draw_mongo").strip()
                                finish_pos = st.text_input("Pos. Final (Int):",key="insert_finish_pos_mongo").strip()
                                run_pos_1 = st.text_input("Pos. C1 (Int):",key="insert_run_pos_1_mongo").strip()
                                run_pos_2 = st.text_input("Pos. C2 (Int):",key="insert_run_pos_2_mongo").strip()
                                run_pos_3 = st.text_input("Pos. C3 (Int):",key="insert_run_pos_3_mongo").strip()
                                finish_time = st.text_input("Tiempo (String, ej: 1.09.98):",key="insert_finish_time_mongo").strip()
                                finish_time_sec = st.text_input("Tiempo en Seg (Numérico):",key="insert_finish_time_sec_mongo").strip()
                        
                        btn_insertar = st.form_submit_button("Insertar Documento", type="primary", use_container_width=True)
                        
                        if btn_insertar:
                            # Validación de campos obligatorios.
                            if not horse_id or not race_id or not horse_name:
                                mensaje_crud = "Error: No podés insertar el registro. El 'ID Caballo', 'ID Carrera' y 'Nombre' son obligatorios."
                                tipo_mensaje = "error"
                            else:
                                inputs_crudos = {
                                    "horse_id": horse_id, "horse_name": horse_name, "horse_number": horse_number,
                                    "race_id": race_id, "jockey": jockey, "trainer": trainer, 
                                    "father": father, "mother": mother, "gfather": gfather,
                                    "actual_weight": actual_weight, "declared_horse_weight": declared_weight,
                                    "draw": draw, "finishing_position": finish_pos,
                                    "running_position_1": run_pos_1, "running_position_2": run_pos_2,
                                    "running_position_3": run_pos_3, "finish_time": finish_time,
                                    "finish_time_seconds": finish_time_sec
                                }
                                
                                nuevo_doc, errores_validacion = validar_y_tipar_datos(inputs_crudos)
                                
                                if errores_validacion:
                                    tipo_mensaje = "errores_multiples"
                                elif nuevo_doc:
                                    # Se evita duplicar un caballo dentro de la misma carrera.
                                    existe = buscar_caballo_por_id_y_carrera(collection, horse_id, race_id)
                                    if existe:
                                        mensaje_crud = f"El caballo {horse_id} ya está registrado en la carrera {race_id}."
                                        tipo_mensaje = "error"
                                    else:
                                        insertar_caballo(collection, nuevo_doc)
                                        mensaje_crud = f"Se insertó el documento exitosamente con {len(nuevo_doc)} campos válidos."
                                        tipo_mensaje = "success"
                                else:
                                    mensaje_crud = "Error inesperado al procesar los datos."
                                    tipo_mensaje = "warning"

                # -------------------------------------------------
                # ACTUALIZACIÓN DE DOCUMENTOS
                # -------------------------------------------------
                elif categoria1 == "Actualización":
                    with st.form("form_actualizacion"):
                        st.markdown("**1. Buscar Registro Exacto:**")

                        colBusqA, colBusqB = st.columns(2)
                        with colBusqA:
                            horse_id_busqueda = st.text_input("ID Caballo (Obligatorio):",key="update_horse_id_busqueda_mongo").upper().strip()
                        with colBusqB:
                            race_id_busqueda = st.text_input("ID Carrera (Obligatorio):",key="update_race_id_busqueda_mongo").upper().strip()

                        st.markdown("**2. Nuevos Datos (dejá en blanco lo que no quieras cambiar):**")
                        
                        upd_name = st.text_input("Nuevo Nombre:",key="update_name_mongo").upper().strip()
                        upd_jockey = st.text_input("Nuevo Jockey:",key="update_jockey_mongo").strip()
                        
                        with st.expander("Ver campos técnicos a modificar"):
                            colA, colB = st.columns(2)
                            with colA:
                                upd_number = st.text_input("Nuevo N° Caballo (Int):",key="update_number_mongo").strip()
                                upd_trainer = st.text_input("Nuevo Entrenador:",key="update_trainer_mongo").strip()
                                upd_father = st.text_input("Nuevo Padre:",key="update_father_mongo").strip()
                                upd_mother = st.text_input("Nueva Madre:",key="update_mother_mongo").strip()
                                upd_gfather = st.text_input("Nuevo Abuelo:",key="update_gfather_mongo").strip()
                                upd_actual_weight = st.text_input("Nuevo Peso Actual (Int):", key="update_actual_weight_mongo").strip()
                            with colB:
                                upd_declared_weight = st.text_input("Nuevo Peso Dec (Int):",key="update_declared_weight_mongo").strip()
                                upd_draw = st.text_input("Nuevo Sorteo (Int):",key="update_draw_mongo").strip()
                                upd_finish_pos = st.text_input("Nueva Pos. Final (Int):",key="update_finish_pos_mongo").strip()
                                upd_run_pos_1 = st.text_input("Nueva Pos. C1 (Int):",key="update_run_pos_1_mongo").strip()
                                upd_run_pos_2 = st.text_input("Nueva Pos. C2 (Int):",key="update_run_pos_2_mongo").strip()
                                upd_run_pos_3 = st.text_input("Nueva Pos. C3 (Int):",key="update_run_pos_3_mongo").strip()
                                upd_time = st.text_input("Nuevo Tiempo (String):", key="update_time_mongo").strip()
                                upd_time_sec = st.text_input("Nuevo Tiempo Seg (Numérico):",key="update_time_sec_mongo").strip()
                        
                        btn_actualizar = st.form_submit_button("Actualizar Documento", type="primary", use_container_width=True)
                        
                        if btn_actualizar:
                            if not horse_id_busqueda or not race_id_busqueda:
                                mensaje_crud = "Tanto el ID del caballo como el ID de la carrera son obligatorios."
                                tipo_mensaje = "error"
                            else:
                                caballo_existe = buscar_caballo_por_id_y_carrera(collection, horse_id_busqueda, race_id_busqueda)
                                if caballo_existe:
                                    inputs_crudos_upd = {
                                        "horse_name": upd_name, "horse_number": upd_number, 
                                        "jockey": upd_jockey, "trainer": upd_trainer, "father": upd_father,
                                        "mother": upd_mother, "gfather": upd_gfather, "actual_weight": upd_actual_weight,
                                        "declared_horse_weight": upd_declared_weight, "draw": upd_draw,
                                        "finishing_position": upd_finish_pos, "running_position_1": upd_run_pos_1,
                                        "running_position_2": upd_run_pos_2, "running_position_3": upd_run_pos_3,
                                        "finish_time": upd_time, "finish_time_seconds": upd_time_sec
                                    }
                                    
                                    campos_a_actualizar, errores_validacion = validar_y_tipar_datos(inputs_crudos_upd)
                                    
                                    if errores_validacion:
                                        tipo_mensaje = "errores_multiples"

                                    elif campos_a_actualizar:
                                        actualizar_caballo(collection, horse_id_busqueda, race_id_busqueda, campos_a_actualizar)
                                        mensaje_crud = f"Se actualizaron {len(campos_a_actualizar)} campos para el caballo {horse_id_busqueda} en la carrera {race_id_busqueda}."
                                        tipo_mensaje = "success"

                                    else:
                                        mensaje_crud = "El registro existe, pero no ingresaste ningún dato nuevo para actualizar."
                                        tipo_mensaje = "warning"

                                else:
                                    mensaje_crud = f"No se encontró al caballo {horse_id_busqueda} participando en la carrera {race_id_busqueda}."
                                    tipo_mensaje = "error"

                # -------------------------------------------------
                # BORRADO DE DOCUMENTOS
                # -------------------------------------------------
                elif categoria1 == "Borrado":
                    tipo_borrado = st.radio("Opciones de Eliminación:",
                                            ["Eliminar caballo de una carrera especifica",
                                             "Eliminar caballo de todas las carreras"]
                                            )
                    
                    with st.form("form_borrado"):
                        if tipo_borrado == "Eliminar caballo de una carrera especifica":
                            st.markdown("**Eliminar registro exacto**")

                            colBusqA, colBusqB = st.columns(2)
                            with colBusqA:
                                horse_id_borrar = st.text_input("ID Caballo (Obligatorio):",key="delete_horse_id_mongo").upper().strip()
                            with colBusqB:
                                race_id_borrar = st.text_input("ID Carrera (Obligatorio):",key="delete_race_id_mongo").upper().strip()
                        else:
                            st.markdown("**Eliminar historial completo**")
                            st.warning("Esto eliminará todas las carreras registradas de este caballo en la base de datos.")

                            horse_id_borrar = st.text_input("ID Caballo (Obligatorio):",key="delete_all_horse_id_mongo").upper().strip()
                            race_id_borrar = None
                            
                        btn_borrar = st.form_submit_button("Ejecutar Eliminación", type="primary", use_container_width=True)
                        
                        if btn_borrar:
                            if tipo_borrado == "Eliminar caballo de una carrera especifica":
                                if horse_id_borrar and race_id_borrar:
                                    resultado = borrar_caballo_carrera_especifica(collection, horse_id_borrar, race_id_borrar)

                                    if resultado.deleted_count > 0:
                                        mensaje_crud = f"Se eliminó correctamente el registro del caballo {horse_id_borrar} en la carrera {race_id_borrar}."
                                        tipo_mensaje = "success"
                                    else:
                                        mensaje_crud = f"No se encontró al caballo {horse_id_borrar} participando en la carrera {race_id_borrar}."
                                        tipo_mensaje = "error"
                                else:
                                    mensaje_crud = "Ambos IDs (Caballo y Carrera) son obligatorios."
                                    tipo_mensaje = "warning"

                            else:
                                if horse_id_borrar:
                                    resultado = borrar_caballo_todas_carreras(collection, horse_id_borrar)
                                    if resultado.deleted_count > 0:
                                        mensaje_crud = f"Se eliminaron {resultado.deleted_count} registros totales del caballo {horse_id_borrar}."
                                        tipo_mensaje = "success"
                                    else:
                                        mensaje_crud = f"No se encontró ningún registro del caballo con ID {horse_id_borrar}."
                                        tipo_mensaje = "error"
                                else:
                                    mensaje_crud = "El ID del Caballo es obligatorio."
                                    tipo_mensaje = "warning"

            # =====================================================
            # CONSULTAS Y SIMULACIÓN
            # =====================================================
            elif modo_operacion == "Consultas/Simulación":
                categoria2 = st.radio("Tipo de consulta", ["Simples", "Complejas", "Historial por Nombre"],key="tipo_consulta_mongo")
                
                if categoria2 == "Simples":
                    opcion = st.selectbox("Seleccione la consulta simple:",
                  [
                        "1. Obtener todos los caballos entrenados por P F YIU",
                        "2. Todos los caballos que ganaron alguna carrera",
                        "3. Caballos que pesan menos de 1000 libras",
                        "4. Cantidad de carreras que se corrieron",
                        "5. Caballos con tiempos menores a 1.23.00"
                    ],
                    key="select_simple_mongo"
                )

                    ejecutar_consulta = st.button("Ejecutar Consulta Simple", use_container_width=True, type="primary",key="btn_simple_mongo")
                
                elif categoria2 == "Complejas":
                    opcion = st.selectbox("Seleccione la consulta compleja:",
                        [
                        "1. Tiempo promedio de todos los caballos",
                        "2. Tiempo promedio de carrera de los caballos entrenados por P F YIU",
                        "3. Caballos con número 10 y tiempo menor a 1.22.70",
                        "4. Listar todos los caballos cuyo nombre comience con A",
                        "5. TOP 10 de tiempos más rápidos"
                        ],
                      key="select_compleja_mongo"
                        )
                    ejecutar_consulta = st.button("Ejecutar Consulta Compleja", use_container_width=True, type="primary", key="btn_compleja_mongo")
                    
                elif categoria2 == "Historial por Nombre":
                    st.info("Esta consulta requiere un parámetro de búsqueda.")
                    nombre_caballo = st.text_input("Ingresar nombre del caballo:", value="",key="historial_nombre_mongo").upper().strip()
                    ejecutar_consulta = st.button("Buscar Historial", use_container_width=True, type="primary",key="btn_historial_mongo")

    # =========================================================
    # PANEL DERECHO - SALIDA
    # =========================================================
    with col2:
        st.subheader("Consola de Salida")

        # Mensajes generados por operaciones CRUD.
        if tipo_mensaje == "errores_multiples":
            st.error("Se encontraron errores de validación de datos. Corregilos para continuar:")

            for error in errores_validacion:
                st.warning(f"{error}")

        elif mensaje_crud:
            if tipo_mensaje == "success": st.success(mensaje_crud)
            elif tipo_mensaje == "error": st.error(mensaje_crud)
            elif tipo_mensaje == "warning": st.warning(mensaje_crud)

        # Ejecución de consultas seleccionadas desde el panel izquierdo.
        if ejecutar_consulta:
            with st.spinner('Buscando en MongoDB...'):
                if modo_operacion == "Consultas/Simulación":

                    if categoria2 == "Simples" and opcion:
                        if opcion.startswith("1."): output_resultado = ejecutar_consulta_y_capturar_output(caballosEntrenadosP_F_YIU, collection)
                        elif opcion.startswith("2."): output_resultado = ejecutar_consulta_y_capturar_output(caballosGanadores, collection)
                        elif opcion.startswith("3."): output_resultado = ejecutar_consulta_y_capturar_output(caballosMenoresDeMil, collection)
                        elif opcion.startswith("4."): output_resultado = ejecutar_consulta_y_capturar_output(cantCarreras, collection)
                        elif opcion.startswith("5."): output_resultado = ejecutar_consulta_y_capturar_output(caballosVeloces, collection)

                    elif categoria2 == "Complejas" and opcion:
                        if opcion.startswith("1."): output_resultado = ejecutar_consulta_y_capturar_output(promedio_tiempo_todos, collection)
                        elif opcion.startswith("2."): output_resultado = ejecutar_consulta_y_capturar_output(promedio_tiempo_entrenador, collection)
                        elif opcion.startswith("3."): output_resultado = ejecutar_consulta_y_capturar_output(caballos_diez_tiempo, collection)
                        elif opcion.startswith("4."): output_resultado = ejecutar_consulta_y_capturar_output(caballosConA, collection)
                        elif opcion.startswith("5."): output_resultado = ejecutar_consulta_y_capturar_output(top_10_tiempos, collection)


                    elif categoria2 == "Historial por Nombre":
                        if not nombre_caballo:
                            st.warning("Por favor, ingrese un nombre válido.")
                        else:
                            # La función original pide input() por consola.
                            # Se reemplaza temporalmente para integrarla con Streamlit.
                            input_original = builtins.input
                            try:
                                builtins.input = lambda *args: nombre_caballo
                                output_resultado = ejecutar_consulta_y_capturar_output(buscarHistorialCaballo, collection)
                            finally:
                                builtins.input = input_original

        # =====================================================
        # RENDERIZADO DEL RESULTADO
        # =====================================================
        if output_resultado:
            if modo_operacion == "Consultas/Simulación" and categoria2 == "Historial por Nombre":
                consulta_limpia = f"historial_{nombre_caballo.replace(' ', '_').lower()}"
            else:
                consulta_limpia = opcion.split(". ", 1)[-1].replace(" ", "_").lower()
            
            st.download_button(
                label="Descargar datos (TXT)",
                data=output_resultado,
                file_name=f"resultado_{consulta_limpia}_mongo.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.code(output_resultado, language="text")
        elif not mensaje_crud and tipo_mensaje != "errores_multiples":
            st.info("Seleccione una operación del panel izquierdo para visualizar los datos aquí.")