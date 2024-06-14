
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def Analisis_descriptivo(df_data):
    st.header("Analisis de datos")

    ##################################################################################################
    ################################### Datos ########################################################
    ##################################################################################################

    st.subheader('Datos')
    st.write("Se elimino la columa 'id' ya que no aporta nueva información, solo es el numero de fila.")
    st.dataframe(df_data,use_container_width= True)

    ##################################################################################################
    ##################################################################################################
    ##################################################################################################


    ##################################################################################################
    ############## Tabla con alguans estadisticas de utilidad ########################################
    ##################################################################################################

    st.header('Estadisticas de utilidad')
    st.table(df_data.describe())

    #########################################################################
    #########################################################################
    #########################################################################

    #####################################################################################
    ############## Grafico de Histograma ################################################
    #####################################################################################
    
    st.subheader("Histograma de los datos")

    feature_names = df_data.select_dtypes(include=['number']).columns

    fig = make_subplots(rows=2, cols=4, subplot_titles=feature_names)

    for index, name in enumerate(feature_names):
        row = index // 4 + 1
        col = index % 4 + 1
        fig.add_trace(
            go.Histogram(
                x=df_data[name], 
                name=name,
                marker=dict(
                    line=dict(
                        color='black',  
                        width=1         
                    )
                ),
            ),
            row=row, col=col
        )

    fig.update_layout(height=600, width=800, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)


    #####################################################################################
    #####################################################################################
    #####################################################################################


    #####################################################################################
    ########## Grafico de Histograma, diferenciando entre la variable objetivo ##########
    #####################################################################################

    st.subheader("Histograma diferenciado por 'Porcentaje de Cobre'")
    Chance= st.slider("Porcentaje de Cobre", min_value=0.1,max_value=2.0,value=0.5, step=0.1)

    df_aux=df_data.copy()
    df_aux['Admit CU%'] = df_aux['CU%'].apply(lambda x: f'Chance > {Chance}' if x > Chance else f'Chance <= {Chance}')


    feature_names = df_aux.select_dtypes(include=['number']).columns

    fig = make_subplots(rows=2, cols=4, subplot_titles=feature_names)

    for index, name in enumerate(feature_names):
        row = index // 4 + 1
        col = index % 4 + 1
        fig.add_trace(
            go.Histogram(x=df_aux[df_aux['Admit CU%'] == f'Chance > {Chance}'][name], 
                        name=f'Chance > {Chance}', 
                        marker=dict(color='blue', line=dict(color='black', width=1)),
                        opacity=0.6),  
            row=row, col=col
        )
        fig.add_trace(
            go.Histogram(x=df_aux[df_aux['Admit CU%'] == f'Chance <= {Chance}'][name], 
                        name=f'Chance <= {Chance}', 
                        marker=dict(color='red', line=dict(color='black', width=1)),
                        opacity=0.6),  
            row=row, col=col
        )

    fig.update_layout(barmode='overlay', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


    #####################################################################################
    #####################################################################################
    #####################################################################################

    #####################################################################################
    ############################## Boxplot ##############################################
    #####################################################################################
   
    st.subheader("Boxplot")

    columnas_numericas = df_data.select_dtypes(include=['number']).columns

    fig = make_subplots(rows=2, cols=4, subplot_titles=columnas_numericas)

    for index, columna in enumerate(columnas_numericas):
        row = index // 4 + 1
        col = index % 4 + 1
        fig.add_trace(
            go.Box(y=df_data[columna], name=columna),
            row=row, col=col
        )

    fig.update_layout(height=600, width=800, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    #####################################################################################
    #####################################################################################
    #####################################################################################



    return None