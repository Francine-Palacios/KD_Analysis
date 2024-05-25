import streamlit as st
import plotly.express as px

def grafico_3d(df_data):
    
    z_min, z_max = st.slider('Selecciona el rango de profundidad (eje z):', 
                            min_value=int(df_data['z'].min()), 
                            max_value=int(df_data['z'].max()), 
                            value=(int(df_data['z'].min()), int(df_data['z'].max())))

    df_filtered = df_data[(df_data['z'] >= z_min) & (df_data['z'] <= z_max)]

    fig = px.scatter_3d(df_filtered, x='x', y='y', z='z',
                        color='CU%',
                        color_continuous_scale='Viridis',  
                        range_color=[df_filtered['CU%'].min(), df_filtered['CU%'].max()])

    fig.update_layout(scene=dict(
                        xaxis_title='Eje X',
                        yaxis_title='Eje Y',
                        zaxis_title='Eje Z'),
                      coloraxis_colorbar=dict(title='Porcentaje de Cobre (CU%)'))

    st.plotly_chart(fig, use_container_width= True )
    return None