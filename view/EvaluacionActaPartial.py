import os

from model.InfoActa import InfoActa
from datetime import datetime
from controller.ControladorPDF import ControladorPdf
from datetime import date #punto 3
# Este archivo contiene las funcionalidades de la vista relacionado con la evaluación de las actas


def agregar_acta(st, controlador):
    st.title("Generación De Actas")
    col1, col2, col3 = st.columns(3)
    col5, col6, col7, col8, col9= st.columns(5) #punto 3
    # Objeto que modelará el formulario
    info_acta_obj = InfoActa(controlador.criterios)
    info_acta_obj.fecha_acta = datetime.today().strftime('%Y-%m-%d')
    with col1:
        info_acta_obj.autor = st.text_input("Autor")
    with col2:
        info_acta_obj.nombre_trabajo = st.text_input("Nombre De Trabajo")
    with col3:
        info_acta_obj.tipo_trabajo = st.selectbox('Tipo', ('Aplicado', 'Investigación'))



    with col5: #punto 5
        info_acta_obj.director = st.selectbox("Escoja un director", (controlador.retornarListaDirectores()[0],controlador.retornarListaDirectores()[1],controlador.retornarListaDirectores()[2],controlador.retornarListaDirectores()[3],controlador.retornarListaDirectores()[4],controlador.retornarListaDirectores()[5],controlador.retornarListaDirectores()[6],controlador.retornarListaDirectores()[7],controlador.retornarListaDirectores()[8]))
    with col6:
        info_acta_obj.codirector = st.text_input("Codirector", "N.A")

    with col7:
        info_acta_obj.jurado1 = st.text_input("Jurado #1")
        info_acta_obj.jurado1Escoger == st.checkbox('Interno', key = "interno1") #punto6
        info_acta_obj.jurado1Escoger == st.checkbox('Externo', key = "Externo1")


    with col8:
        info_acta_obj.jurado2 = st.text_input("Jurado #2")
        info_acta_obj.jurado2Escoger = st.checkbox('Interno')#punto6
        info_acta_obj.jurado2Escoger = st.checkbox('Externo')



    with col9: #punto 3
        info_acta_obj.fecha_presentacion = st.date_input("Fecha presentacion", date(2022, 11, 6))
    enviado_btn = st.button("Enviar")

    # Cuando se oprime el botón se agrega a la lista
    if enviado_btn and info_acta_obj.autor != "" and info_acta_obj.nombre_trabajo != "" and info_acta_obj.director != "" \
            and info_acta_obj.jurado1 != "" and info_acta_obj.jurado2 != "":
        controlador.agregar_evaluacion(info_acta_obj)
        st.success("Acta Agregada Exitosamente.")

    elif enviado_btn:
        st.error("Llene Todos Los Campos Vacíos.")
    else:
        st.info("No Deje Ningún Espacio En Blanco En Los Datos")
    # Retorna el controlador pq solo las colecciones se pasan en python por referencia,
    # entonces de esta manera se actualiza el controlador en la vista principal

    return controlador


def ver_historico_acta(st, controlador):
    st.title("Histórico")
    numero = 1
    if [acta.autor for acta in controlador.actas]:
        st.write("Estudiantes registrados en el sistema:")
    else:
        st.warning("Ningún Estudiante Registrado Aún.")
    for acta in controlador.actas:
        st.write("#### Acta #", numero)
        numero += 1
        col1, col2, col3, col4 = st.columns(4)
        col5, col6, col7, col8 = st.columns(4)
        col9, col10, col11 = st.columns(3)
        with col1:
            st.write("**Autor**")
            st.write(acta.autor)
        with col2:
            st.write("**Nombre De Trabajo**")
            st.write(acta.nombre_trabajo)
        with col3:
            st.write("**Tipo De Trabajo**")
            st.write(acta.tipo_trabajo)
        with col4:
            st.write("**Fecha De Creación**")
            st.write(acta.fecha_acta)

        with col11: #punto 3
            st.write("**Fecha De presentación**")
            st.write(acta.fecha_presentacion)

        with col5:
            st.write("**Director**")
            st.write(acta.director)
        with col6:
            st.write("**Codirector**")
            st.write(acta.codirector)
        with col7:
            st.write("**Jurado #1**")
            st.write(acta.jurado1)
        with col8:
            st.write("**Jurado #2**")
            st.write(acta.jurado2)
        with col9:
            st.write("**Nota Final**")
            if not acta.estado:
                st.write("Sin nota")
            elif acta.nota_final > 3.5:
                st.write(acta.nota_final, "Acta Aprobada")
            else:
                st.write(acta.nota_final, "Acta Reprobada")
        with col10:
            st.write("**Estado**")
            if not acta.estado:
                st.write("Acta pendiente por calificar")
            else:
                st.write("Acta calificada")


def evaluar_criterios(st, controlador):
    st.title("Evaluación de Criterios")
    flag = False
    num = 1
    temp = 0.0
    opcion = st.selectbox('Elija el autor a calificar', [acta.autor for acta in controlador.actas if not acta.estado])
    st.write("#### Criterios")
    for acta in controlador.actas:
        if acta.autor == opcion:
            flag = True
            for criterio in acta.criterios:
                st.write(criterio.descripcion)
                st.write("Valor de:", criterio.porcentaje * 100, "%")
                nota_jurado1 = st.number_input(str(num) + ". Nota Jurado 1", 0.0, 5.0)
                nota_jurado2 = st.number_input(str(num) + ". Nota Jurado 2", 0.0, 5.0)
                criterio.nota = ((nota_jurado1 + nota_jurado2) / 2) * criterio.porcentaje
                criterio.observacion = st.text_input(str(num) + ". Observación", "Sin Comentarios.")
                criterio.observacionAdicional = st.text_input(str(num) + ". Observación Adicional", "Sin Comentarios.")#punto9
                criterio.restricciones = st.text_input(str(num) + ". Restricciones", "Sin Comentarios.")#punto9
                temp += criterio.nota
                num += 1
            if temp > 3.5:
                st.write("#### Nota Final", temp, "Acta Aprobada.")
            else:
                st.write("#### Nota Final", temp, "Acta Reprobada.")

    if not flag:
        st.warning("Sin Estudiantes Por Calificar.")

    enviado_califica = st.button("Enviar")

    for acta in controlador.actas:
        #Actualiza el model con la informacion
        if acta.autor == opcion and enviado_califica:
            acta.nota_final = temp
            acta.estado = True
    if flag:
        nota_min = 3.5
        if enviado_califica and temp > nota_min:
            st.balloons()
            st.success("Evaluación De acta Agregada exitosamente, acta aprobada.")
        elif enviado_califica and temp <= nota_min:
            st.snow()
            st.success("Evaluación De Acta Agregada Exitosamente, acta reprobada.")
        else:
            st.info("Llene Todos Los Campos Vacíos.")


def ver_estadisticas(st, controlador):
    cantidadProyectosAplicados = 0  # punto 10
    cantidadInvestigaciones = 0  # punto 10
    cantidadJuradosExternos = 0
    cantidadJuradosInternos = 0
    cantidadNotaSuperior = 0



    for acta in controlador.actas:
        if acta.tipo_trabajo == "Aplicado":
            cantidadProyectosAplicados +=1
        else:
            cantidadInvestigaciones +=1


        if acta.jurado1Escoger == 'Interno' or acta.jurado2Escoger == 'Interno':
            cantidadJuradosInternos += 1

        if acta.jurado1Escoger == 'Externo' or acta.jurado2Escoger == 'Externo':
            cantidadJuradosExternos += 1

        if acta.nota_final > 4.8:
            cantidadNotaSuperior +=1



    st.title("Estádisticas generales")

    st.metric("Proyectos Aplicados",value = cantidadProyectosAplicados,
    delta_color="inverse")
    st.metric("Proyectos de Investigacion", value=cantidadInvestigaciones,
              delta_color="inverse")
    st.metric("Cantidad jurados internos", value=cantidadJuradosInternos,
              delta_color="inverse")
    st.metric("Cantidad jurados externos", value=cantidadJuradosExternos,
              delta_color="inverse")
    st.metric("Cantidad de proyectos con nota superior a 4.8", value=cantidadNotaSuperior,
              delta_color="inverse")


def exportar_acta(st, controlador):
    st.title("Generación de PDF")
    nombre_autor = st.selectbox('Elija el autor ya calificado', [acta.autor for acta in controlador.actas if acta.estado])

    if nombre_autor:
        #Fue seleccionado el autor
        enviado_pdf = st.button("Generar PDF")
        if enviado_pdf:
            controlador_pdf = ControladorPdf()
            controlador_pdf.exportar_acta(st,controlador, nombre_autor)
            st.success("Acta generada en PDF exitosamente, consulte la carpeta de salida 'outputs'.")
    else:
        st.info("Seleccione El Estudiante.")

    if len(controlador.actas) == 0:
        st.warning("No Hay Ningún Estudiante Calificado Actualmente.")



