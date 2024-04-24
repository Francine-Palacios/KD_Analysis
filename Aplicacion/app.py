import streamlit as st
import pandas as pd
from informacion import Info
from Analisis_descriptivo import Analisis_descriptivo
from Grafico_3d import grafico_3d


########################################################################
############### Configuracion e informacion ############################
########################################################################


st.set_page_config(page_title='KDA', layout='wide',
                #    initial_sidebar_state=st.session_state.get('sidebar_state', 'collapsed'),
)
_, _, col3 = st.columns([3,6,3])

with col3:
    st.image("./Departamento_de_matematicas (1).jpg", width=250)

_, col2, _ = st.columns([1,6,1])

with col2:
    st.title('Análisis descriptivo de Arizona’s Copper Deposit (KD)')

texto_descripcion = """
Esta aplicion fue generada para un analisis descripitvo
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
        


InfoTab,Analisis,Grafico = st.tabs(["Información","Analisis Descriptivo", 'Grafico'])

        
st.sidebar.title("Analisis descriptivo de Arizona’s Copper Deposit (KD) ")
st.sidebar.caption("Universidad Tecnica Federico Santa María")


##################################################################################################
############## Tabla con los datos ############################################
##################################################################################################
path=r'..\Datos\kd.blocks.csv'
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