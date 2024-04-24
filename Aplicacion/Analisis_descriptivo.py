
import streamlit as st

import plotly.express as px


def Analisis_descriptivo(df_data):
    
    st.header('Datos')
    st.write("Se elimino la columa 'id' ya que no aporta nueva información, solo es el numero de fila.")
    st.dataframe(df_data)
    ##################################################################################################
    ############## Tabla con alguans estadisticas de utilidad ################################################
    ##################################################################################################

    st.header('Estadisticas de utilidad')
    st.table(df_data.describe())

    #########################################################################
    #########################################################################
    #########################################################################

    #########################################################################
    ############## Graficos #################################################
    #########################################################################
    st.sidebar.subheader("Plot de datos")
    with st.sidebar.expander('Parametros para el Histograma'):
        st.markdown("Para los graficos de histograma, seleccione las columnas de interes")
        if st.checkbox("Todas las columnas"):
            feature_names = df_data.columns 
            pass
        else:
            columnas=st.multiselect('Seleccione las columnas que le interesan para los graficos ', df_data.columns)
            feature_names=columnas

        Chance= st.slider("¿Cuanto considera que se acepta en 'CU%'?", min_value=0.1,max_value=1.0,value=0.5, step=0.1)

    ############ Grafico de Histograma ############
    st.subheader("Histogramas")
    if feature_names== []:
        st.warning('Seleccione parametros en la parte izquierda de su pantalla')
   
    for name in feature_names:
        fig = px.histogram(df_data, x=name, marginal="rug", color_discrete_sequence=['indianred'])
        st.plotly_chart(fig, use_container_width=True)


    ########## Grafico de Histograma, diferenciando entre la variable objetivo #####
    st.subheader("Histograma diferenciado la variable objetivo")
    if feature_names== []:
        st.warning('Seleccione parametros en la parte izquierda de su pantalla')
    df_aux = df_data.copy()

    df_aux['Admit CU%'] = df_aux['CU%'].apply(lambda x: f'Chance > {Chance}' if x > Chance else f'Chance <= {Chance}')

    # feature_names = ['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR ', 'CGPA', 'Research', 'Chance of Admit ']

    for name in feature_names:
        fig = px.histogram(df_aux, x=name, color='Admit CU%', barmode='overlay',
                          color_discrete_map={f'Chance > {Chance}': 'blue', f'Chance <= {Chance}': 'red'})
        st.plotly_chart(fig, use_container_width=True)




    ######## Boxplot ###########
    st.subheader('Boxplot')
    with st.sidebar.expander('Parametros para el Boxplot'):
        st.markdown("Para los graficos de Boxplot, seleccione las columnas de interes")
        if st.checkbox("Todas"):
            feature_names = df_data.columns
            pass
        else:
            columnas=st.multiselect('Seleccione las columnas que le interesan para el boxplot ', df_data.columns)
            feature_names=columnas

    if feature_names == []:
        st.warning('Seleccione parametros en la parte izquierda de su pantalla')
    # feature_names = ['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR ', 'CGPA', 'Research', 'Chance of Admit ']

    for name in feature_names:
        fig = px.box(df_data, y=name, color_discrete_sequence=['goldenrod'])
        fig.update_layout(title=name, yaxis_title="Valor")
        st.plotly_chart(fig, use_container_width=True)





    return None