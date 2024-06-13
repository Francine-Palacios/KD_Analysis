import streamlit as st
import plotly.express as px

def grafico_3d(df_data, seleccionar_rango=True, etiqueta='', max=False):
    range_color_max=df_data['CU%'].max()
    if max:
       range_color_max=1.83  #Maximo del Data set original.
    if seleccionar_rango:
      z_min, z_max = st.slider('Selecciona el rango de profundidad (eje z):' + etiqueta, 
                              min_value=int(df_data['z'].min()), 
                              max_value=int(df_data['z'].max()), 
                              value=(int(df_data['z'].min()), int(df_data['z'].max())))
    else:
       z_min=df_data['z'].min()
       z_max=df_data['z'].max()
    df_filtered = df_data[(df_data['z'] >= z_min) & (df_data['z'] <= z_max)]

    fig = px.scatter_3d(df_filtered, x='x', y='y', z='z',
                        color='CU%',
                        color_continuous_scale='Viridis',  
                        range_color=[0, range_color_max])

    fig.update_layout(scene=dict(
                        xaxis_title='Eje X',
                        yaxis_title='Eje Y',
                        zaxis_title='Eje Z'),
                      coloraxis_colorbar=dict(title='Porcentaje de Cobre (CU%)'))

    st.plotly_chart(fig, use_container_width= True )
    return None