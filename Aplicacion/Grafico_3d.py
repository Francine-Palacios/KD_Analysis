import streamlit as st
import plotly.express as px

def grafico_3d(df_data):
    
    # Slider para seleccionar el rango de 'z'
    z_min, z_max = st.slider('Selecciona el rango de profundidad (eje z):', 
                            min_value=int(df_data['z'].min()), 
                            max_value=int(df_data['z'].max()), 
                            value=(int(df_data['z'].min()), int(df_data['z'].max())))

    # Filtrado de datos basado en el rango de 'z'
    df_filtered = df_data[(df_data['z'] >= z_min) & (df_data['z'] <= z_max)]

    # Creación de la figura con Plotly
    fig = px.scatter_3d(df_filtered, x='x', y='y', z='z',
                        color='CU%',
                        color_continuous_scale='Viridis',  # Escala de colores
                        range_color=[df_filtered['CU%'].min(), df_filtered['CU%'].max()])

    # Actualización de los títulos de los ejes
    fig.update_layout(scene=dict(
                        xaxis_title='Eje X',
                        yaxis_title='Eje Y',
                        zaxis_title='Eje Z'),
                      coloraxis_colorbar=dict(title='Porcentaje de Cobre (CU%)'))

    # Mostrar la figura en Streamlit
    st.plotly_chart(fig)
    return None