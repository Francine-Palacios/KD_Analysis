import streamlit as st
import pandas as pd
from informacion import Info
from Analisis_descriptivo import Analisis_descriptivo
from Grafico_3d import grafico_3d

from Procesamiento_data import Consideraciones_data
from Procesamiento_data import tubos
from Procesamiento_data import tubos_eleccion

from funciones_auxiliares import aplicar_filtros
from funciones_auxiliares import combinar_datos
from funciones_auxiliares import grafico_3d_combinado
from funciones_auxiliares import grafico_linea

from info_modelo import contenido_info_modelo
########################################################################
############### Configuracion e informacion ############################
########################################################################


st.set_page_config(page_title='KDA', layout='wide',
                #    initial_sidebar_state=st.session_state.get('sidebar_state', 'collapsed'),
)


_, _, col3 = st.columns([3,6,3])

with col3:
    url_imagen = "https://matematica.usm.cl/wp-content/themes/dmatUSM/assets/img/logoDMAT2.png"

    st.image(url_imagen, width=250)



_, col2, _ = st.columns([1,6,1])

with col2:
    st.title('Análisis descriptivo de Arizona’s Copper Deposit (KD)')

texto_descripcion = """
Esta aplicación fue desarrollada en Python como un visualizador de los resultados del análisis de datos de minería. La producción, predicción y otros procesamientos se llevaron a cabo en un archivo separado utilizando R.
"""


texto_info = """
- Autor: Francine Palacios - Bastian Aceiton
- Ramo: Laboratorio de Modelación
- Institución: Universidad Tecnica Federico Santa Maria
"""
st.snow()



_, exp_col, _ = st.columns([1,3,1])
with exp_col:
    with st.expander(" Información y usos "):
        st.markdown(texto_descripcion)
        st.info(texto_info)
        


InfoTab,Analisis,Grafico, Kriging = st.tabs(["Información","Analisis Descriptivo", 'Grafico', "Kriging"])

        



##################################################################################################
############## Tabla con los datos ############################################
##################################################################################################
path = "https://raw.githubusercontent.com/Francine-Palacios/KD_Analysis/34bb00bfd08595554baa4d6317fd013e4521203d/Datos/kd.blocks.csv"
df_data = pd.read_csv(path, sep=' ', header=None)
column_names = ['id', 'x', 'y', 'z', 'tonn', 'blockvalue', 'destination', 'CU%', 'process_profit']
df_data.columns=column_names
df_data = df_data.drop('id', axis=1)


with InfoTab:
    Info()

with Analisis:
    Analisis_descriptivo(df_data)

with Grafico:
    grafico_3d(df_data)


with Kriging:

    Consideraciones, resultados_grafico, futura_propuesta  = st.tabs(["Consideraciones", "Graficos de las predicciones", "Futura Propuesta"])

    with Consideraciones:
        contenido_info_modelo()
        path2="https://raw.githubusercontent.com/Francine-Palacios/KD_Analysis/main/Resultados/"
        pred_simple= pd.read_csv(path2+"kriging_simple.csv")
        pred_simple = pred_simple.rename(columns={'CU_original':'CU%'})
        pred_ordinario= pd.read_csv(path2+"kriging_ordinario.csv")
        pred_ordinario = pred_ordinario.rename(columns={'CU_original':'CU%'})
        pred_universal= pd.read_csv(path2+"kriging_universal.csv")
        pred_universal = pred_universal.rename(columns={'CU_original':'CU%'})
        max_index_available = min(len(pred_simple), len(pred_ordinario), len(pred_universal))
        max_index = st.slider('Selecciona hasta qué índice visualizar', min_value=1, max_value=max_index_available, value=300)

        grafico_linea(pred_simple, pred_ordinario, pred_universal, max_index)
                
    
    with resultados_grafico:
        
        grafico_simple_predicciones, grafico_simple_predicciones_vs_reales  = st.tabs(["Predicciones", "Predicciones v/s reales"])
        with grafico_simple_predicciones:
            with st.form(key='filtros_form'):
                tipo_kriging = st.selectbox("Selecciona el tipo de Kriging", ["simple", "ordinario", "universal"])
                umbral = st.number_input('Umbral de CU%', min_value=0.0, max_value=100.0, value=0.0, step=0.01)
                filtrar_cu = st.checkbox('Mostrar solo puntos donde CU% es distinto de 0')
                z_range = st.slider('Rango de z', min_value=int(df_data['z'].min()), max_value=int(df_data['z'].max()), value=(int(df_data['z'].min()), int(df_data['z'].max())), step=1)
                submit_button = st.form_submit_button(label='Aplicar filtros')

            if submit_button:
                path2="https://raw.githubusercontent.com/Francine-Palacios/KD_Analysis/main/Resultados/"
                pred_simple= pd.read_csv(f"https://raw.githubusercontent.com/Francine-Palacios/KD_Analysis/main/Resultados/kriging_{tipo_kriging}.csv")
                pred_simple = pred_simple.rename(columns={'CU_original':'CU%'})
                z_min, z_max = z_range
                df_filtrado = aplicar_filtros(pred_simple, umbral, filtrar_cu, z_min, z_max)
                st.write("Datos filtrados:")
                st.dataframe(df_filtrado)
                grafico_3d(df_filtrado, etiqueta= ' Kriging Simple', max=True, seleccionar_rango=False)
        with grafico_simple_predicciones_vs_reales:
            with st.form(key='filtros_form_real_vs_predic'):
                tipo_kriging = st.selectbox("Selecciona el tipo de Kriging", ["simple", "ordinario", "universal"])
                umbral = st.number_input('Umbral para CU%', min_value=0.0, max_value=100.0, value=0.0, step=0.01)
                filtrar_cu = st.checkbox('Mostrar solo puntos donde CU% son distinto de 0')
                z_range = st.slider('Rango de z', min_value=int(pred_simple['z'].min()), max_value=int(pred_simple['z'].max()), value=(int(pred_simple['z'].min()), int(pred_simple['z'].max())), step=1)
                submit_button = st.form_submit_button(label='Aplicar filtros')

            if submit_button:
                path2="https://raw.githubusercontent.com/Francine-Palacios/KD_Analysis/main/Resultados/"
                pred_simple= pd.read_csv(path2 + f"kriging_{tipo_kriging}.csv")
                pred_simple = pred_simple.rename(columns={'CU_original':'CU%'})
                z_min, z_max = z_range
                df_filtrado = aplicar_filtros(pred_simple, umbral, filtrar_cu, z_min, z_max)
                df_data_filtrado = df_data[(df_data['z'] >= z_min) & (df_data['z'] <= z_max)]
                df_combinado = combinar_datos(df_filtrado, df_data_filtrado)
                st.write("Datos combinados:")
                st.dataframe(df_combinado)
                grafico_3d_combinado(df_combinado, seleccionar_rango=False, max=True)
            
    with futura_propuesta:
        Consideraciones_data()
        combined_df, combined_dfm=tubos(df_data, 1000)
        grafico_3d(combined_df, seleccionar_rango=False)
        st.dataframe(combined_df)