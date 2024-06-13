import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st


def aplicar_filtros(df, umbral, filtrar_cu, z_min, z_max):
    df_filtrado = df.copy()
    df_filtrado.loc[df_filtrado['CU%'] < umbral, 'CU%'] = 0
    if filtrar_cu:
        df_filtrado = df_filtrado[df_filtrado['CU%'] != 0]
    df_filtrado = df_filtrado[(df_filtrado['z'] >= z_min) & (df_filtrado['z'] <= z_max)]
    df_filtrado = df_filtrado.dropna()  
    return df_filtrado



def combinar_datos(pred_simple, df_data):
    pred_simple_copy = pred_simple.copy()
    df_data_copy = df_data.copy()

    pred_simple_copy['coord'] = list(zip(pred_simple_copy['x'], pred_simple_copy['y'], pred_simple_copy['z']))
    df_data_copy['coord'] = list(zip(df_data_copy['x'], df_data_copy['y'], df_data_copy['z']))
    
    coords_comunes = set(pred_simple_copy['coord']).intersection(set(df_data_copy['coord']))
    
    pred_simple_filtrado = pred_simple_copy[~pred_simple_copy['coord'].isin(coords_comunes)].copy()
    
    pred_simple_filtrado['origen'] = 'predicho'
    df_data_copy['origen'] = 'real'
    
    df_combinado = pd.concat([pred_simple_filtrado, df_data_copy], ignore_index=True)
    
    df_combinado = df_combinado.drop(columns=['coord'])
    
    return df_combinado





def grafico_3d_combinado(df_combinado, seleccionar_rango=True, etiqueta='', max=False):
    range_color_max = df_combinado['CU%'].max()
    if max:
       range_color_max = 1.83  
    if seleccionar_rango:
        z_min, z_max = st.slider('Selecciona el rango de profundidad (eje z):' + etiqueta, 
                                min_value=int(df_combinado['z'].min()), 
                                max_value=int(df_combinado['z'].max()), 
                                value=(int(df_combinado['z'].min()), int(df_combinado['z'].max())))
    else:
        z_min = df_combinado['z'].min()
        z_max = df_combinado['z'].max()
        
    df_filtered = df_combinado[(df_combinado['z'] >= z_min) & (df_combinado['z'] <= z_max)]

    
    df_real = df_filtered[df_filtered['origen'] == 'real']
    df_predicho = df_filtered[df_filtered['origen'] == 'predicho']

    
    fig = go.Figure()

   
    fig.add_trace(go.Scatter3d(
        x=df_predicho['x'], y=df_predicho['y'], z=df_predicho['z'],
        mode='markers',
        marker=dict(
            size=5,
            color=df_predicho['CU%'],
            colorscale='Viridis',
            cmin=0,
            cmax=range_color_max,
            colorbar=dict(title='Porcentaje de Cobre (CU%)'),
            line=dict(color='rgba(0,0,0,0)')  
        ),
        name='Predicho'
    ))

    fig.add_trace(go.Scatter3d(
        x=df_real['x'], y=df_real['y'], z=df_real['z'],
        mode='markers',
        marker=dict(
            size=5,
            color=df_real['CU%'],
            colorscale='Viridis',
            cmin=0,
            cmax=range_color_max,
            colorbar=dict(title='Porcentaje de Cobre (CU%)'),
            line=dict(color='black', width=2)  
        ),
        name='Real'
    ))

  
    fig.update_layout(scene=dict(
                        xaxis_title='Eje X',
                        yaxis_title='Eje Y',
                        zaxis_title='Eje Z'),
                      margin=dict(l=0, r=0, b=0, t=0))

    st.plotly_chart(fig, use_container_width=True)

    return None



def grafico_linea(df_simple, df_ordinario, df_universal, max_index):
    fig = go.Figure()

    # Agregar la línea para pred_simple
    fig.add_trace(go.Scatter(
        x=df_simple.index[:max_index], y=df_simple['CU%'][:max_index],
        mode='lines+markers',  # Conectar los puntos con líneas y mostrar los marcadores
        name='Kriging Simple',
        line=dict(color='blue'),
        marker=dict(size=6)
    ))

    # Agregar la línea para pred_ordinario
    fig.add_trace(go.Scatter(
        x=df_ordinario.index[:max_index], y=df_ordinario['CU%'][:max_index],
        mode='lines+markers',  # Conectar los puntos con líneas y mostrar los marcadores
        name='Kriging Ordinario',
        line=dict(color='green'),
        marker=dict(size=6)
    ))

    # Agregar la línea para pred_universal
    fig.add_trace(go.Scatter(
        x=df_universal.index[:max_index], y=df_universal['CU%'][:max_index],
        mode='lines+markers',  # Conectar los puntos con líneas y mostrar los marcadores
        name='Kriging Universal',
        line=dict(color='red'),
        marker=dict(size=6)
    ))

    # Configurar la disposición de la gráfica
    fig.update_layout(title='Comparación de CU% entre diferentes métodos de Kriging',
                      xaxis_title='Índice',
                      yaxis_title='Porcentaje de Cobre (CU%)',
                      margin=dict(l=0, r=0, b=0, t=40))

    st.plotly_chart(fig, use_container_width=True)

    return None